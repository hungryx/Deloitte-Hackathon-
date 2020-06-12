# *******************************************************
# File for testing errors in functions related to channel
# Author: Nikola Medimurac
# Date Started: 6/3/2020
# *******************************************************
# Functions tested in this file include:
# channel.channel_invite()
# channel.channel_details()
# channel.channel_messages()
# channel.channel_leave()
# channel.channel_join()
# channel.channel_addowner()
# channel.channel_removeowner()

'''
Error tests for the implementation of channel
'''

# pylint: disable=redefined-outer-name

import pytest
import auth
import channel
import channels
from error import InputError, AccessError
import website_data as wd


@pytest.fixture
def make_two_users():
    '''
    Create fixture that resets the server state so that there are only 2 users
    '''
    wd.clear_all_data()
    user1 = auth.auth_register('user1@gmail.com', 'thisismypassword', 'myfirstname', 'mylastname')
    user2 = auth.auth_register('myemail@gmail.com', '123idk', 'name', 'anothername')
    return (user1, user2)


# ************* Test Input Errors ***************
def test_channel_invalid_channel_id(make_two_users):
    '''
    Test all channel commands with invalid channel id
    '''
    # Get data for two users
    user1, user2 = make_two_users
    # make 1 channel by user1 and get user 2 to join it
    channel_1_name = 'test channel'
    channels.channels_create(user1['token'], channel_1_name, True)
    # Find a channel id that is not valid, there is only 1 channel that's valid
    # so make sure we don't pick that channel
    wrong_id = 100

    # Call all commands with a invalid channel id
    # Test invite
    with pytest.raises(InputError):
        channel.channel_invite(user1['token'], wrong_id, user2['u_id'])
    with pytest.raises(InputError):
        channel.channel_invite(user1['token'], 999999, user2['u_id'])
    # Test details
    with pytest.raises(InputError):
        channel.channel_details(user1['token'], wrong_id, 0)
    with pytest.raises(InputError):
        channel.channel_details(user1['token'], 999999, 0)
    # Test messages
    with pytest.raises(InputError):
        channel.channel_messages(user1['token'], wrong_id, 0)
    with pytest.raises(InputError):
        channel.channel_messages(user1['token'], 999999, 0)
    # Test leaving
    with pytest.raises(InputError):
        channel.channel_leave(user1['token'], wrong_id)
    with pytest.raises(InputError):
        channel.channel_leave(user1['token'], 999999)
    # Test joining
    with pytest.raises(InputError):
        channel.channel_join(user1['token'], wrong_id)
    with pytest.raises(InputError):
        channel.channel_join(user1['token'], 999999)
    # Test addowner
    with pytest.raises(InputError):
        channel.channel_addowner(user1['token'], wrong_id, user2['u_id'])
    with pytest.raises(InputError):
        channel.channel_addowner(user1['token'], 999999, user2['u_id'])
    # Test removeowner
    with pytest.raises(InputError):
        channel.channel_removeowner(user1['token'], wrong_id, user2['u_id'])
    with pytest.raises(InputError):
        channel.channel_removeowner(user1['token'], 999999, user2['u_id'])


def test_channel_invite_invalid(make_two_users):
    '''
    Test if invites raises InputError when adding an invalid user id or adding
    an already exister user
    '''
    # Get data for two users
    user1, user2 = make_two_users
    # make 1 channel by user1
    channel_1_name = 'test channel'
    channel_1_id = channels.channels_create(user1['token'], channel_1_name, True)['channel_id']
    # Find an id number that doesnt correspond to the two users made
    wrong_id = 420

    # Join/Invite an existing user
    channel.channel_join(user2['token'], channel_1_id)
    with pytest.raises(InputError):
        channel.channel_join(user2['token'], channel_1_id)
    with pytest.raises(InputError):
        channel.channel_invite(user1['token'], channel_1_id, user2['u_id'])

    # Invite possible different cases for invalid user id
    with pytest.raises(InputError):
        channel.channel_invite(user1['token'], channel_1_id, 'a')
    with pytest.raises(InputError):
        channel.channel_invite(user1['token'], channel_1_id, 999999)
    with pytest.raises(InputError):
        channel.channel_invite(user1['token'], channel_1_id, wrong_id)


def test_channel_messages_invalid_start(make_two_users):
    '''
    Test if messages raises InputError when starting at an invalid index
    '''
    # Get data for two users
    user1, _ = make_two_users
    # make 1 channel by user1
    channel_1_name = 'test channel'
    channel_1_id = channels.channels_create(user1['token'], channel_1_name, True)

    # Invite possible different cases for invalid user id
    with pytest.raises(InputError):
        channel.channel_messages(user1['token'], channel_1_id, 12)
    with pytest.raises(InputError):
        channel.channel_messages(user1['token'], channel_1_id, 11111)


