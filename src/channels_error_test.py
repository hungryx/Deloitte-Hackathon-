# ************************************************
# File for testing functions related to channel
# Author: Nikola Medimurac
# Date Started: 8/3/2020
# ************************************************
# Functions tested in this file include:
# channels.channels_list()
# channels.channels.channels_listall()
# channels.channels_create()

'''
Error tests for the implementation of channels
'''

import pytest
import auth
import channels
from error import InputError, AccessError
import website_data as wd

# pylint: disable=redefined-outer-name

@pytest.fixture
def make_one_user():
    '''
    create fixture for creating 1 user
    '''
    wd.clear_all_data()
    user = auth.auth_register('user1@gmail.com', 'thisismypassword', 'myfirstname', 'mylastname')
    return user


def test_channel_creation_too_long(make_one_user):
    '''
    Check if channels.channels_create raises appropriate error when input is too long
    This is the only type of invalid input
    '''
    # Get data for one user
    user = make_one_user
    # Try to create channel with too long name and check if exception is raised
    # Check with exactly 21 letters
    with pytest.raises(InputError):
        # Check with exactly 21 letters
        channels.channels_create(user['token'], 'a' * 21, True)
    # Check with a really big number
    with pytest.raises(InputError):
        channels.channels_create(user['token'], 'a' * 1000, True)


def test_channels_access_error_invalid_token():
    '''
    Test access errors for all functions requiring access but setting up a user
    without permission
    '''
    # Try using all channels functions but passing an invalid token to it
    # Every token string will be invalid since no users are registered
    with pytest.raises(AccessError):
        channels.channels_create('fakeToken', 'name', True)
    with pytest.raises(AccessError):
        channels.channels_listall('fakeToken')
    with pytest.raises(AccessError):
        channels.channels_list('fakeToken')
