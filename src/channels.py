'''
Author: Nikola Medimurac
Implementation of channels related functions for backend
'''

import website_data as wd
from error import InputError, AccessError

def channels_list(token):
    '''
    Function for getting a list of every channel the user is in
    Returns a dictionary conatining a list of 'channel_id' and 'name'
    '''
    # Get the id of the user calling the function from their token
    user_id = wd.get_id_from_token(token)
    if user_id is None:
        raise AccessError(description="Invalid token given")
    # Iterate through every channel and add every channel user in to a list
    # Might be innefficent for very big lists but this is small scale
    channel_list = []
    all_channel_data = wd.get_data('channel data')
    for channel_data in all_channel_data:
        if user_id in channel_data['members']:
            channel_list.append({'channel_id' : channel_data['id'], 'name' : channel_data['name']})
    return {'channels' : channel_list}

def channels_listall(token):
    '''
    Function for getting a list of every channel including private channels
    Returns a dictionary conatining a list of 'channel_id' and 'name'
    '''
    # Get the id of the user calling the function from their token
    # Dont need id for this function but we still need to check its an existing user
    user_id = wd.get_id_from_token(token)
    if user_id is None:
        raise AccessError(description="Invalid token given")
    # Iterate through every channel and add every channel user in to a list
    # Might be innefficent for very big lists but this is small scale
    channel_list = []
    all_channel_data = wd.get_data('channel data')
    for channel_data in all_channel_data:
        channel_list.append({'channel_id' : channel_data['id'], 'name' : channel_data['name']})
    return {'channels' : channel_list}

def channels_create(token, channel_name, is_public):
    '''
    Function for creating a new channel
    Appends the new channel data to the end of the channel data list
    Also returns the id value of the new channel
    '''
    # Get the id of the user calling the function from their token
    user_id = wd.get_id_from_token(token)
    if user_id is None:
        raise AccessError(description="Invalid token given")
    # Check that the channel name is not too long
    if len(channel_name) > 20:
        raise InputError(description="Channel name is too long")
    # Get the id value of the new channel, this is 1 higher then the last channel id
    # If first channel created then set channel id as 0
    new_id = wd.get_next_id('channel id')
    # Create the new channel data
    new_channel_data = {'id'        : new_id,
                        'name'      : channel_name,
                        'members'   : [user_id],
                        'owners'    : [user_id],
                        'messages'  : [],
                        'public'    : is_public,
                        'standup time' : None,
                        'standup creator' : None,
                        'standup message' : '',
                        'hangman word' : None,
                        'hangman guesses' : [],
                        }
    wd.append_data('channel data', new_channel_data)
    return {'channel_id' : new_id}
