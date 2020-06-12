# ************************************************
# File for testing functions related to messaging
# Author: Nikola Medimurac
# Date Started: 9/3/2020
# ************************************************
# Functions tested in this file include:
# search()

'''
Tests for the implementation of other
'''

import pytest
import auth
import channel
import channels
import other
import message
from error import AccessError
import website_data as wd

# pylint: disable=redefined-outer-name,pointless-string-statement

@pytest.fixture
def make_two_users():
    '''
    create fixture that resets the server state so that there are only 2 users
    '''
    wd.clear_all_data()
    user1 = auth.auth_register('user1@gmail.com', 'thisismypassword', 'myfirstname', 'mylastname')
    user2 = auth.auth_register('myemail@gmail.com', '123idk', 'name', 'anothername')
    return (user1, user2)


def test_search(make_two_users):
    '''
    Test function for testing search under several different cases in the same slack setup
    '''
    # Get data for two users
    user1, user2 = make_two_users
    # Create 2 channels, add user 1 to both and user 2 to channel 1 only
    channel_1_name = 'thisisnum1'
    channel_2_name = 'anotherome'
    channel_1_id = channels.channels_create(user1['token'], channel_1_name, True)['channel_id']
    channel_2_id = channels.channels_create(user1['token'], channel_2_name, True)['channel_id']
    channel.channel_join(user2['token'], channel_1_id)

    # Add messages to both channels, hold the timestamps for every message sent
    # and a list of every messages id
    '''
    message_ids = [message.message_send(user1['token'], channel_1_id, 'a'),
                   message.message_send(user2['token'], channel_1_id, 'b'),
                   message.message_send(user1['token'], channel_1_id, 'c'),
                   message.message_send(user1['token'], channel_2_id, 'a'),
                   message.message_send(user2['token'], channel_1_id, 'a'),
                   message.message_send(user1['token'], channel_2_id, 'ab')]
    '''
    message_ids = []
    # Create the messages and put a delay between them, to check the timestamps are ordered correct
    message_ids.append(message.message_send(user1['token'], channel_1_id, 'a')['message_id'])
    message_ids.append(message.message_send(user2['token'], channel_1_id, 'b')['message_id'])
    message_ids.append(message.message_send(user1['token'], channel_1_id, 'c')['message_id'])
    message_ids.append(message.message_send(user1['token'], channel_2_id, 'a')['message_id'])
    message_ids.append(message.message_send(user2['token'], channel_1_id, 'a')['message_id'])
    message_ids.append(message.message_send(user1['token'], channel_2_id, 'ab')['message_id'])
    message_ids.append(message.message_send(
        user1['token'],
        channel_1_id,
        'lets try alot of words'
    )['message_id'])
    message_ids.append(message.message_send(
        user1['token'],
        channel_1_id,
        'lets try some words'
    )['message_id'])

    # Now that the messages have been sent check that search give correct output
    search_a1 = other.search(user1['token'], 'a')
    search_a2 = other.search(user2['token'], 'a')
    search_ab1 = other.search(user1['token'], 'ab')
    search_ab2 = other.search(user2['token'], 'ab')
    search_words = other.search(user1['token'], 'lets try alot')
    # Check that each message appears in the search return,
    # Only checking that message_id matches to verify the correct message dictionaries are returned
    # Checking the first search query of 'a' by user 1
    assert search_a1['messages'][0]['message_id'] == message_ids[4]
    assert search_a1['messages'][1]['message_id'] == message_ids[3]
    assert search_a1['messages'][2]['message_id'] == message_ids[0]
    #assert any(message['message_id'] == message_ids[0] for message in search_a1)
    #assert any(message['message_id'] == message_ids[3] for message in search_a1)
    #assert any(message['message_id'] == message_ids[4] for message in search_a1)

    # Checking the second search query of 'a' by user 2
    assert search_a2['messages'][0]['message_id'] == message_ids[4]
    assert search_a2['messages'][1]['message_id'] == message_ids[0]
    #assert any(message['message_id'] == message_ids[3] for message in search_a2)
    # Checking the third search query of 'ab' by user 1
    assert search_ab1['messages'][0]['message_id'] == message_ids[5]
    assert len(search_ab1['messages']) == 1
    #assert any(message['message_id'] == message_ids[5] for message in search_ab1)
    # Checking the fourth search query of 'ab' by user 1
    assert search_ab2['messages'] == []
    # Check the query with multiple words
    assert search_words['messages'][0]['message_id'] == message_ids[6]
    assert len(search_words['messages']) == 1


def test_users_all_multiple_users(make_two_users):
    '''
    Test users all for multiple users
    Only testing this normal case because it cannot be called when there are no
    valid users due to no valid tokens
    '''
    # Get data for two users
    user1, _ = make_two_users
    # Create the user data structures that represent the users datas
    user1_data = {'u_id' : 0,
                  'email' : 'user1@gmail.com',
                  'name_first' : 'myfirstname',
                  'name_last' : 'mylastname',
                  'handle_str' : 'myfirstnamemylastnam'
                 }
    user2_data = {'u_id' : 1,
                  'email' : 'myemail@gmail.com',
                  'name_first' : 'name',
                  'name_last' : 'anothername',
                  'handle_str' : 'nameanothername'
                 }

    # Get list of users
    user_list = other.users_all(user1['token'])
    # Check both users are in the list and only they exist in the list
    user_list_data = user_list['users']
    assert len(user_list_data) == 2
    assert any(user == user1_data for user in user_list_data)
    assert any(user == user2_data for user in user_list_data)


def test_other_invalid_token():
    '''
    Test using the other function with an invalid input
    If we create no users then every token will be invalid
    '''
    # try with invalid token
    with pytest.raises(AccessError):
        other.search('fakeToken', 'a')
    with pytest.raises(AccessError):
        other.users_all('fakeToken')
    # Try use a token as a number
    with pytest.raises(AccessError):
        other.search(420, 'a')
    with pytest.raises(AccessError):
        other.users_all(420)
