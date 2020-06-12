'''
Author: Nikola Medimurac
Implementation of message related backend functions
'''

from datetime import datetime
import threading
import website_data as wd
import message_commands as mes_com
from message_helper import get_user_id_and_message_data, create_message, check_message_waiting
from error import InputError, AccessError


# ************* Functions for message from specs ****************
def message_send(token, channel_id, message):
    '''
    Function to send messages to channels
    Updates the website_data to store the message appropriatly
    Returns the id of the new message created
    '''
    # Get the current timestamp first so that its more accurate then later
    timestamp = int(datetime.utcnow().timestamp()) + 36000
    # Check the message cotents and check if a command was called
    if message:
        com_called = mes_com.message_command_caller(message, channel_id)
        # If a command was called then dont send the message
        if com_called:
            return {}
    # use the helper function to create the new message data
    try:
        new_message_data = create_message(token, channel_id, message, timestamp)
    except Exception as err:
        raise err
    # Add the new message to the website data
    wd.append_data('message data', new_message_data)
    # Also append the message id to the message list inside the channel data
    channel_data = wd.get_data_with_id('channel data', channel_id)
    channel_data['messages'].append(new_message_data['id'])
    wd.set_data_with_id('channel data', channel_id, channel_data)
    return {'message_id' : new_message_data['id']}

def message_edit(token, message_id, message):
    '''
    Function to edit messages to channels
    Updates the message contents in the database and deleted if set to nothing
    Doesnt return anything
    '''
    # Get the id of the user calling the function from their token
    user_id = wd.get_id_from_token(token)
    if user_id is None:
        raise AccessError(description="Invalid token given")
    # Get the data of the specified message, raise InputError if it doesnt exist
    message_data = wd.get_data_with_id('message data', message_id)
    if message_data is None:
        raise InputError(description="Invalid message id given")
    # Check if the user is in the list of owners or is the one who created the message
    channel_data = wd.get_data_with_id('channel data', message_data['channel id'])
    if user_id not in channel_data['owners'] or user_id != message_data['sender id']:
        raise AccessError(description="User does not have permission to edit message")
    # Check that the message given is not too long
    if len(message) > 1000:
        raise InputError(description="Message is too long")

    # Now replace the contents of the message or delete if input is empty string
    if not message:
        all_message_data = wd.get_data('message data')
        all_message_data.remove(message_data)
        wd.set_data('message data', all_message_data)
        channel_data['messages'].remove(message_id)
        wd.set_data_with_id('channel data', channel_data['id'], channel_data)
    else:
        message_data['contents'] = message
        wd.set_data_with_id('message data', message_id, message_data)
    return {}

def message_remove(token, message_id):
    '''
    Function to remove messages from a channel
    Works the same as edit with an empty string
    Doesnt return anything
    '''
    message_edit(token, message_id, '')
    return {}

def message_react(token, message_id, react_id):
    '''
    function to allow a user to add a react to a message
    returns empty dictionary but adds react to message data
    '''
    # get user id and message data from token and channel_id
    try:
        user_id, message_data = get_user_id_and_message_data(token, message_id)
    except Exception as err:
        raise err
    # Check react id is a valid number
    if react_id not in wd.get_valid_react_ids():
        raise InputError(description="Invalid react id given")
    # Check if the user has already reacted to this message
    for react in message_data['reacts'][:]:
        if react['user id'] == user_id:
        # Check if its a duplicate, if it is raise input error, if not remove it from list
            if react['react id'] == react_id:
                raise InputError(description="User has already reacted with this react id")
    # Add the new react to the end of the react list
    message_data['reacts'].append({'react id' : react_id, 'user id' : user_id})
    return {}

def message_unreact(token, message_id, react_id):
    '''
    function to allow a user to remove a react from a message
    returns empty dictionary but removes react from message data
    '''
    # get user id and message data from token and channel_id
    try:
        user_id, message_data = get_user_id_and_message_data(token, message_id)
    except Exception as err:
        raise err
    # Check react id is a valid number
    if react_id not in wd.get_valid_react_ids():
        raise InputError(description="Invalid react id given")
    # Find the users react in the list
    for react in message_data['reacts'][:]:
        # Loop through until we find a react by the user
        if react['user id'] == user_id:
            # Check if the react matches the given id
            if react['react id'] == react_id:
                message_data['reacts'].remove(react)
                wd.set_data_with_id('message data', message_id, message_data)
                return {}
    # If we get here then the react wasnt found and so doesnt exist
    raise InputError(description="User has not reacted with this react id")

def message_pin(token, message_id):
    '''
    function to allow a user to mark a message as pinned
    returns empty dictionary but changes message data internally
    '''
    # get user id and message data from token and channel_id
    try:
        user_id, message_data = get_user_id_and_message_data(token, message_id)
    except Exception as err:
        raise err
   # Get the user data to check if the user is an owner
    user_data = wd.get_data_with_id('user data', user_id)
    if user_data['permission id'] != 1:
        # Spec says InputError but sounds like it should be AccessError??
        raise InputError(description="User is not an owner of the Slackr")
    # Check if the message was already unpinned
    if message_data['pinned']:
        raise InputError(description="Message is already pinned")
    # If the user is an owner then set the data for the message pin as true
    message_data['pinned'] = True
    wd.set_data_with_id('message data', message_id, message_data)
    return {}

def message_unpin(token, message_id):
    '''
    function to allow a user to unmark a message as pinned
    returns empty dictionary but changes message data internally
    '''
    # get user id and message data from token and channel_id
    try:
        _, message_data = get_user_id_and_message_data(token, message_id)
    except Exception as err:
        raise err
   # Get the user data to check if the user is an owner
    user_data = wd.get_data_with_id('user data', message_data['sender id'])
    if user_data['permission id'] != 1:
        # Spec says InputError but sounds like it should be AccessError??
        raise InputError(description="User is not an owner of the Slackr")
    # Check if the message was already unpinned
    if not message_data['pinned']:
        raise InputError(description="Message is already not pinned")
    # If the user is an owner then set the data for the message pin as true
    message_data['pinned'] = False
    wd.set_data_with_id('message data', message_id, message_data)
    return {}

def message_sendlater(token, channel_id, message, time_sent):
    '''
    Function to send messages to channels after a time delay
    Updates the website_data to store the message appropriatly
    Returns the id of the new message created
    '''
    # First check the token is valid
    if wd.get_id_from_token(token) is None:
        raise AccessError(description="Invalid token given")
    # Following the example linked in the specifications to get time stamp
    #timestamp_now = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    timestamp_now = int(datetime.utcnow().timestamp()) + 36000
    # Check that the time is actually in the future
    if timestamp_now > time_sent:
        raise InputError(description="Time to be sent cannot be in the past")
    # If the time stamp is the current time then call message_send normal
    if timestamp_now == time_sent:
        return message_send(token, channel_id, message)
    # Use the helper function to create the new message data
    try:
        new_message_data = create_message(token, channel_id, message, time_sent)
    except Exception as err:
        raise err
    # Add the message to the list of message to be sent later
    wd.append_data('send later', new_message_data)
    # Put a timer to send the message when the time is over
    time_till_send = time_sent - timestamp_now
    send_t = threading.Timer(time_till_send, lambda: check_message_waiting(new_message_data['id']))
    send_t.daemon = True
    send_t.start()
    return {'message_id' : new_message_data['id']}
