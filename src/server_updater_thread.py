'''
Author: Nikola Medimurac
This is a thread that runs in the background of the server
This thread continually loops every second and checks for updates the server should do
This thread is designed to easily add more tasks to it
The tasks this thread performs include:
    - Saving the data to a file so that it is persistent
    - Checking messages in send later queue and seeing if they should be sent
    - Checking for active standups that have finished
'''

import pickle
import website_data as wd

# ********** Functions Called in Thread *************
def save_data():
    '''
    This function gets the current data in the server
    and saves it to a file using pickle. This allow for
    persistent data storage
    This functions has no inputs of outputs
    '''
    # Get the website_data
    data = wd.get_all_data()
    # Save the data to a file called stored_website_data.pickle
    with open('stored_website_data.pickle', 'wb') as file:
        pickle.dump(data, file)


# ********** Main Function for Thread ****************
def main_updater_thread_loop():
    '''
    This is the main function that is looped in the
    server updater thread
    This has no inputs or outputs
    '''
    save_data()
