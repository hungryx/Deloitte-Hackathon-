# ************************************************
# File for testing functions related to messaging
# Author: Nikola Medimurac
# Date Started: 3/3/2020
# ************************************************

'''
Tests for the implementation of message
'''

from datetime import datetime, timezone
import time
import pytest
import auth
import channel
import channels
import message
from error import InputError, AccessError
import website_data as wd

# pylint: disable=redefined-outer-name

@pytest.fixture
def make_two_users():
    '''
    create fixture that resets the server state so that there are only 2 users
    '''
    wd.clear_all_data()
    user1 = auth.auth_register('user1@gmail.com', 'thisismypassword', 'myfirstname', 'mylastname')
    user2 = auth.auth_register('myemail@gmail.com', '123idk', 'name', 'anothername')
    return (user1, user2)


# **************** Testing message_send() Function *****************
def test_send_functional_message(make_two_users):
    '''
    Test function for testing messages under normal conditions
    '''
    # Get data for two users
    user1, _ = make_two_users
    # Create a channel by user 1
    channel_1_name = 'test chan'
    channel_1_id = channels.channels_create(user1['token'], channel_1_name, True)['channel_id']
    # Create messages and keep time stamp of first one saved
    message_1_id = message.message_send(user1['token'], channel_1_id, 'Hello World!')['message_id']
    # Get time stamp of when the message was sent
    message_1_timestamp = int(datetime.utcnow().timestamp()) + 36000
    # Try the edge case of sending 1000 characters
    message.message_send(user1['token'], channel_1_id, 'a' * 1000)

    # Get the messages in the channel using channel_messages
    message_list = channel.channel_messages(user1['token'], channel_1_id, 0)
    message_1_content = message_list['messages'][1]
    # Check only 2 messages were sent to the channel
    assert len(message_list['messages']) == 2
    # Check contents of message is correct
    assert message_1_content['message_id'] == message_1_id
    assert message_1_content['u_id'] == user1['u_id']
    assert message_1_content['message'] == 'Hello World!'
    # Try check the timestamp with both the timestamp value and 1 behind in case
    # they ticked over before we recorded it
    assert message_1_content['time_created'] == message_1_timestamp or message_1_content[
        'time_created'] == message_1_timestamp - 1


def test_send__message_invalid_input(make_two_users):
    '''
    Test message send for invalid inputs
    Invalid inputs are when the string is >1000 characters long or empty
    Empty messages is an invalid input in the assumptions (illogical to send)
    '''
    # Get data for two users
    user1, _ = make_two_users
    # Create a channel by user 1
    channel_1_name = 'test chan'
    channel_1_id = channels.channels_create(user1['token'], channel_1_name, True)['channel_id']

    # Check sending messages with invalid inputs
    with pytest.raises(InputError):
        message.message_send(user1['token'], channel_1_id, '')
    with pytest.raises(InputError):
        message.message_send(user1['token'], channel_1_id, 'a' * 1001)
    # Server handles the case of inputs of wrong type so dont need to check anymore
    #with pytest.raises(InputError):
        #message.message_send(user1['token'], channel_1_id, None)
    with pytest.raises(InputError):
        invalid_id = 101
        message.message_send(user1['token'], invalid_id, 'Hello!')

def test_send_message_access_error(make_two_users):
    '''
    Test trying to post message in channel user is not part of
    '''
    # Get data for two users
    user1, user2 = make_two_users
    # Create a channel by user 1
    channel_1_name = 'test chan'
    channel_1_id = channels.channels_create(user1['token'], channel_1_name, True)['channel_id']

    # Get user 2 to try send message to channel 1 which they are not in
    with pytest.raises(AccessError):
        message.message_send(user2['token'], channel_1_id, 'hello what up')


# ****************** Testing remove_message() Function **********************
def test_remove_message_normal(make_two_users):
    '''
    Test removing messages under normal use cases
    '''
    # Get data for two users
    user1, _ = make_two_users
    # Create a channel by user 1
    channel_1_name = 'test chan'
    channel_1_id = channels.channels_create(user1['token'], channel_1_name, True)['channel_id']
    # Create messages and keep time stamp of first one saved
    message_1_id = message.message_send(user1['token'], channel_1_id, 'Hello World!')['message_id']
    message_2_id = message.message_send(user1['token'], channel_1_id, 'Hello again')['message_id']

    # Check message list is correct before removing
    message_list = channel.channel_messages(user1['token'], channel_1_id, 0)
    messages_1_content = message_list['messages'][0]
    messages_2_content = message_list['messages'][1]
    assert len(message_list['messages']) == 2
    assert messages_1_content['message_id'] == message_2_id
    assert messages_2_content['message_id'] == message_1_id

    # Now remove message 1 and check the message list is still correct
    message.message_remove(user1['token'], message_1_id)

    # Check that updated list of messages is still correct
    # message_2_id is now first in list
    message_list = channel.channel_messages(user1['token'], channel_1_id, 0)
    messages_1_content = message_list['messages'][0]
    assert len(message_list['messages']) == 1
    assert messages_1_content['message_id'] == message_2_id