def test_channel_remove_add_owner_invalid_users(make_two_users):
    '''
    Test adding and removing owners by and to invalid user ids
    '''
    # Get data for two users and make a third user
    user1, user2 = make_two_users
    user3 = auth.auth_register('user3@gmail.com', 'apassword', 'nameisfirst', 'nameislast')
    # make 1 channel by user1 and get user 2 and 3 to join it and give user 2 owner
    channel_1_name = 'test channel'
    channel_1_id = channels.channels_create(user1['token'], channel_1_name, True)['channel_id']
    channel.channel_join(user2['token'], channel_1_id)
    channel.channel_join(user3['token'], channel_1_id)
    channel.channel_addowner(user1['token'], channel_1_id, user2['u_id'])
    # Find a user id that does not exist
    wrong_id = 420

    # Try different possible comibnations of invalid user ids to raise InputErrors
    with pytest.raises(InputError):
        channel.channel_addowner(user2['token'], channel_1_id, user1['u_id'])
    with pytest.raises(InputError):
        channel.channel_addowner(user1['token'], channel_1_id, wrong_id)
    with pytest.raises(InputError):
        channel.channel_removeowner(user2['token'], channel_1_id, user3['u_id'])
    with pytest.raises(InputError):
        channel.channel_removeowner(user2['token'], channel_1_id, wrong_id)


# *********** Testing Access Errors **************
def test_channel_access_errors_permissions(make_two_users):
    '''
    Test access errors for all functions requiring access but setting up a user
    without permission
    '''
    # Get data for two users
    user1, user2 = make_two_users
    # make a third user for this test
    user3 = auth.auth_register('user3@gmail.com', 'apassword', 'nameisfirst', 'nameislast')
    channel_1_name = 'test chan 1'
    channel_1_id = channels.channels_create(user1['token'], channel_1_name, True)['channel_id']
    channel_2_name = 'test chan 2'
    channel_2_id = channels.channels_create(user2['token'], channel_2_name, False)['channel_id']
    # Get user 2 to join channel 1
    channel.channel_join(user2['token'], channel_1_id)

    # Try accessing all the functions without having permission to do it
    # Do this for both normal members and owner to check permission work correctly for both
    # Invite user in and not in channel by user who is not in channel
    with pytest.raises(AccessError):
        channel.channel_invite(user3['token'], channel_1_id, user1['u_id'])
    with pytest.raises(AccessError):
        channel.channel_invite(user1['token'], channel_2_id, user3['u_id'])
    # Call channel details on channel not in
    with pytest.raises(AccessError):
        channel.channel_details(user3['token'], channel_1_id, 0)
    # Create message for chat not in
    with pytest.raises(AccessError):
        channel.channel_messages(user3['token'], channel_1_id, 0)
    # Leave channel not part of
    with pytest.raises(AccessError):
        channel.channel_leave(user3['token'], channel_1_id)
    # Attempthing to join a private channel
    with pytest.raises(AccessError):
        channel.channel_join(user3['token'], channel_2_id)
    # Use add owner by member and non member of a channel
    with pytest.raises(AccessError):
        channel.channel_addowner(user2['token'], channel_1_id, user1['u_id'])
    with pytest.raises(AccessError):
        channel.channel_addowner(user2['token'], channel_1_id, user3['u_id'])
    with pytest.raises(AccessError):
        channel.channel_addowner(user3['token'], channel_1_id, user1['u_id'])
    # Use remove owner by member, non member and owner on owner of a channel
    with pytest.raises(AccessError):
        channel.channel_removeowner(user2['token'], channel_1_id, user1['u_id'])
    with pytest.raises(AccessError):
        channel.channel_removeowner(user3['token'], channel_1_id, user2['u_id'])
    with pytest.raises(AccessError):
        channel.channel_removeowner(user1['token'], channel_1_id, user1['u_id'])


def test_channel_access_error_invalid_token():
    '''
    Test access errors for all functions requiring access but setting up a user
    without permission
    '''
    # Try using all channels functions but passing an invalid token to it
    # Every token string will be invalid since no users are logged in
    # Invalid inputs are given but based on assumptions the token is checked
    # for validity first and throws the first error if invalid
    with pytest.raises(AccessError):
        channel.channel_invite('faketoken', 1, 1)
    with pytest.raises(AccessError):
        channel.channel_details('faketoken', 1, 0)
    with pytest.raises(AccessError):
        channel.channel_messages('faketoken', 1, 0)
    with pytest.raises(AccessError):
        channel.channel_leave('faketoken', 1)
    with pytest.raises(AccessError):
        channel.channel_join('faketoken', 1)
    with pytest.raises(AccessError):
        channel.channel_addowner('faketoken', 1, 1)
    with pytest.raises(AccessError):
        channel.channel_removeowner('faketoken', 1, 1)
