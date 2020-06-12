'''
Author: Nikola Medimurac
Implementation of other functions ignoring flask stuff
These functions include:
    - search
    - users_all
    - admin_user_permission_change
    - workspace_reset
    - admin_user_remove
'''
# List of dictionaries, where each dictionary contains
# types u_id, email, name_first, name_last, handle_str

import channels
import auth
import website_data as wd
from error import AccessError, InputError

# ************ Helper Functions **********
def user_data_to_users(user_data):
    '''
    This function takes in an entry from the list of "user data"
    and converts it to a dictionary of type users (described in specs)
    '''
    user = {}
    user['u_id'] = user_data['id']
    user['email'] = user_data['email']
    user['name_first'] = user_data['first name']
    user['name_last'] = user_data['last name']
    user['handle_str'] = user_data['disp name']
    return user


def meassage_data_to_message(user_id, message_data):
    '''
    This function takes in an entry from the list of "message data"
    and converts it to a dictionary of type message (described in specs)
    '''
    message = {}
    message['message_id'] = message_data['id']
    message['u_id'] = message_data['id']
    message['message'] = message_data['contents']
    message['time_created'] = message_data['timestamp']
    # Get the react data for the message
    message['reacts'] = []
    for react_id in wd.get_valid_react_ids():
        # Create react data for each react id, set react id first
        react_data = {}
        react_data['react_id'] = react_id
        # Iterate through the list of reacts and add them to the list if same id
        react_data['u_ids'] = []
        for react in message_data['reacts']:
            if react['react id'] == react_id:
                react_data['u_ids'].append(react['user id'])
        # Check if user id is in the list
        if user_id in react_data['u_ids']:
            react_data['is_this_user_reacted'] = True
        else:
            react_data['is_this_user_reacted'] = False
        # Attach react data to list of reacts
        message['reacts'].append(react_data)
    message['is_pinned'] = message_data['pinned']
    return message

# ********** Other Functions **************

def search(token, string):
    '''
    Function that finds all the messages that contain a string
    that matches the one given
    Returns messages satifying this condtion
    '''
    # Get the id of the user calling the function from their token
    user_id = wd.get_id_from_token(token)
    if user_id is None:
        raise AccessError(description="Invalid token given")
    # Split the query string up into seperate words
    query = string.split(' ')
    # Get the ids of all channels the user is in
    user_channels = channels.channels_list(token)
    # Iterate through each channels messages and check if any have a match
    message_list = []
    for channel in user_channels['channels']:
        channel_data = wd.get_data_with_id("channel data", channel['channel_id'])
        for message_id in channel_data['messages']:
            message_data = wd.get_data_with_id("message data", message_id)
            # iterate through each word in the message
            counter = 0
            for word in message_data['contents'].split(' '):
                # Check if the the word matches the first word in the query
                if word == query[counter]:
                    counter += 1
                    if counter == len(query):
                        # append message to list if we find a match
                        message = meassage_data_to_message(user_id, message_data)
                        message_list.append(message)
                        break
                else:
                    # if the words dont match then reset the match counter
                    counter = 0
    # Now that we have a list of all messages containing the query sort it
    message_list_sorted = sorted(message_list, key=lambda k: k['message_id'])
    message_list_sorted = sorted(message_list_sorted, key=lambda k: k['time_created'])
    # Reverse this to get the newest message first
    message_list_sorted = message_list_sorted[::-1]
    return {'messages' : message_list_sorted}

def users_all(token):
    '''
    Function that returns a list of all users
    Converts the user data structure in website data
    to a structure that matches the specification
    '''
    # Get the id of the user calling the function from their token
    user_id = wd.get_id_from_token(token)
    if user_id is None:
        raise AccessError(description="Invalid token given")
    # Get all the data related to users
    all_user_data = wd.get_data('user data')
    # Iterate through each user data and add it to the list
    user_list = []
    for user_data in all_user_data:
        user_list.append(user_data_to_users(user_data))
    return {'users' : user_list}

def admin_user_permission_change(token, change_user_id, permission_id):
    '''
    Function to change the permission id of a user
    currently only 2 types of permission ids
    Only an owner can change permissions of another user
    This functions returns nothing
    '''
    # Get the id of the user calling the function from their token
    user_id = wd.get_id_from_token(token)
    if user_id is None:
        raise AccessError(description="Invalid token given")
    # Get the data of the user calling this function to see if they have permission
    user_data = wd.get_data_with_id('user data', user_id)
    if user_data['permission id'] != 1:
        raise AccessError(description="User is not a slack owner")
    # Check correct permission id is given
    if permission_id != 1 and permission_id != 2: #pylint: disable=consider-using-in
        raise InputError(description="Invalid permission id given")
    # Check the user id to change is valid and get their data
    change_user_data = wd.get_data_with_id('user data', change_user_id)
    if change_user_data is None:
        raise InputError(description="User id given does not exist")
    # Change the users data to the new permission id
    change_user_data['permission id'] = permission_id
    wd.set_data_with_id('user data', change_user_id, change_user_data)
    return {}

def admin_user_remove(token, u_id):
    '''
    Function to remove a user from the slackr workspace
    Must be an owner to use this function
    This functions returns nothing
    '''
    # Get the id of the user calling the function from their token
    user_id = wd.get_id_from_token(token)
    if user_id is None:
        raise AccessError(description="Invalid token given")
    # Get the data of the user calling this function to see if they have permission
    user_data = wd.get_data_with_id('user data', user_id)
    if user_data['permission id'] != 1:
        raise AccessError(description="User calling this is not a slack owner")
    # Check the user id to remove is valid and get their data
    rm_user_data = wd.get_data_with_id('user data', u_id)
    if rm_user_data is None:
        raise InputError(description="User id given does not exist")
    # Now start updating memory to remove all this users stuff
    # Remove from users
    all_user_data = wd.get_data('user data')
    all_user_data.remove(rm_user_data)
    wd.set_data('user data', all_user_data)
    # Remove user from channels list of members and update standup creator to be deleted user
    all_channel_data = wd.get_data('channel data')
    for i in range(len(all_channel_data)): #pylint: disable=consider-using-enumerate
        if u_id in all_channel_data[i]['members']:
            all_channel_data[i]['members'].remove(u_id)
        if u_id in all_channel_data[i]['owners']:
            all_channel_data[i]['owners'].remove(u_id)
        if u_id == all_channel_data[i]['standup creator']:
            all_channel_data[i]['standup creator'] = 100001
    wd.set_data('channel data', all_channel_data)
    # Update messages to be from deleted user
    all_message_data = wd.get_data('message data')
    for i in range(len(all_message_data)): #pylint: disable=consider-using-enumerate
        if u_id == all_message_data[i]['sender id']:
            all_message_data[i]['sender id'] = 100001
    # Invalidate the token of the deleted user if they are online
    all_valid_tokens = wd.get_data('valid tokens')
    for valid_token in all_valid_tokens:
        if valid_token['user id'] == u_id:
            auth.auth_logout(valid_token['token'])

def workspace_reset():
    '''
    Function that reset the workspace back to original default state
    Has no inputs or outputs
    '''
    # Call the clear all data function in website_data
    wd.clear_all_data()
    return {}
