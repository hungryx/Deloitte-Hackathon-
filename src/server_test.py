'''
Author: Nikola Medimurac
Test file for testing the server
Uses urllib functions to test
The server has also been tested through using postman
'''

import json
import urllib
import flask #pylint: disable=unused-import

# Set BASE_URL depending on what you set port as
BASE_URL = 'http://127.0.0.1:8080'

# ***** Helper function for test *******
def send_data(data, route):
    '''
    Helper function for sending a dictionary to
    a route in a post request
    '''
    req = urllib.request.Request(f"{BASE_URL}" + route, data=data, method="POST")
    payload = json.load(urllib.request.urlopen(req))
    return payload


def test_system():
    '''
    This function will test the server functions under normal use
    '''
    # Test server responds to requests clear all the website data
    send_data({}, '/workspace/reset')
