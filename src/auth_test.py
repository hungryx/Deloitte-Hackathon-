# ************************************************
# File for testing functions related to auth
# Author: Sam
# Date Started: 3/3/2020
# ************************************************
# Functions tested in this file include:
# auth_register()
# auth_login()
# auth_logout()

'''
Tests for the implementation of auth
'''

import pytest
from auth import auth_register, auth_login, auth_logout,\
                 auth_passwordreset_request, auth_passwordreset_reset
from error import InputError
import website_data as wd

def test_register():
    '''
    Testing valid new registers
    '''
    wd.clear_all_data()
    results1 = auth_register("bigpythonenergy@gmail.com", "Apple1", "Big", "Energy")
    assert isinstance(results1['u_id'], int)
    assert isinstance(results1['token'], str)
    results2 = auth_register("matt.damon@gmail.com.au", "Orange1", "Matt", "Damon")
    assert isinstance(results2['u_id'], int)
    assert isinstance(results2['token'], str)
    results3 = auth_register("will.smith@gmail.co.uk", "Grapes1", "William", "Smithington")
    assert isinstance(results3['u_id'], int)
    assert isinstance(results3['token'], str)
    results4 = auth_register("will.smith@gmail.co.us", "Grapes1", "William", "Smithington")
    assert isinstance(results4['u_id'], int)
    assert isinstance(results4['token'], str)
def test_register_email():
    '''
    Testing if invalid email registers raise an InputError
    '''
    wd.clear_all_data()
    with pytest.raises(InputError):
        auth_register("hummus", "Apple1", "Big", "Energy")
    with pytest.raises(InputError):
        auth_register("hummus@", "Apple1", "Big", "Energy")
    with pytest.raises(InputError):
        auth_register("hummus@gmail", "Apple1", "Big", "Energy")
    with pytest.raises(InputError):
        auth_register("hummus.com", "Apple1", "Big", "Energy")
    with pytest.raises(InputError):
        auth_register("hummus@.com", "Apple1", "Big", "Energy")
    with pytest.raises(InputError):
        auth_register("@hummus", "Apple1", "Big", "Energy")
    with pytest.raises(InputError):
        auth_register(".hummus", "Apple1", "Big", "Energy")
    with pytest.raises(InputError):
        auth_register("hummus.", "Apple1", "Big", "Energy")
    with pytest.raises(InputError):
        auth_register("@.hummus", "Apple1", "Big", "Energy")
    with pytest.raises(InputError):
        auth_register("@hummus.com", "Apple1", "Big", "Energy")
    with pytest.raises(InputError):
        auth_register("@hummus", "Apple1", "Big", "Energy")

def test_register_double():
    '''
    Registering valid new users and testing if reregistering raises an InputError
    '''
    wd.clear_all_data()
    auth_register("bigpythonenergy@gmail.com", "Apple1", "Big", "Energy")
    with pytest.raises(InputError):
        auth_register("bigpythonenergy@gmail.com", "Apple1", "Big", "Energy")
    with pytest.raises(InputError):
        auth_register("bigpythonenergy@gmail.com", "Apple1", "Bob", "Edwards")
    with pytest.raises(InputError):
        auth_register("bigpythonenergy@gmail.com", "Canteloupe1", "Matt", "Damon")

    auth_register("matt.damon@gmail.com.au", "Orange1", "Matt", "Damon")
    with pytest.raises(InputError):
        auth_register("matt.damon@gmail.com.au", "Orange1", "Matt", "Damon")
    with pytest.raises(InputError):
        auth_register("matt.damon@gmail.com.au", "Apple1", "Bob", "Edwards")
    with pytest.raises(InputError):
        auth_register("matt.damon@gmail.com.au", "Apple1", "Big", "Energy")

    auth_register("will.smith@gmail.co.uk", "Grapes1", "William", "Smithington")
    with pytest.raises(InputError):
        auth_register("will.smith@gmail.co.uk", "Orange1", "Matt", "Damon")
    with pytest.raises(InputError):
        auth_register("will.smith@gmail.co.uk", "Apple1", "Bob", "Edwards")
    with pytest.raises(InputError):
        auth_register("will.smith@gmail.co.uk", "Canteloupe1", "Matt", "Damon")

