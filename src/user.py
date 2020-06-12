'''
Author: Nikola Medimurac
Implementation of user related functions for backend
'''
import urllib.request
import hashlib
import re
from PIL import Image
import website_data as wd
from error import InputError, AccessError

#pylint: disable=too-many-locals
#pylint: disable=too-many-arguments

# ******** Helper Functions for channel ***************
def get_user_id_and_user_data(token):
    '''
    This is a helper function that gets the user_id and user data from website data
    given a token and channel id
    Raises input errors if invalid token is given, channel id doesnt exist or
    user is not a member of the channel
    '''
    # Get the id of the user calling the function from their token
    user_id = wd.get_id_from_token(token)
    if user_id is None:
        raise AccessError(description="Invalid token given")
    # Get the data of the specified user
    user_data = wd.get_data_with_id('user data', user_id)
    return user_id, user_data

def is_handle_used(handle):
    '''
    Helper function that check if a handle is unused
    Returns true if the handle does nto belong to any user
    '''
    # Get data of all the users
    all_user_data = wd.get_data('user data')
    # Loop through all user data, if match occurs return Ture
    for user_data in all_user_data:
        if user_data['disp name'] == handle:
            return True
    # Return False here as no match was found
    return False

def is_valid_email(email):
    '''
    Helper function that checks if the email is
    a valid email
    Return a boolean value
    '''
    # Following the example linked in the specifications
    regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    return bool(re.search(regex, email))

# ************** user functions *****************8
def user_profile(token, u_id, port):
    '''
    Function that is used to get information about user profile
    Returns user data structure as specfified in the specifications
    '''
    # First check if its a special user
    if u_id >= 100000:
        special_user = wd.get_data_with_id('special users', u_id)
        return {'user' : special_user}
    # Check valid token given
    try:
        _, _ = get_user_id_and_user_data(token)
    except Exception as err:
        raise err
    # Get the user data of the u_id given
    user_data = wd.get_data_with_id('user data', u_id)
    # Convert user data to the user data type from the specifications
    user = {'u_id'          : user_data['id'],
            'email'         : user_data['email'],
            'name_first'    : user_data['first name'],
            'name_last'     : user_data['last name'],
            'handle_str'    : user_data['disp name']
           }
    # If they have a profile picture then add that field in
    if user_data['img name'] != '':
        user['profile_img_url'] = 'http://localhost:' + str(port) + '/profile_imgs/'
        user['profile_img_url'] += user_data['img name'] + '.jpg'
    return {'user' : user}

def user_profile_setname(token, name_first, name_last):
    '''
    Function that is used to change the users first and last name
    Returns nothing but mdifies the database in the website
    '''
    # Get user id and user data from token and channel_id
    try:
        user_id, user_data = get_user_id_and_user_data(token)
    except Exception as err:
        raise err
    # Check that the names given are valid inputs
    if not isinstance(name_first, str):
        raise InputError(description="first name must be a string")
    if not isinstance(name_last, str):
        raise InputError(description="last name must be a string")
    # Check that the names are not whitespace characters
    if name_first.isspace() or name_first is None:
        raise InputError(description="first name must not be invalid")
    if name_last.isspace() or name_last is None:
        raise InputError(description="last name must not be invalid")
    # Check first name is correct length
    if not name_first or len(name_first) > 50:
        raise InputError(description="First name has incorrect length")
    # Check last name is correct length
    if not name_last or len(name_last) > 50:
        raise InputError(description="Last name has incorrect length")

    # Set the new values of first and last name and save in database
    user_data['first name'] = name_first
    user_data['last name'] = name_last
    wd.set_data_with_id('user data', user_id, user_data)
    return {}

def user_profile_setemail(token, email):
    '''
    Function that is used to change the email of the user
    Returns nothing but mdifies the database in the website
    '''
    # Get user id and user data from token
    try:
        user_id, user_data = get_user_id_and_user_data(token)
    except Exception as err:
        raise err
    # Checking if the email is valid
    if not isinstance(email, str):
        raise InputError(description="email must be a string")
    if not is_valid_email(email):
        raise InputError(description="Invalid email given")
    # Check email is unused
    all_user_data = wd.get_data("user data")
    if any(user_data['email'] == email for user_data in all_user_data):
        raise InputError(description="Email already belongs to a user")

    # Set the new values of first and last name and save in database
    user_data['email'] = email
    wd.set_data_with_id('user data', user_id, user_data)
    return {}

def user_profile_sethandle(token, handle_str):
    '''
    Function that is used to change the users display name
    Returns nothing but mdifies the database in the website
    '''
    # Get user id and user data from token and channel_id
    try:
        user_id, user_data = get_user_id_and_user_data(token)
    except Exception as err:
        raise err
    # Check valid handle is given
    if not isinstance(handle_str, str):
        raise InputError(description="Display name must be a string")
    # Check first name is correct length
    if len(handle_str) < 2 or len(handle_str) > 20:
        raise InputError(description="Display name is incorrect length")
    # Check it is unique
    if is_handle_used(handle_str):
        raise InputError(description="Display name already taken by a user")

    # Set the new values of first and last name and save in database
    user_data['disp name'] = handle_str
    wd.set_data_with_id('user data', user_id, user_data)
    return {}

def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    '''
    Function that lets a user update their profile picture
    Given a url and the dimensions, this function will go the url,
    grab the image, crop the image, save it and link it to their profile
    '''
    # Get user id and user data from token and channel_id
    try:
        user_id, user_data = get_user_id_and_user_data(token)
    except Exception as err:
        raise err
    # Check the dimensions given are valid (start < end) and save them in a tuple
    if x_start >= x_end or y_start >= y_end:
        raise InputError("Invalid dimensions, start must be less than end value")
    dimensions = (x_start, y_start, x_end, y_end)
    # Grab the contents from the url
    print(img_url)
    try:
        url_image = urllib.request.urlopen(img_url)
    except urllib.error.HTTPError:
        raise InputError(description='Did not get status 200')
    # Load in the image using PIL
    try:
        im = Image.open(url_image) #pylint: disable=invalid-name
    except IOError:
        raise InputError(description="Could not load an image from url")
    # Check the image is a jpeg
    if im.format != "JPEG" and im.format != "JPG":
        raise InputError('Image given is not a jpeg image')
    # Get the dimensions of image and check given input fits inside
    width, height = im.size
    if x_start < 0 or x_end > width or y_start < 0 or y_end > height:
        print('Invalid dimensions, not within image')
    # Crop the image
    im = im.crop(dimensions) #pylint: disable=invalid-name
    # Save the image under a unique name
    # This name will be generated as a hash of the url + dimensions
    image_name = hashlib.sha256((img_url).encode()).hexdigest()
    image_name += '-'+str(x_start)+'-'+str(y_start)+'-'+str(x_end)+'-'+str(y_end)
    # Link profile to this img_url and update user data
    user_data['img name'] = image_name
    wd.set_data_with_id('user data', user_id, user_data)
    # Save the image in memory
    image_path = '../profile_imgs/' + image_name
    im.save(image_path, format='jpeg')
    return {}