def test_message_remove_invalid(make_two_users):
    '''
    Test invalid input my removing message that doesnt exist
    Try the case of using a previously existing message id and case where it
    never existed
    '''
    # Get data for two users
    user1, _ = make_two_users
    # Create a channel by user 1
    channel_1_name = 'test chan'
    channel_1_id = channels.channels_create(user1['token'], channel_1_name, True)['channel_id']
    # Create messages and keep time stamp of first one saved
    message_1_id = message.message_send(user1['token'], channel_1_id, 'Hello World!')['message_id']
    # Remove the message made
    message.message_remove(user1['token'], message_1_id)

    # Check that input errors are raised
    with pytest.raises(InputError):
        message.message_remove(user1['token'], message_1_id)
    with pytest.raises(InputError):
        message.message_remove(user1['token'], message_1_id + 1)
    with pytest.raises(InputError):
        message.message_remove(user1['token'], -1)


def test_message_remove_access_error(make_two_users):
    '''
    Test removing messages raising access errors correctly
    '''
    # Get data for two users
    user1, user2 = make_two_users
    # Create a channel by user 1 and get user 2 to join it
    channel_1_name = 'test chan'
    channel_1_id = channels.channels_create(user1['token'], channel_1_name, True)['channel_id']
    # Get user 2 to join channel 1
    channel.channel_join(user2['token'], channel_1_id)
    # Create a message
    message_1_id = message.message_send(user1['token'], channel_1_id, 'Hello World!')['message_id']

    # Try get user2 to remove this message as this is the only way the access error can occur
    # Since they are not admin or creator of message
    with pytest.raises(AccessError):
        message.message_remove(user2['token'], message_1_id)


# ******************* Testing message_edit() Function *****************************
def test_message_edit_normal(make_two_users):
    '''
    Test edit messages by checking if message has been altered and is identical
    to edit
    '''
    # Get data for two users
    user1, _ = make_two_users
    # Create a channel by user 1
    channel_1_name = 'test chan'
    channel_1_id = channels.channels_create(user1['token'], channel_1_name, True)['channel_id']
    # Create messages and keep time stamp of first one saved
    message_1_id = message.message_send(
        user1['token'], channel_1_id, 'hello world!'
    )['message_id']
    message_2_id = message.message_send(
        user1['token'], channel_1_id, 'I hate this project'
    )['message_id']
    message_3_id = message.message_send(
        user1['token'], channel_1_id, 'pls can this just be over'
    )['message_id']

    # Check message infomation is correct before editing
    message_list = channel.channel_messages(user1['token'], channel_1_id, 0)
    messages_1_content = message_list['messages'][0]
    messages_2_content = message_list['messages'][1]
    messages_3_content = message_list['messages'][2]
    assert len(message_list) == 3
    assert messages_3_content['message'] == 'hello world!'
    assert messages_2_content['message'] == 'I hate this project'
    assert messages_1_content['message'] == 'pls can this just be over'

    # Now edit message 2 and check everything the new list is still right
    # Also edit message 1 to '' so that it is deleted
    message.message_edit(user1['token'], message_2_id, 'I feel so dead')
    message.message_edit(user1['token'], message_1_id, '')

    # Check new list is correct
    message_list = channel.channel_messages(user1['token'], channel_1_id, 0)
    messages_1_content = message_list['messages'][0]
    messages_2_content = message_list['messages'][1]
    assert len(message_list['messages']) == 2
    assert messages_2_content['message'] == 'I feel so dead'
    assert messages_1_content['message'] == 'pls can this just be over'
    assert messages_1_content['message_id'] == message_3_id


def test_message_edit_input_error(make_two_users):
    '''
    Test edit messages raising input errors correctly
    '''
    # Get data a user
    user1, _ = make_two_users
    # Create a channel by user 1 and send a message in it
    channel_1_name = 'test chan'
    channel_1_id = channels.channels_create(user1['token'], channel_1_name, True)['channel_id']
    message_1_id = message.message_send(user1['token'], channel_1_id, 'Hello World!')
    # Try to edit message in invalid channel or edit message to be >1000 characters
    with pytest.raises(InputError):
        message.message_edit(user1['token'], message_1_id, 'a' * 1001)


