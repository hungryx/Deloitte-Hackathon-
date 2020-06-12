'''
Author: Nikola Medimurac
Implementation of standup functions ignoring flask stuff
For InputErrors raised by an invalid channel, a valid channel
is considered an existing channel the user is a member of
If the user is not a member is raises an AccessError instead
this makes more sense then the spe
'''

import threading
from datetime import datetime
import website_data as wd
from error import InputError, AccessError

# ****** Helper Functions not in spec ***********
def finish_standup(channel_id):
    '''
    This function is called when a standup is finished
    posts the messages from the standup and resets the standup data
    Returns nothing
    '''
    channel_data = wd.get_data_with_id('channel data', channel_id)
    new_id = wd.get_next_id('message id')
    # Create a new message using the data from the standup
    # Cant use other message function since this is slightly different
    new_message = {'id'         : new_id,
                   'sender id'  : channel_data['standup creator'],
                   'channel id' : channel_id,
                   'contents'   : channel_data['standup message'],
                   'timestamp'  : channel_data['standup time'],
                   'pinned'     : False,
                   'reacts'     : []
                  }
    wd.append_data('message data', new_message)
    # Also append the message id to the message list inside the channel data
    channel_data['messages'].append(new_id)
    # Update data in channel to show there is no standup active
    channel_data['standup time'] = None
    channel_data['standup creator'] = None
    channel_data['standup message'] = ''
    wd.set_data_with_id('channel data', channel_id, channel_data)

def get_user_id_and_channel_data(token, channel_id):
    '''
    This is a helper function that gets the user_id and channel data from website data
    given a token and channel id
    Raises input errors if invalid token is given, channel id doesnt exist or
    user is not a member of the channel
    '''
    # Get the id of the user calling the function from their token
    user_id = wd.get_id_from_token(token)
    if user_id is None:
        raise AccessError(description="Invalid token given")
    # Get the data of the specified channel, raise InputError if it doesnt exist
    channel_data = wd.get_data_with_id('channel data', channel_id)
    if channel_data is None:
        raise InputError(description="Invalid channel id given")
    # Check if the user is in the list of members in the channel
    if user_id not in channel_data['members']:
        raise AccessError(description="User is not a member of the channel")
    return user_id, channel_data

# ********* Standup functions in specs ***********
def standup_start(token, channel_id, length):
    '''
    Function to begin a standup in a channel
    Sets the time that the stand up will end in data
    Returs the timestamp of when the standup will end
    '''
    # Get user id and channel data from token and channel_id
    try:
        user_id, channel_data = get_user_id_and_channel_data(token, channel_id)
    except Exception as err:
        raise err
    # Check that there is not currently an active standup
    standup_status = standup_active(token, channel_id)
    if standup_status['is_active']:
        raise InputError(description="Already an active standup")
    # If valid to start standup then set up channel data to indicate when standup ends and creator
    #timestamp_now = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    timestamp_now = int(datetime.utcnow().timestamp()) + 36000
    timestamp_done = timestamp_now + length
    channel_data['standup time'] = timestamp_done
    channel_data['standup message'] = ''
    channel_data['standup creator'] = user_id
    wd.set_data_with_id('channel data', channel_id, channel_data)
    standup_timer = threading.Timer(length, lambda: finish_standup(channel_id))
    standup_timer.start()
    return {'time_finish' : timestamp_done}


def standup_active(token, channel_id):
    '''
    Function to check if a standup is active
    Returns a bool value if the standup is active and
    the timestamp for when the standup will finish
    '''
    # Get user id and channel data from token and channel_id
    try:
        _, channel_data = get_user_id_and_channel_data(token, channel_id)
    except Exception as err:
        raise err
    # Check the standup time field in channel data
    standup_time = channel_data['standup time']
    if standup_time is None:
        return {'is_active' : False, 'time_finish' : None}
    # Get current time stamp
    #timestamp_now = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    timestamp_now = int(datetime.utcnow().timestamp()) + 36000
    # Check if the time stamp is passed the end of the standup
    if timestamp_now > channel_data['standup time']:
        return {'is_active' : False, 'time_finish' : None}
    # If none condition met are above then standup is active
    return {'is_active' : True, 'time_finish' : channel_data['standup time']}


def standup_send(token, channel_id, message):
    '''
    Function that will add a message to the message buffer
    This total message will be displayed at the end of the standup
    This function also does not return anything
    '''
    # Get user id and channel data from token and channel_id
    try:
        user_id, channel_data = get_user_id_and_channel_data(token, channel_id)
    except Exception as err:
        raise err
    # Check that a standup is active
    standup_status = standup_active(token, channel_id)
    if not standup_status['is_active']:
        raise InputError(description="No active standup")
    # Check the message is correct length
    if not message or len(message) > 1000:
        raise InputError(description="Message is incorrect length")
    # If all the inputs are valid, append the message to the current standup message
    # Create a new line in the message if not the first message
    if channel_data['standup message']:
        channel_data['standup message'] += '\n'
    # Put the users display name in front of the message
    user_data = wd.get_data_with_id('user data', user_id)
    message_with_name = user_data['disp name'] + ': ' + message
    # Add the message to the total message and save it in the website data
    channel_data['standup message'] += message_with_name
    wd.set_data_with_id('channel data', channel_id, channel_data)
    return {}
