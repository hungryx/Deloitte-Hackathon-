# ************************************************
# File for testing functions related to channel
# Author: Nikola Medimurac
# Date Started: 3/3/2020
# ************************************************
# Functions tested in this file include:
# channels.channels_list()
# channels.channels.channels_listall()
# channels.channels_create()

'''
Tests for the implementation of channels
'''

import pytest
import auth
import channels
import channel
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


def test_channel_creation_normal(make_two_users):
    '''
    Test functions for creating a channel
    Checks if it returns an integer (channel_id) as requried
    '''
    # Get data for two users
    user1, user2 = make_two_users
    # Create public and private channel and check if they return an int between 0 and 65535
    channel_1_id = channels.channels_create(user1['token'], 'public channel', True)['channel_id']
    channel_2_id = channels.channels_create(user1['token'], 'private channel', False)['channel_id']
    assert isinstance(channel_1_id, int)
    assert channel_1_id >= 0
    assert channel_1_id <= 65535
    assert isinstance(channel_2_id, int)
    assert channel_2_id >= 0
    assert channel_2_id <= 65535

    # Also check a user can create a channel with the same name twice but different id

    assert channels.channels_create(user1['token'], 'public channel', True) != \
    channels.channels_create(user1['token'], 'public channel', True)
    assert channels.channels_create(user1['token'], 'private channel', False) != \
    channels.channels_create(user1['token'], 'private channel', False)

    # Check that creating a channel on two different users does not produce the same result
    assert channels.channels_create(user2['token'], 'public channel', True) != \
    channels.channels_create(user1['token'], 'public channel', True)
    assert channels.channels_create(user2['token'], 'private channel', False) != \
    channels.channels_create(user1['token'], 'private channel', False)


def test_channel_lists(make_two_users):
    '''
    Test channel listing functions channels.channels_list() and
    channels.channels_listall() for correct output
    '''
    user1, user2 = make_two_users
    # Create three channels, user 1 is in channel 1 and 3, user 2 is in channel 2
    channel_1_name = 'thisisnum1'
    channel_2_name = 'anotherone'
    channel_3_name = 'privateChan'
    channel_1_id = channels.channels_create(user1['token'], channel_1_name, True)['channel_id']
    channel_2_id = channels.channels_create(user2['token'], channel_2_name, True)['channel_id']
    channel_3_id = channels.channels_create(user1['token'], channel_3_name, False)['channel_id']

    # Check that user 1 and user 2 see the correct listing of channels using
    # channels.channels_list()
    assert (channels.channels_list(user1['token'])['channels']) == ([
        {'channel_id': channel_1_id, 'name': channel_1_name},
        {'channel_id': channel_3_id, 'name': channel_3_name}
    ])
    assert (channels.channels_list(user2['token'])['channels']) == [{
        'channel_id': channel_2_id, 'name': channel_2_name
    }]
    # Check that user 1 and user 2 see the correct listing of channels using
    # channels.channels.channels_listall()
    assert (channels.channels_listall(user1['token'])['channels']) == ([
        {'channel_id': channel_1_id, 'name': channel_1_name},
        {'channel_id': channel_2_id, 'name': channel_2_name},
        {'channel_id': channel_3_id, 'name': channel_3_name}
    ])
    assert (channels.channels_listall(user2['token'])['channels']) == ([
        {'channel_id': channel_1_id, 'name': channel_1_name},
        {'channel_id': channel_2_id, 'name': channel_2_name},
        {'channel_id': channel_3_id, 'name': channel_3_name}
    ])

    # Make user 2 leave a channel and user 1 join a channel to test effect of
    # joining, leaving, having no channels and being in all channels
    channel.channel_join(user1['token'], channel_2_id)
    channel.channel_leave(user2['token'], channel_2_id)
    # Check that user 1 and user 2 see the correct listing of channels using
    # channels.channels_list()
    assert (channels.channels_list(user1['token'])['channels']) == ([
        {'channel_id': channel_1_id, 'name': channel_1_name},
        {'channel_id': channel_2_id, 'name': channel_2_name},
        {'channel_id': channel_3_id, 'name': channel_3_name}
    ])
    assert (channels.channels_list(user2['token'])['channels']) == []
    # Check that user 1 and user 2 see the correct listing of channels using
    # channels.channels.channels_listall()
    assert (channels.channels_listall(user1['token'])['channels']) == ([
        {'channel_id': channel_1_id, 'name': channel_1_name},
        {'channel_id': channel_2_id, 'name': channel_2_name},
        {'channel_id': channel_3_id, 'name': channel_3_name}
    ])
    assert (channels.channels_listall(user2['token'])['channels']) == ([
        {'channel_id': channel_1_id, 'name': channel_1_name},
        {'channel_id': channel_2_id, 'name': channel_2_name},
        {'channel_id': channel_3_id, 'name': channel_3_name}
    ])
