'''
Author: Nikola Medimurac
This module is used to define all the data used by the website
and functions to interface with the data
website_data must not be accessed anywhere outside this module
Additional keys and functiosn can be added as neccesary
'''
# import hashlib

# pylint: disable=global-statement,invalid-name

# Make 1 big dictionary that contains all the data relating to the website
# Add more keys to this dictionary as required
website_data = {}

# Define valid react ids, this is so it is extensible in the future if needed
valid_react_ids = [1]

# Define all valid data structures used to interface with this server
# This is used to check what inputs are valid, for quickly generating test
# data and to be used as a reference
data_types = {'email'   : 'test@gmail.com',
              'id'      : 1,
              'length'  : 1,
              'password': 'testpass',
              'token'   : 'randomtoken123',
              'message' : 'message',
              'name'    : 'name',
              'code'    : 'code',
              'is_'     : True,
              'time_'   : 1,
              '_id'     : 1,
              '_url'    : 'usr string',
              '_str'    : 'string',
              'end'     : 1,
              'start'   : 1,
              'user'    : {'u_id' : 1,
                           'email' : 'test@gmail.com',
                           'name_first' : 'a',
                           'name_last' : 'b',
                           'handle_str' : 'ab'
                           },
              'users'   : [{'u_id' : 1,
                            'email' : 'test@gmail.com',
                            'name_first' : 'a',
                            'name_last' : 'b',
                            'handle_str' : 'ab'
                           }],
              'messages': [{'message_id' : 1,
                            'u_id' : 1,
                            'message' : 'a',
                            'time_created' : 1,
                            'reacts' : {'react_id' : 1,
                                        'u_ids' : [1, 2],
                                        'is_this_user_reacted' : True,
                                        },
                            'is_pinned' : False,
                            }],
              'channels': [{'channel_id' : 1,
                            'name' : 'name'
                            }],
              'members' : [{'u_id' : 1,
                            'name_first' : 'a',
                            'name_last' : 'b',
                           }],
              'reacts'  : {'react_id' : 1,
                           'u_ids' : [1, 2],
                           'is_this_user_reacted' : True,
                           },
              }


# Methods for interfacing with data, need to pass name of data struct as string
# ******** Getter Functions *************
def get_all_data():
    '''
    Getter method
    Returns the entire website data dictionary
    '''
    global website_data
    return website_data.copy()

def get_data(data_name):
    '''
    Getter method
    Returns corresponding data list under the key in website data
    Data list is given as a string and returns None if no key matches
    '''
    global website_data
    # Check if the key is in the website data, if not return None
    if data_name in website_data:
        return website_data[data_name].copy()
    return None

def get_data_with_id(data_name, data_id):
    '''
    Getter method that returns the data with the corresponding id given
    Returns None if the corresponding id does not exist in the data
    '''
    global website_data
    # Find the position of the data with the corresponding id
    # Return that data or return None if not found
    for index, dic in enumerate(website_data[data_name]):
        if dic['id'] == data_id:
            return website_data[data_name][index].copy()
    return None

def get_valid_react_ids():
    '''
    Getter method
    Returns valid react ids
    '''
    global valid_react_ids
    return valid_react_ids.copy()

def get_data_types():
    '''
    Getter method
    Returns a copy of all valid data types for interface
    '''
    global data_types
    return data_types.copy()

# ******** Setter Functions *************
def set_all_data(new_data):
    '''
    Setter method
    Makes the entire website data equal to given value
    '''
    global website_data
    website_data = new_data

def set_data(data_name, new_data):
    '''
    Setter method
    Makes the entire given data list inside website_data equal to given value
    '''
    global website_data
    # Check if the key is in the website data, if not do nothing
    if data_name in website_data:
        website_data[data_name] = new_data

def append_data(data_name, new_data):
    '''
    Setter method
    Appends a new entry to the end of a given data list in website_data
    '''
    global website_data
    # Check if the key is in the website data, if not return None
    if data_name in website_data:
        website_data[data_name].append(new_data)

def set_data_with_id(data_name, data_id, new_data):
    '''
    Setter method that replaces the data with the corresponding id with the new data
    Returns None if the correspodning id does not exist in the data
    '''
    global website_data
    # Find the position of the data with the corresponding id
    for index, dic in enumerate(website_data[data_name]):
        if dic['id'] == data_id:
            # Set the data to the new value at that point
            website_data[data_name][index] = new_data

# ************ Other Functions ***************
def get_id_from_token(token):
    '''
    Given a token get the corresponding id of the user
    '''
    # Find the value of the token in the list of valid tokens
    for valid_token in website_data['valid tokens']:
        if valid_token['token'] == token:
            return valid_token['user id']
    return None

def clear_all_data():
    '''
    Function to reset the server data to the intial empty state
    '''
    global website_data
    initial_id_data = {'user id' : 0, 'channel id' : 0, 'message id' : 0}
    website_data = {'user data'     : [],
                    'channel data'  : [],
                    'message data'  : [],
                    'valid tokens'  : [],
                    'next id'       : initial_id_data,
                    'send later'    : [],
                    'special users' : [],
                    'reset code' : [],
                   }
    set_all_data(website_data)

def get_next_id(data_name):
    '''
    Function that gets the value of the next id for a specified data struct
    Increments this value in memory as well when called so always unique
    '''
    global website_data
    website_data['next id'][data_name] += 1
    return website_data['next id'][data_name] - 1
