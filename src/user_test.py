# ************************************************
# File for testing functions related to channel
# Author: William Dieu
# Date Started: 4/3/2020
# ************************************************
# Functions tested in this file include:
# user_profile
# user_profile_setname
# user_profile_setemail
# user_profile_sethandle

'''
Tests for the implementation of user
'''

import pytest
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle
from auth import auth_register
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

#==============================[user_profile]==================================#

def test_profile(register_user):
    '''
    Test obtaining profile of a user
    '''
    user1 = register_user
    profile = user_profile(user1['token'], user1['u_id'], 0)['user']
    # Check all details of user is identical to signing up details
    assert profile['email'] == 'william.dieu@unsw.edu.au'
    assert profile['name_first'] == 'William'
    assert profile['name_last'] == 'Dieu'
    assert profile['handle_str'] == 'williamdieu'

def test_profile_invalid(register_user):
    '''
    Test that requesting profile of a user with an invalid user_id results in
    an InputError
    '''
    user1 = register_user
    invalid_id = str(user1['u_id'])

    with pytest.raises(InputError):
        user_profile(user1['token'], invalid_id, 0)
    with pytest.raises(InputError):
        user_profile(user1['token'], '', 0)
    with pytest.raises(InputError):
        user_profile(user1['token'], None, 0)

#===========================[user_profile_setname]=============================#

def test_setname(register_user):
    '''
    Test changing name of a user
    '''
    user1 = register_user
    user_profile_setname(user1['token'], 'Will', 'Yao')
    profile = user_profile(user1['token'], user1['u_id'], 0)['user']
    # Check that the first and last name of the user has changed to that of the request
    assert profile['name_first'] == 'Will'
    assert profile['name_last'] == 'Yao'

def test_setname_too_short_or_long(register_user):
    '''
    Test that changing name that is >50 or < 1 results in an InputError
    '''
    user1 = register_user

    with pytest.raises(InputError):
        user_profile_setname(user1['token'], '', 'Dieu')
    with pytest.raises(InputError):
        user_profile_setname(user1['token'], 'W' * 51, 'Dieu')
    with pytest.raises(InputError):
        user_profile_setname(user1['token'], 'William', '')
    with pytest.raises(InputError):
        user_profile_setname(user1['token'], 'William', 'D' * 51)

def test_setname_invalid(register_user):
    '''
    Test that changing name to an invalid input results in an InputError
    '''
    user1 = register_user

    with pytest.raises(InputError):
        user_profile_setname(user1['token'], ' ', 'Dieu')
    with pytest.raises(InputError):
        user_profile_setname(user1['token'], 'William', ' ')
    with pytest.raises(InputError):
        user_profile_setname(user1['token'], None, 'Dieu')
    with pytest.raises(InputError):
        user_profile_setname(user1['token'], 'William', None)

#==========================[user_profile_setemail]=============================#

def test_setemail(register_user):
    '''
    Test changing email of a user
    '''
    user1 = register_user
    user_profile_setemail(user1['token'], 'will.dieu@unsw.edu.au')
    profile = user_profile(user1['token'], user1['u_id'], 0)['user']
    # check that the email of the user has changed to that of the request
    assert profile['email'] == 'will.dieu@unsw.edu.au'

def test_setemail_used(register_user, register_another_user):
    '''
    Test changing email to a used one results in an InputError
    Changing to own email will raise also error as it's redundant
    '''
    user1 = register_user
    _ = register_another_user

    with pytest.raises(InputError):
        user_profile_setemail(user1['token'], 'william.yao@unsw.edu.au')
    with pytest.raises(InputError):
        user_profile_setemail(user1['token'], 'william.dieu@unsw.edu.au')

def test_setemail_invalid(register_user):
    '''
    Test that changing email to an invalid input results in an InputError
    '''
    user1 = register_user

    with pytest.raises(InputError):
        user_profile_setemail(user1['token'], 'will.dieu.com')
    with pytest.raises(InputError):
        user_profile_setemail(user1['token'], None)
    with pytest.raises(InputError):
        user_profile_setemail(user1['token'], '')

#===========================[user_profile_sethandle]==============================#

def test_sethandle(register_user):
    '''
    Test changing handle of a user
    '''
    user1 = register_user
    user_profile_sethandle(user1['token'], 'willyd')
    profile = user_profile(user1['token'], user1['u_id'], 0)['user']
    # check that the handle of the user has changed to that of the request
    assert profile['handle_str'] == 'willyd'

def test_sethandle_too_short_or_long(register_user):
    '''
    Test that changing handle that is >20 or < 2 results in an InputError
    '''
    user1 = register_user

    with pytest.raises(InputError):
        user_profile_sethandle(user1['token'], 'w')
    with pytest.raises(InputError):
        user_profile_sethandle(user1['token'], 'w' * 21)

def test_sethandle_used(register_user, register_another_user):
    '''
    Test changing handle to a used one results in an InputError
    Changing to own handle will raise also error as it's redundant
    '''
    user1 = register_user
    _ = register_another_user

    with pytest.raises(InputError):
        user_profile_sethandle(user1['token'], 'williamyao')
    with pytest.raises(InputError):
        user_profile_sethandle(user1['token'], 'williamdieu')

def test_sethandle_invalid(register_user):
    '''
    Test that changing handle to an invalid input results in an InputError
    '''
    user1 = register_user

    with pytest.raises(InputError):
        user_profile_sethandle(user1['token'], None)
    with pytest.raises(InputError):
        user_profile_sethandle(user1['token'], '')

#===============================[invalid_token]================================#

def test_invalid_token(register_user):
    '''
    Test that using an invalid token results in an AccessError
    '''
    user1 = register_user
    invalid_token = 420

    with pytest.raises(AccessError):
        user_profile(invalid_token, user1['u_id'], 0)
    with pytest.raises(AccessError):
        user_profile_setname(invalid_token, 'Will', 'Yao')
    with pytest.raises(AccessError):
        user_profile_setemail(invalid_token, 'will.dieu@unsw.edu.au')
    with pytest.raises(AccessError):
        user_profile_sethandle(invalid_token, 'willyd')
