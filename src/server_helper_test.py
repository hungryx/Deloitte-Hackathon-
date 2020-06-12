'''
Author: Nikola Medimurac
Tests for server helper functions
'''

import website_data as wd
import server_helper

def test_is_input_correct_normal():
    '''
    Test function for testing is_input_correct
    given all the possible data types correct
    This tests that it checks all the data types correctly
    '''
    # Define the dictionary that contains every possible type
    # from the specifications
    input_data = wd.get_data_types()
    data_required = list(input_data.keys())
    assert server_helper.is_input_correct(input_data, data_required)
