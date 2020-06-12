'''
Author: Nikola Medimurac, William Dieu
Implementation of authorisation related backend functions
'''

import hashlib
import re
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from error import InputError
import website_data as wd


# *********** Helper Functions ***************
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

def send_reset_code(email):
    '''
    Helper function that sends sets up a SMTP connection and sends an email to the user
    '''
    # Set up connection with Gmail's SMTP server and creating reset code
    sender_email = "bigpythonenergy@gmail.com"
    password = "G}'R.em&9-cRY}'x?wkUr}9`8"
    reset_code = hashlib.sha256(email.encode()).hexdigest()
    # Create message to send reset code to user
    message = MIMEMultipart("alternative")
    message["Subject"] = "Reset Code"
    message["From"] = sender_email
    message["To"] = email
    text = "Your reset code is: " + reset_code
    message.attach(MIMEText(text, "plain"))
    # Send message to user's email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, email, message.as_string())
    return reset_code

# ********** Functions for Auth *******
def auth_login(email, password):
    '''
    Function for logging in an already existing user in the database
    Returns a token which can be used to authenticate the user
    '''
    # First check that the email given is valid and used
    # Checking if the email is valid
    if not is_valid_email(email):
        raise InputError(description="Invalid email given")
    # Now find the corresponding user data given the email
    all_user_data = wd.get_data('user data')
    for user_data in all_user_data:
        if user_data['email'] == email:
            # Check that the password given matches
            password_hashed = hashlib.sha256(password.encode()).hexdigest()
            if user_data['password'] != password_hashed:
                raise InputError(description="Incorrect password")
            # Since password is correct, get token and id and return it
            # Also add the token to the list of valid tokens
            token = hashlib.sha256((email + str(user_data['id'])).encode()).hexdigest()
            wd.append_data('valid tokens', {'user id' : user_data['id'], 'token' : token})
            return {'u_id' : user_data['id'], 'token' : token}
    # If the email does not correspond to any user's email, it is unused
    raise InputError(description="Email does not belong to any user")

def auth_logout(token):
    '''
    Function for logging out the user
    This removes their token from the list of valid tokens
    '''
    # Check that the token given is a valid token
    # Remove it if it is and return True, else just return False
    all_valid_tokens = wd.get_data("valid tokens")
    for valid_token in all_valid_tokens:
        if valid_token['token'] == token:
            all_valid_tokens.remove(valid_token)
            wd.set_data("valid tokens", all_valid_tokens)
            return {'is_success' : True}
    return {'is_success' : False}


def auth_register(email, password, name_first, name_last):
    '''
    Function for registering a new user on Slackr
    This takes the details and appends it to the user data structure
    '''
    # First check the inputs given are correct
    # Checking if the email is valid
    if not is_valid_email(email):
        raise InputError(description="Invalid email given")
    # Check email is unused
    all_user_data = wd.get_data("user data")
    if any(user_data['email'] == email for user_data in all_user_data):
        raise InputError(description="Email already belongs to a user")
    # Check password is long enough
    if len(password) < 6:
        raise InputError(description="Password is too short")
    # Check first name is correct length
    if not name_first or len(name_first) > 50:
        raise InputError(description="First name has incorrect length")
    # Check last name is correct length
    if not name_last or len(name_last) > 50:
        raise InputError(description="Last name has incorrect length")

    # Now that the inputs are correct register the user
    # Hash the password so it is not stored in plain text
    password_hashed = hashlib.sha256(password.encode()).hexdigest()
    # Get the new id for the user
    new_id = wd.get_next_id('user id')
    # If first user created then give owner permissions id
    permission_id = 2
    if new_id == 0:
        permission_id = 1
    # Get what the display name of the user should be
    name_combined = name_first.lower() + name_last.lower()
    name_combined = name_combined[:20]
    disp_name = name_combined[:]
    # Check if the display name is already being used
    # If so add an incrementing number in front till unique
    counter = 0
    while is_handle_used(disp_name):
        disp_name = str(counter) + name_combined
        disp_name = disp_name[:20]
        counter += 1
    # Now get the users token so it can be added to the websites data
    # The token is the hash of the users email + id
    token = hashlib.sha256((email + str(new_id)).encode()).hexdigest()
    wd.append_data('valid tokens', {'user id' : new_id, 'token' : token})

    # Create the new user data structure and append it to the list
    new_user_data = {'id'           : new_id,
                     'email'        : email,
                     'first name'   : name_first,
                     'last name'    : name_last,
                     'disp name'    : disp_name,
                     'password'     : password_hashed,
                     'permission id': permission_id,
                     'img name'     : '',
                    }
    wd.append_data('user data', new_user_data)
    return {'u_id' : new_id, 'token' : token}

def auth_passwordreset_request(email):
    '''
    Function for sending a reset code to an email
    '''
    # First check if the email is valid
    if not is_valid_email(email):
        raise InputError(description="Invalid email given")
    # Now find the corresponding user given the email
    all_user_data = wd.get_data('user data')
    for user_data in all_user_data:
        if user_data['email'] == email:
            # Send the user a reset code to their email and add code to database
            code = send_reset_code(email)
            wd.append_data('reset code', {'code' : code, 'email' : email})

    # If email does not correspond to a user, it is unused.
    # Does not raise an error to prevent individual from checking if specific
    # emails have registered on this site
    return {}

def auth_passwordreset_reset(reset_code, new_password):
    '''
    Function for resetting a password from a reset code
    '''
    # First check password is long enough
    if len(new_password) < 6:
        raise InputError(description="Password is too short")
    # Check if the database has any entries before checking
    all_reset_codes = wd.get_data('reset code')
    if not all_reset_codes:
        raise InputError(description="Reset code is not valid")
    # Check if the reset code is a valid code
    for reset in all_reset_codes:
        if reset['code'] == reset_code:
            reset_email = reset['email']
        else:
            raise InputError(description="Reset code is not valid")
    # Remove reset code from database
    all_reset_codes.remove(reset) #pylint: disable=undefined-loop-variable
    wd.set_data('reset code', all_reset_codes)
    # Hash the password so it is not stored in plain text
    password_hashed = hashlib.sha256(new_password.encode()).hexdigest()
    # Save the new password in database
    all_user_data = wd.get_data("user data")
    for user_data in all_user_data:
        if user_data['email'] == reset_email:
            user_data['password'] = password_hashed
    wd.set_data_with_id('user data', user_data['id'], user_data) #pylint: disable=undefined-loop-variable
    return {}