def test_message_edit_access_error(make_two_users):
    '''
    Test edit messages raising access errors correctly
    '''
    # Get data for two users
    user1, user2 = make_two_users
    # Create a channel by user 1 and get user 2 to join it
    channel_1_name = 'test chan'
    channel_1_id = channels.channels_create(user1['token'], channel_1_name, True)['channel_id']
    # Get user 2 to join channel 1
    channel.channel_join(user2['token'], channel_1_id)
    # Create a message
    message_1_id = message.message_send(user1['token'], channel_1_id, 'Hello World!')['message_id']
    message_2_id = message.message_send(user1['token'], channel_1_id, 'Hello World!2')['message_id']

    # Try get user2 to remove this message as this is the only way the access error can occur
    # Since they are not admin or creator of message
    with pytest.raises(AccessError):
        message.message_edit(user2['token'], message_1_id, 'random message')
    with pytest.raises(AccessError):
        message.message_edit(user2['token'], message_2_id, '')

# ******************* Testing message_sendlater() Function *****************************
def test_message_sendlater(make_two_users):
    '''
    Test function for testing messages at a scheduled time
    '''
    # Get data for two users
    user1, _ = make_two_users
    # Create a channel by user 1
    channel_1_name = 'test chan'
    channel_1_id = channels.channels_create(user1['token'], channel_1_name, True)['channel_id']
    # Get time stamp of when the message was sent
    timestamp_now = int(datetime.utcnow().timestamp()) + 36000

    time_send = timestamp_now + 2
    message_1_id = message.message_sendlater(user1['token'], channel_1_id,
                                             'Hello World!', time_send)['message_id']
    # Send a second message before scheduled one
    _ = message.message_send(user1['token'], channel_1_id, 'Second message')['message_id']
    # Get the messages in the channel using channel_messages
    message_list = channel.channel_messages(user1['token'], channel_1_id, 0)
    # check that only the message sent now appears in the channel messages
    assert len(message_list['messages']) == 1
    message_2_content = message_list['messages'][0]
    assert message_2_content['message'] == 'Second message'
    # Wait 2 seconds and see if the scheduled message is added to the channel
    # Continually call the checker function during this time as the sever effectively will do this
    time.sleep(2)
    #message.check_message_waiting(message_1_id)
    # Check the messages in the channel now as both should be there and are in right order
    message_list = channel.channel_messages(user1['token'], channel_1_id, 0)
    assert len(message_list['messages']) == 2
    message_2_content = message_list['messages'][1]
    assert message_2_content['message'] == 'Second message'
    message_1_content = message_list['messages'][0]
    assert message_1_content['message'] == 'Hello World!'
    # Check the entire scheduled message is correct
    assert message_1_content['message_id'] == message_1_id
    assert message_1_content['u_id'] == user1['u_id']
    assert message_1_content['message'] == 'Hello World!'
    assert message_1_content['time_created'] == time_send
    assert message_1_content['reacts'] == [{'react_id' : 1,
                                            'u_ids' : [],
                                            'is_this_user_reacted' : False
                                            }]
    assert not message_1_content['is_pinned']


def test_message_sendlater_input_error(make_two_users):
    '''
    Test function for sendlater with incorrect inputs
    '''
    # Get data for a user
    user1, _ = make_two_users
    # Create a channel by user 1 and send a message in it
    channel_1_name = 'test chan'
    channel_1_id = channels.channels_create(user1['token'], channel_1_name, True)['channel_id']
    #message_1_id = message.message_send(user1['token'], channel_1_id, 'Hello World!')
    # Set up valid and invalid time stamp by going back in time
    # Get time stamp of when the message was sent
    timestamp_now = int(datetime.utcnow().timestamp()) + 36000
    time_sent_valid = timestamp_now + 10
    time_sent_invalid = timestamp_now - 10
    # Error for scheduled time being before timestamp_now
    with pytest.raises(InputError):
        message.message_sendlater(user1['token'], channel_1_id, 'a' * 100, time_sent_invalid)
    # Error for scheduled message > 1000 characters
    with pytest.raises(InputError):
        message.message_sendlater(user1['token'], channel_1_id, 'a' * 1001, time_sent_valid)
    # Error for invalid channel ID
    with pytest.raises(InputError):
        message.message_sendlater(user1['token'], (channel_1_id + 1), 'a' * 1001, time_sent_valid)


