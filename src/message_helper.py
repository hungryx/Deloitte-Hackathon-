'''
Author: Nikola Medimurac
Helper functions for message related functions
'''
from datetime import datetime
import website_data as wd
from error import InputError, AccessError


# ******** Helper Functions for messages ***************
def get_user_id_and_message_data(token, message_id):
    '''
    This is a helper function that gets the user_id and message data from website data
    given a token and channel id
    Raises input errors if invalid token is given, message id doesnt exist or
    user is not a member of the channel the message was sent in
    '''
    # Get the id of the user calling the function from their token
    user_id = wd.get_id_from_token(token)
    if user_id is None:
        raise AccessError(description="Invalid token given")
    # Get the data of the specified message, raise InputError if it doesnt exist
    message_data = wd.get_data_with_id('message data', message_id)
    if message_data is None:
        raise InputError(description="Invalid message id given")
    # Check if the user is in the list of members
    channel_data = wd.get_data_with_id('channel data', message_data['channel id'])
    if user_id not in channel_data['members']:
        raise AccessError(description="User is not member of channel the message is in")
    return user_id, message_data

def create_message(token, channel_id, message, timestamp):
    '''
    Helper function for creating a new message with a specified time stamp
    This is made as a helper function so message_send and message_send_later can use it
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
    # Check that the message isn't None
    if not message:
        raise InputError(description="Invalid message id given")
    # Check that the message given is not too long
    if len(message) > 1000:
        raise InputError(description="Message is too long")
    # Check that the message given is empty
    if not message:
        raise InputError(description="Message can not be empty")

    # Get the id value of the new message, this is 1 higher then the last message id
    # If first message created then set message id as 0
    new_id = wd.get_next_id('message id')
    # Create message data structure and append it to message list
    new_message_data = {'id'            : new_id,
                        'sender id'     : user_id,
                        'channel id'    : channel_id,
                        'contents'      : message,
                        'timestamp'     : timestamp,
                        'pinned'        : False,
                        'reacts'        : []
                       }
    return new_message_data


def create_message_special_user(user_id, channel_id, message):
    '''
    Helper function for creating a new message by a special user
    This is currently only used for the hangman bot to post messages
    '''
    # Get the timestamp when the message was called to make
    timestamp = int(datetime.utcnow().timestamp()) + 36000
    # Get the data of the specified channel, raise InputError if it doesnt exist
    channel_data = wd.get_data_with_id('channel data', channel_id)
    if channel_data is None:
        return
    # Check that the message given is not too long or empty
    if len(message) > 1000 or not message:
        return

    # Get the id value of the new message, this is 1 higher then the last message id
    # If first message created then set message id as 0
    new_id = wd.get_next_id('message id')
    # Create message data structure and append it to message list
    new_message_data = {'id'            : new_id,
                        'sender id'     : user_id,
                        'channel id'    : channel_id,
                        'contents'      : message,
                        'timestamp'     : timestamp,
                        'pinned'        : False,
                        'reacts'        : []
                       }
    # Add the new message to the website data
    wd.append_data('message data', new_message_data)
    # Also append the message id to the message list inside the channel data
    channel_data = wd.get_data_with_id('channel data', channel_id)
    channel_data['messages'].append(new_message_data['id'])
    wd.set_data_with_id('channel data', channel_id, channel_data)


def check_message_waiting(message_id):
    '''
    Function that given a message in the send later waiting list
    will send the corressponding message to the channel
    Will not send the message if the time now is less then the time
    to be sent
    This Function takes in the id of the message and returns True if sent False if not sent
    It also will do nothing if given an incorrect input
    '''
    message_data = wd.get_data_with_id('send later', message_id)
    if message_data is None:
        return False
    # Get the current timestamp first so that its more accurate then later
    # following the example linked in the specifications
    timestamp_now = int(datetime.utcnow().timestamp()) + 36000
    # Check that the current time is passed or equal to when the message should be sent
    if timestamp_now < message_data['timestamp']:
        return False
    # Move the message data to the message data section of the database
    wd.append_data('message data', message_data)
    # Also append the message id to the message list inside the channel data
    channel_data = wd.get_data_with_id('channel data', message_data['channel id'])
    channel_data['messages'].append(message_data['id'])
    wd.set_data_with_id('channel data', message_data['channel id'], channel_data)
    # Remove message data from the send later list now that its sent
    all_send_later_data = wd.get_data('send later')
    all_send_later_data.remove(message_data)
    wd.set_data('send later', all_send_later_data)
    return True
