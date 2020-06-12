# ************************************************
# File for testing errors in functions related to standup
# Author: William Dieu
# Date Started: 27/3/2020
# ************************************************
# Functions tested in this file include:
# standup_start
# standup_active
# standup_send

'''
Error tests for the implementation of standup
'''

import time
import pytest
from auth import auth_register
from channels import channels_create
from standup import standup_start, standup_active, standup_send
from error import InputError, AccessError
import website_data as wd

# pylint: disable=redefined-outer-name

@pytest.fixture
def register_user():
    '''
    create fixture that resets the server state so that there is only 1 user
    '''
    wd.clear_all_data()
    return auth_register('william.dieu@unsw.edu.au', 'Qwerty123!', 'William', 'Dieu')

@pytest.fixture
def register_another_user():
    '''
    create fixture that creates another
    '''
    return auth_register('william.yao@unsw.edu.au', 'Qwerty123!', 'William', 'Yao')

def test_standup_invalid(register_user):
    '''
    Test starting a standup period with an invalid channel id
    '''
    # Get data for one user
    user1 = register_user
    # Create a public and private channel with user 1 in it
    channel_1_name = 'public ch'
    channels_create(user1['token'], channel_1_name, True)

    # Initiate startup
    invalid_id = 101
    with pytest.raises(InputError):
        standup_start(user1['token'], invalid_id, 1)

def test_standup_already_active(register_user):
    '''
    Test starting a standup period in a channel with a standup existing
    '''
    # Get data for one user
    user1 = register_user
    # Create a public and private channel with user 1 in it
    channel_1_name = 'public ch'
    channel_2_name = 'private ch'
    channel_1_id = channels_create(user1['token'], channel_1_name, True)['channel_id']
    channel_2_id = channels_create(user1['token'], channel_2_name, False)['channel_id']

    # Initiate startup for 1 second
    standup_start(user1['token'], channel_1_id, 1)
    standup_start(user1['token'], channel_2_id, 1)

    # Attempt to initiate startup while startup is active in channel
    with pytest.raises(InputError):
        standup_start(user1['token'], channel_1_id, 1)
    with pytest.raises(InputError):
        standup_start(user1['token'], channel_2_id, 1)

def test_standup_active_invalid(register_user):
    '''
    Test checking if a standup is active in an invalid channel
    '''
    # Get data for one user
    user1 = register_user
    # Create a channel with user 1 in it
    channel_1_name = 'public ch 1'
    channel_1_id = channels_create(user1['token'], channel_1_name, True)['channel_id']

    # Initiate standup for 1 second
    standup_start(user1['token'], channel_1_id, 1)

    # Attempt to check invalid channel if a standup is active
    invalid_id = 101
    with pytest.raises(InputError):
        standup_active(user1['token'], invalid_id)

def test_standup_send(register_user, register_another_user):
    '''
    Test checking sending messages in a standup
    '''
    # Get data for two users
    user1 = register_user
    user2 = register_another_user
    # Create a public and private channel with user 1 in it
    channel_1_name = 'public ch'
    channel_2_name = 'private ch'
    channel_1_id = channels_create(user1['token'], channel_1_name, True)['channel_id']
    channel_2_id = channels_create(user1['token'], channel_2_name, False)['channel_id']

    # Initiate standup for 1 second in public channel
    standup_start(user1['token'], channel_1_id, 1)
    invalid_id = 101
    # Send message in invalid channel
    with pytest.raises(InputError):
        standup_send(user1['token'], invalid_id, 'Hello')
    # send message with more than 1000 characters
    with pytest.raises(InputError):
        standup_send(user1['token'], channel_1_id, 'a' * 10001)
    # Send message in channel with inactive standup
    with pytest.raises(InputError):
        standup_send(user1['token'], channel_2_id, 'World')
    # Send valid message in valid channel but non authorised user
    with pytest.raises(AccessError):
        standup_send(user2['token'], channel_1_id, 'Hi!')
    time.sleep(1)

def test_standup_invalid_tokens(register_user):
    '''
    Test standup functions with invalid token
    '''
    # Get data for one user
    user1 = register_user
    # Create a channel with user 1 in it
    channel_1_name = 'public ch 1'
    channel_1_id = channels_create(user1['token'], channel_1_name, True)['channel_id']

    # Initiate standup for 1 second
    with pytest.raises(AccessError):
        standup_start('faketoken', channel_1_id, 1)
    with pytest.raises(AccessError):
        standup_active('faketoken', channel_1_id)
    with pytest.raises(AccessError):
        standup_send('faketoken', channel_1_id, 'Hello')