def test_message_sendlater_access_error(make_two_users):
    '''
    Test for sendlater with access errors
    '''
    # Get data for two users
    user1, user2 = make_two_users
    # Create a channel by user 1 and get user 2 to join it
    channel_1_name = 'test chan'
    channel_1_id = channels.channels_create(user1['token'], channel_1_name, True)['channel_id']
    # Set up a valid time_sent timestamp
    time_sent = int(datetime.now().replace(tzinfo=timezone.utc).timestamp()) + 10
    # Try get user2 to send message in channel they are not in
    with pytest.raises(AccessError):
        message.message_sendlater(user2['token'], channel_1_id, 'random message', time_sent)


# ***************** Testing message_react() and message_unreact Function ************************
def test_message_react_unreact_normal(make_two_users):
    '''
    Test for react and unreact under normal use
    '''
    # Get data for two users
    user1, user2 = make_two_users
    # Create a channel by user 1 and get user 2 to join it
    channel_1_name = 'test chan'
    channel_1_id = channels.channels_create(user1['token'], channel_1_name, True)['channel_id']
    channel.channel_join(user2['token'], channel_1_id)
    # Create message in channel 1
    message_1_id = message.message_send(user1['token'], channel_1_id, 'Hello World!')['message_id']
    # Get user 1 and 2 to react to the message with valid react_id (1)
    react_id = 1
    message.message_react(user1['token'], message_1_id, react_id)
    message.message_react(user2['token'], message_1_id, react_id)
    # Get the messages in the channel using channel_messages by user 1 and 2
    message_list_u1 = channel.channel_messages(user1['token'], channel_1_id, 0)
    message_list_u2 = channel.channel_messages(user2['token'], channel_1_id, 0)
    message_u1_content = message_list_u1['messages'][0]
    message_u2_content = message_list_u2['messages'][0]
    # Check the reacts to the message are correct, user and user 2 should have the same message
    assert message_u1_content['reacts'][0]['is_this_user_reacted']
    assert message_u1_content['reacts'][0]['react_id'] == 1
    assert user1['u_id'] in message_u1_content['reacts'][0]['u_ids']
    assert user2['u_id'] in message_u1_content['reacts'][0]['u_ids']
    assert message_list_u1 == message_list_u2

    # ********* Now check unreacting works **************
    # Get user 2 to unreact the message
    message.message_unreact(user2['token'], message_1_id, react_id)
    # Repeat the process above and check reacts are still correct
    # Get the messages in the channel using channel_messages by user 1 and 2
    message_list_u1 = channel.channel_messages(user1['token'], channel_1_id, 0)
    message_list_u2 = channel.channel_messages(user2['token'], channel_1_id, 0)
    message_u1_content = message_list_u1['messages'][0]
    message_u2_content = message_list_u2['messages'][0]
    # Check the reacts to the message are correct, user and user 2 should have the same message
    assert message_u1_content['reacts'][0]['is_this_user_reacted']
    assert message_u1_content['reacts'][0]['react_id'] == 1
    assert user1['u_id'] in message_u1_content['reacts'][0]['u_ids']
    assert not message_u2_content['reacts'][0]['is_this_user_reacted']
    assert message_u2_content['reacts'][0]['react_id'] == 1
    assert user1['u_id'] in message_u2_content['reacts'][0]['u_ids']


def test_message_react_unreact_input_error(make_two_users):
    '''
    Test for react and unreact with incorrect inputs
    '''
    # Get data for two users
    user1, user2 = make_two_users
    # Create a channel by user
    channel_1_name = 'test chan'
    channel_1_id = channels.channels_create(user1['token'], channel_1_name, True)['channel_id']
    channel.channel_join(user2['token'], channel_1_id)
    # Create message in channel and get user 2 to react to it
    message_1_id = message.message_send(user1['token'], channel_1_id, 'Hello World!')['message_id']
    message.message_react(user2['token'], message_1_id, 1)
    # Set up invalid message_id
    wrong_id = 10
    # React to the message with valid react_id (1) but invalid message_id
    react_id = 1
    with pytest.raises(InputError):
        message.message_react(user1['token'], wrong_id, react_id)
    # react_id is not a valid React ID. The only valid react ID the frontend has is 1
    # Set up invalid react_id (2)
    invalid_react_id = 2
    # React to the message with invalid react_id
    with pytest.raises(InputError):
        message.message_react(user1['token'], message_1_id, invalid_react_id)
    # Message with ID message_id already contains an active React with ID react_id
    # React to a message with valid react
    message.message_react(user1['token'], message_1_id, react_id)
    # Try to react again with the same user
    with pytest.raises(InputError):
        message.message_react(user1['token'], message_1_id, react_id)

    # ***** Test unreact invalid inputs ************
    # React to the message with invalid react_id
    with pytest.raises(InputError):
        message.message_unreact(user2['token'], message_1_id, invalid_react_id)
    # Message with ID message_id already contains an active React with ID react_id
    # unreact to a message with valid react
    message.message_unreact(user2['token'], message_1_id, react_id)
    # Try to react again with the same user
    with pytest.raises(InputError):
        message.message_unreact(user2['token'], message_1_id, react_id)