def test_register_password():
    '''
    Testing if invalid password registers raise an InputError
    '''
    wd.clear_all_data()
    with pytest.raises(InputError):
        auth_register("bigpythonenergy@gmail.com", "Ant1", "Big", "Energy")
    with pytest.raises(InputError):
        auth_register("bob.edwards@gmail.com", "Ant", "Bob", "Edwards")
    with pytest.raises(InputError):
        auth_register("matt.damon@gmail.com", "ant", "Matt", "Damon")
    with pytest.raises(InputError):
        auth_register("bigpythonenergy@gmail.com", "ant1", "Big", "Energy")
    with pytest.raises(InputError):
        auth_register("bob.edwards@gmail.com", "a", "Bob", "Edwards")
    with pytest.raises(InputError):
        auth_register("matt.damon@gmail.com", "A", "Matt", "Damon")
    with pytest.raises(InputError):
        auth_register("bigpythonenergy@gmail.com", "0", "Big", "Energy")
    with pytest.raises(InputError):
        auth_register("bob.edwards@gmail.com", "8253", "Bob", "Edwards")
    with pytest.raises(InputError):
        auth_register("matt.damon@gmail.com", "     ", "Matt", "Damon")

def test_register_firstname():
    '''
    Testing if invalid first name registers raise an InputError
    '''
    wd.clear_all_data()
    with pytest.raises(InputError):
        auth_register("bigpythonenergy@gmail.com", "Apple1", "", "Energy")
    with pytest.raises(InputError):
        auth_register("bigpythonenergy@gmail.com", "Apple1", "a" * 51, "Energy")
    with pytest.raises(InputError):
        auth_register("matt.damon@gmail.com.au", "Orange1", "", "Damon")
    with pytest.raises(InputError):
        auth_register("matt.damon@gmail.com.au", "Orange1", "F" * 100, "Damon")
    with pytest.raises(InputError):
        auth_register("will.smith@gmail.co.uk", "Grapes1", "", "Smithington")
    with pytest.raises(InputError):
        auth_register("will.smith@gmail.co.uk", "Grapes1", "1" * 150, "Smithington")

def test_register_lastname():
    '''
    Testing if invalid last name registers raise an InputError
    '''
    wd.clear_all_data()
    with pytest.raises(InputError):
        auth_register("bigpythonenergy@gmail.com", "Apple1", "Big", "")
    with pytest.raises(InputError):
        auth_register("bigpythonenergy@gmail.com", "Apple1", "Big", "a" * 51)
    with pytest.raises(InputError):
        auth_register("matt.damon@gmail.com.au", "Orange1", "Matt", "")
    with pytest.raises(InputError):
        auth_register("matt.damon@gmail.com.au", "Orange1", "Matt", "F" * 100)
    with pytest.raises(InputError):
        auth_register("will.smith@gmail.co.uk", "Grapes1", "William", "")
    with pytest.raises(InputError):
        auth_register("will.smith@gmail.co.uk", "Grapes1", "William", "1" * 150)

def test_login():
    '''
    Testing the login function on new users
    '''
    wd.clear_all_data()
    register1 = auth_register("bigpythonenergy@gmail.com", "Apple1", "Big", "Energy")
    login1 = auth_login("bigpythonenergy@gmail.com", "Apple1")
    assert register1['u_id'] == login1['u_id']
    assert register1['token'] == login1['token']
    register2 = auth_register("matt.damon@gmail.com.au", "Orange1", "Matt", "Damon")
    login2 = auth_login("matt.damon@gmail.com.au", "Orange1")
    assert register2['u_id'] == login2['u_id']
    assert register2['token'] == login2['token']
    register3 = auth_register("will.smith@gmail.co.uk", "Grapes1", "William", "Smithington")
    login3 = auth_login("will.smith@gmail.co.uk", "Grapes1")
    assert register3['u_id'] == login3['u_id']
    assert register3['token'] == login3['token']

def test_login_invalid_email():
    '''
    Testing if using an invalid email on login raises an InputError
    '''
    wd.clear_all_data()
    auth_register("bigpythonenergy@gmail.com", "Apple1", "Big", "Energy")
    auth_register("matt.damon@gmail.com.au", "Orange1", "Matt", "Damon")
    auth_register("will.smith@gmail.co.uk", "Grapes1", "William", "Smithington")
    with pytest.raises(InputError):
        auth_login("hummus", "Apple1")
    with pytest.raises(InputError):
        auth_login("hummus@", "Apple1")
    with pytest.raises(InputError):
        auth_login("@hummus", "Apple1")
    with pytest.raises(InputError):
        auth_login("hummus.com", "Apple1")
    with pytest.raises(InputError):
        auth_login(".hummus", "Orange1")
    with pytest.raises(InputError):
        auth_login("hummus.@", "Orange1")
    with pytest.raises(InputError):
        auth_login("@.hummus", "Orange1")
    with pytest.raises(InputError):
        auth_login("@", "Grapes1")
    with pytest.raises(InputError):
        auth_login(".", "Grapes1")

