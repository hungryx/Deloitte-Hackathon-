# ************************************************
# File for testing functions related to standup
# Author: William Dieu
# Date Started: 27/3/2020
# ************************************************
# Functions tested in this file include:
# standup_start
# standup_active
# standup_send

'''
Tests for the implementation of standup
'''

import time
from datetime import datetime, timezone
import pytest
from auth import auth_register
from channels import channels_create
from channel import channel_invite, channel_messages
from standup import standup_start, standup_active, standup_send
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


def test_standup_start(register_user):
    '''
    Test starting a standup period
    '''
    # Get data for one user
    user1 = register_user
    # Create a public and private channel with user 1 in it
    channel_1_name = 'public ch'
    channel_2_name = 'private ch'
    channel_1_id = channels_create(user1['token'], channel_1_name, True)['channel_id']
    channel_2_id = channels_create(user1['token'], channel_2_name, False)['channel_id']

    # Initiate startup for 1 second
    standup_1 = standup_start(user1['token'], channel_1_id, 1)
    standup_2 = standup_start(user1['token'], channel_2_id, 1)

    # Check if the standup time finish matches length of duration for both private
    # and public channel
    current_time = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    assert standup_1['time_finish'] == 1 + current_time
    assert standup_2['time_finish'] == 1 + current_time
    time.sleep(1)

def test_standup_active(register_user):
    '''
    Test checking if a standup is active
    '''
    # Get data for one user
    user1 = register_user
    # Create a public and private channel with user 1 in it
    channel_1_name = 'public ch 1'
    channel_2_name = 'private ch 1'
    channel_3_name = 'public ch 2'
    channel_4_name = 'private ch 2'
    channel_1_id = channels_create(user1['token'], channel_1_name, True)['channel_id']
    channel_2_id = channels_create(user1['token'], channel_2_name, False)['channel_id']
    channel_3_id = channels_create(user1['token'], channel_3_name, True)['channel_id']
    channel_4_id = channels_create(user1['token'], channel_4_name, False)['channel_id']

    # Initiate standup for 1 second
    standup_start(user1['token'], channel_1_id, 1)
    standup_start(user1['token'], channel_2_id, 1)

    # Check if the standup is active and if the time finish matches length of
    # duration for both public and private channel
    standup_check_1 = standup_active(user1['token'], channel_1_id)
    standup_check_2 = standup_active(user1['token'], channel_2_id)
    assert standup_check_1['is_active']
    assert standup_check_2['is_active']
    current_time = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    assert standup_check_1['time_finish'] == 1 + current_time
    assert standup_check_2['time_finish'] == 1 + current_time
    # Check if the standup is inactive for channel 3 and 4
    standup_check_3 = standup_active(user1['token'], channel_3_id)
    standup_check_4 = standup_active(user1['token'], channel_4_id)
    assert standup_check_3 == {'is_active': False, 'time_finish': None}
    assert standup_check_4 == {'is_active': False, 'time_finish': None}
    time.sleep(1)

def test_standup_active_expired(register_user):
    '''
    Test checking if a standup is active in an invalid channel
    '''
    # Get data for one user
    user1 = register_user
    # Create a channel with user 1 in it
    channel_1_name = 'public ch 1'
    channel_2_name = 'private ch 1'
    channel_1_id = channels_create(user1['token'], channel_1_name, True)['channel_id']
    channel_2_id = channels_create(user1['token'], channel_2_name, False)['channel_id']

    # Initiate standup for 1 second
    standup_start(user1['token'], channel_1_id, 1)
    standup_start(user1['token'], channel_2_id, 1)
    time.sleep(2)

    # Check that the standup is inactive
    standup_check_1 = standup_active(user1['token'], channel_1_id)
    standup_check_2 = standup_active(user1['token'], channel_2_id)
    assert standup_check_1 == {'is_active': False, 'time_finish': None}
    assert standup_check_2 == {'is_active': False, 'time_finish': None}

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
    # Invite user 2 to both channels
    channel_invite(user1['token'], channel_1_id, user2['u_id'])
    channel_invite(user1['token'], channel_2_id, user2['u_id'])

    # Initiate standup for 1 second
    standup_start(user1['token'], channel_1_id, 1)
    standup_start(user1['token'], channel_2_id, 1)

    # Send messages to both public and private channel
    standup_send(user1['token'], channel_1_id, 'This')
    standup_send(user2['token'], channel_1_id, 'is')
    standup_send(user1['token'], channel_1_id, 'a')
    standup_send(user2['token'], channel_1_id, 'standup')
    check_1 = 'williamdieu: This\nwilliamyao: is\nwilliamdieu: a\nwilliamyao: standup'

    standup_send(user1['token'], channel_2_id, 'This')
    standup_send(user2['token'], channel_2_id, 'is')
    standup_send(user1['token'], channel_2_id, 'a')
    standup_send(user2['token'], channel_2_id, 'standoff')
    check_2 = 'williamdieu: This\nwilliamyao: is\nwilliamdieu: a\nwilliamyao: standoff'

    # Wait for standup to end and check if messages exist in channel_messages
    time.sleep(2)
    message_1 = channel_messages(user1['token'], channel_1_id, 0)['messages']
    message_2 = channel_messages(user1['token'], channel_2_id, 0)['messages']
    assert message_1[0]['u_id'] == user1['u_id']
    assert message_1[0]['message'] == check_1
    assert message_2[0]['u_id'] == user1['u_id']
    assert message_2[0]['message'] == check_2