# ************** Testing message_pin and message_unpin Functions ********************
def test_message_pin_unpin(make_two_users):
    '''
    Test for pin and unpin under normal use
    '''
    # Get data for two users
    user1, _ = make_two_users
    # Create a channel by user 1 and get user 2 to join it
    channel_1_name = 'test chan'
    channel_1_id = channels.channels_create(user1['token'], channel_1_name, True)['channel_id']
    # Create message in channel 1
    message_1_id = message.message_send(user1['token'], channel_1_id, 'Hello World!')['message_id']
    # Get the messages in the channel using channel_messages by user 1
    message_list = channel.channel_messages(user1['token'], channel_1_id, 0)
    message_content = message_list['messages'][0]
    # Check the message is not pinned since it was just created
    assert not message_content['is_pinned']

    # Get user 1 to pin the message
    message.message_pin(user1['token'], message_1_id)
    # Get the messages in the channel using channel_messages by user 1
    message_list = channel.channel_messages(user1['token'], channel_1_id, 0)
    message_content = message_list['messages'][0]
    # Check the message is now pinned
    assert message_content['is_pinned']

    # ********* Now check unpinning works **************
    # Get user 1 to unpin the message
    message.message_unpin(user1['token'], message_1_id)
    # Get the messages in the channel using channel_messages by user 1
    message_list = channel.channel_messages(user1['token'], channel_1_id, 0)
    message_content = message_list['messages'][0]
    # Check the message is now pinned
    assert not message_content['is_pinned']

def test_message_pin_unpin_input_error(make_two_users):
    '''
    Test for pin and unpin witn incorect inputs
    '''
    # message_id is not a valid message within a channel that the authorised user has joined
    # Get data for two users
    user1, user2 = make_two_users
    # Create a channel by user
    channel_1_name = 'test chan'
    channel_1_id = channels.channels_create(user1['token'], channel_1_name, True)['channel_id']
    channel.channel_join(user2['token'], channel_1_id)
    # Create 2 messages in channel
    message_1_id = message.message_send(user2['token'], channel_1_id, 'Hello World!')['message_id']
    message_2_id = message.message_send(user2['token'], channel_1_id, 'Hello World!')['message_id']
    # Pin message 1
    message.message_pin(user1['token'], message_1_id)
    # try pin again
    with pytest.raises(InputError):
        message.message_pin(user1['token'], message_1_id)
    # try get a member not an ower to pin message
    with pytest.raises(InputError):
        message.message_pin(user2['token'], message_1_id)
    # try pin an invalid message id
    with pytest.raises(InputError):
        message.message_pin(user1['token'], message_1_id + 21)

    # ***** Test unpin invalid inputs ************
    # Try unpin an unpinned message
    with pytest.raises(InputError):
        message.message_unpin(user1['token'], message_2_id)
    # try get a member not an ower to unpin message
    with pytest.raises(InputError):
        message.message_pin(user2['token'], message_1_id)
    # try pin an invalid message id
    with pytest.raises(InputError):
        message.message_unpin(user1['token'], message_1_id + 21)

# ********** Testing invalid tokens ***********************
def test_channel_access_error_invalid_token():
    '''
    Test all functions but with an invalid token
    Every token string will be invalid since no users are logged in
    Invalid inputs are given but based on assumptions the token is checked for
    validity first and throws the first error if invalid
    '''
    with pytest.raises(AccessError):
        message.message_send('faketoken', 1, 'a')
    with pytest.raises(AccessError):
        message.message_remove('faketoken', 1)
    with pytest.raises(AccessError):
        message.message_edit('faketoken', 1, 'a')
    with pytest.raises(AccessError):
        message.message_react('faketoken', 1, 1)
    with pytest.raises(AccessError):
        message.message_unreact('faketoken', 1, 1)
    with pytest.raises(AccessError):
        message.message_pin('faketoken', 1)
    with pytest.raises(AccessError):
        message.message_unpin('faketoken', 1)
    with pytest.raises(AccessError):
        message.message_sendlater('faketoken', 1, 'a', 2)