def test_login_unused_email():
    '''
    Testing if using an unused email on login raises an InputError
    '''
    wd.clear_all_data()
    auth_register("bigpythonenergy@gmail.com", "Apple1", "Big", "Energy")
    auth_register("matt.damon@gmail.com.au", "Orange1", "Matt", "Damon")
    auth_register("will.smith@gmail.co.uk", "Grapes1", "William", "Smithington")
    with pytest.raises(InputError):
        auth_login("hummus@gmail.com", "Apple1")
    with pytest.raises(InputError):
        auth_login("hummus@yahoo.com", "Apple1")
    with pytest.raises(InputError):
        auth_login("garlicbread@hotmail.com", "Apple1")
    with pytest.raises(InputError):
        auth_login("cheese@outlook.com.au", "Orange1")
    with pytest.raises(InputError):
        auth_login("mudcake@live.com.au", "Orange1")
    with pytest.raises(InputError):
        auth_login("aldi@optusnet.com.au", "Orange1")
    with pytest.raises(InputError):
        auth_login("pytestprodigy@gmail.co.uk", "Grapes1")
    with pytest.raises(InputError):
        auth_login("litfam@live.co.uk", "Grapes1")
    with pytest.raises(InputError):
        auth_login("squadgoalz@outlook.co.uk", "Grapes1")

def test_login_password():
    '''
    Testing if using an invalid password on login raises an InputError
    '''
    wd.clear_all_data()
    auth_register("bigpythonenergy@gmail.com", "Apple1", "Big", "Energy")
    auth_register("matt.damon@gmail.com.au", "Orange1", "Matt", "Damon")
    auth_register("will.smith@gmail.co.uk", "Grapes1", "William", "Smithington")
    with pytest.raises(InputError):
        auth_login("bigpythonenergy@gmail.com", "PearJuice1")
    with pytest.raises(InputError):
        auth_login("matt.damon@gmail.com.au", "Canteloupe1")
    with pytest.raises(InputError):
        auth_login("will.smith@gmail.co.uk", "Cherries1")
    with pytest.raises(InputError):
        auth_login("bigpythonenergy@gmail.com", "ohmygod")
    with pytest.raises(InputError):
        auth_login("matt.damon@gmail.com.au", "pytestprodigy")
    with pytest.raises(InputError):
        auth_login("will.smith@gmail.co.uk", "garlicbread")
    with pytest.raises(InputError):
        auth_login("bigpythonenergy@gmail.com", "4324324")
    with pytest.raises(InputError):
        auth_login("matt.damon@gmail.com.au", "         ")
    with pytest.raises(InputError):
        auth_login("will.smith@gmail.co.uk", "00000000")

def test_logout():
    '''
    Testing the logout function on logged in users
    '''
    wd.clear_all_data()
    result1 = auth_register("bigpythonenergy@gmail.com", "Apple1", "Big", "Energy")
    result2 = auth_register("matt.damon@gmail.com.au", "Orange1", "Matt", "Damon")
    result3 = auth_register("will.smith@gmail.co.uk", "Grapes1", "William", "Smithington")
    assert auth_logout(result1['token'])
    assert auth_logout(result2['token'])
    assert auth_logout(result3['token'])

def test_logout_invalid():
    '''
    Testing the logout function on already logged out users
    '''
    wd.clear_all_data()
    result1 = auth_register("bigpythonenergy@gmail.com", "Apple1", "Big", "Energy")
    result2 = auth_register("matt.damon@gmail.com.au", "Orange1", "Matt", "Damon")
    result3 = auth_register("will.smith@gmail.co.uk", "Grapes1", "William", "Smithington")
    auth_logout(result1['token'])
    auth_logout(result2['token'])
    auth_logout(result3['token'])
    assert not auth_logout(result1['token'])['is_success']
    assert not auth_logout(result2['token'])['is_success']
    assert not auth_logout(result3['token'])['is_success']

def test_passwordreset():
    '''
    Testing the password reset function on a user
    '''
    wd.clear_all_data()
    email = "williamdieu8@gmail.com"
    result = auth_register(email, "HelloWorld123", "William", "Dieu")
    auth_logout(result['token'])
    auth_passwordreset_request(email)
    auth_passwordreset_reset(
        "cb7e554d2a0fc3ac6ef9c433c769f8a5ab923fb35f0161f5f43a40d603d7491b",
        "GoodbyeWorld123"
    )
    auth_login(email, "GoodbyeWorld123")
    with pytest.raises(InputError):
        auth_login(email, "HelloWorld123")
    with pytest.raises(InputError):
        auth_passwordreset_reset(
            "cb7e554d2a0fc3ac6ef9c433c769f8a5ab923fb35f0161f5f43a40d603d7491b",
            "Thiswillfail123"
        )
