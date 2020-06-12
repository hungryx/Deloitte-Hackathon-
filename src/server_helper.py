'''
Author: Nikola Medimurac
This file is used to contain all helper function used in the server
List of helper functions include:
    - is_input_correct(data_given, data_required):
'''

import threading
import pickle
from datetime import datetime, timezone
import os
import website_data as wd
import server_updater_thread as serv_up_thread
import message
import standup

def is_input_correct(data_given, data_required): # pylint: disable=too-many-branches, too-many-return-statements
    '''
    This is a helper function for the server
    It checks that the input passed to a function is correct
    Takes a list of strings of the fields required for the function called
    and the data given from the request
    This function is also linked to the data_types defined in website_data
    allowing it to be easily extensible for new data types (no changes needed
    to this function if new data types added)
    Returns True if input is correct, False if input is incorrect
    '''
    # First check the right number of inputs where given
    if len(data_given) != len(data_required):
        return False
    # Now check that all the keys required are present and of right type
    # Get the list of all the data_types possible to check against
    data_types = wd.get_data_types()
    # Loop through each data type required and check its a key in data given
    for data_name in data_required:
        # Since data types can be subset of the actual name, loop till we find the matching one
        # This breaks if 2 data types are different but are defined by the same string in the name
        # It will take the longest matching string in this case
        data_type_name = ''
        matching_letters = 0
        for data_type in data_types:
            if data_type in data_name:
                if len(data_type) > matching_letters:
                    matching_letters = len(data_type)
                    data_type_name = data_type
        # Check that the data name given was found to be an actual data type
        if data_type_name == '':
            return False
        # If the data name is not in data given or data types then return False
        if data_name not in data_given:
            return False
        # Check the data type is correct, if not return false
        #if type(data_given[data_name]) !=  type(data_types[data_type_name]):
        if not isinstance(data_given[data_name], type(data_types[data_type_name])):
            return False
        # Check if its a list, if so use recursion of this function to check through the list
        if isinstance(type(data_given[data_name]), list):
            for thing_in_input_list in data_given[data_name]:
                if not is_input_correct(thing_in_input_list, list(thing_in_input_list.keys())):
                    return False
        # Check if its a dictionary, if so use recursion to check entries in dictionary
        # Also check all the keys in the dictionary match up
        if isinstance(type(data_given[data_name]), dict):
            # Checking that dictionary keys match those in data_types
            if list(data_given[data_name].keys()) != list(data_types[data_type_name].keys()):
                return False
            # Check that the keys are defined correctly
            for key in list(data_given[data_name].keys()):
                if not is_input_correct(key, [key]):
                    return False
    # if we reach here then every entry has been checked and so return true
    return True

def load_stored_data():
    '''
    Function to load the stored data into the websites data
    This should be called everytime the website starts
    '''
    # load the data from a file called stored_website_data.pickle
    file_name = 'stored_website_data.pickle'
    # Need to check file exists and is not empty
    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
        with open('stored_website_data.pickle', 'rb') as file:
            data = pickle.load(file)
        # Save the data in the websites data memory
        wd.set_all_data(data)
    else:
        # If there no data to read then set workspace to be clear
        wd.clear_all_data()


def run_updater_thread():
    '''
    Function to setup the updater thread to run every second
    '''
    # Setup thread to run once a second
    timer = threading.Timer(1.0, run_updater_thread)
    timer.daemon = True
    timer.start()
    # Call the main looping function for the server thread
    serv_up_thread.main_updater_thread_loop()


def check_messages_to_send():
    '''
    Checks if any messages are in the waiting to send list and calls sendlater on them
    This is useful in case the server shuts off so send later messages arnt lost
    '''
    # Iterate through the send later data and pass the ids to check_message_waiting
    send_later_data = wd.get_data('send later')
    if len(send_later_data) == 0:
        return
    ids_to_send = []
    counter = 0
    for data in send_later_data:
        # Call check function to send message if passed time
        if not message.check_message_waiting(data['id']):
            # If the message is not ready to send yet then start a timer to send it when time
            ids_to_send.append(data['id'])
            time_now = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
            time_till_send = data['timestamp'] - time_now
            timer = threading.Timer(time_till_send,
                                    lambda: message.check_message_waiting(ids_to_send[counter]))
            timer.daemon = True
            timer.start()
            counter += 1

def check_standups_active():
    '''
    Checks if any standups are active and places a timer to close them when the time is done
    This is used in case the server goes off so that the timers to end standups are restored
    '''
    # Iterate through channel data and check if any standups are active
    all_channel_data = wd.get_data('channel data')
    if len(all_channel_data) == 0:
        return
    standup_ids = []
    counter = 0
    for data in all_channel_data:
        # Check if there is an active standup
        if data['standup time'] is None:
            # if no active stand up then move to next channel
            continue
        # If data indicates an active standup
        time_now = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
        if time_now <= data['standup time']:
            # if time now is after the stand up finish then call finish function
            standup.finish_standup(data['id'])
        else:
            # if standup is still in progress, set timer to end when time is done
            standup_ids.append(data['id'])
            time_till_send = data['standup time'] - time_now
            timer = threading.Timer(time_till_send,
                                    lambda: message.check_message_waiting(standup_ids[counter]))
            timer.daemon = True
            timer.start()
            counter += 1
