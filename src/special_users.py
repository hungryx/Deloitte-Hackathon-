'''
Author: Nikola Medimurac
This file is for creating special users on the server
Currently the only special user is the hangman bot and deleted user
More bots or other special types of users can be added here
Special users are diciated by having an id above 100000
'''

import website_data as wd

def create_special_users(port):
    '''
    Function to add special users to website data
    Currently only adds hangman_bot
    '''
    url = 'http://localhost:' + str(port) + '/profile_imgs/'
    hangman_bot_data = {"id" : 100000,
                        "email" : "no email",
                        "name_first" : 'Hangman',
                        "name_last" : 'Bot',
                        "handle_str" : 'hangman_bot',
                        "profile_img_url" : url + 'hangman_bot' + '.jpg',
                        }
    deleted_user_data = {"id" : 100001,
                         "email" : "no email",
                         "name_first" : 'Deleted',
                         "name_last" : 'User',
                         "handle_str" : 'deleted_user',
                         "profile_img_url" : url + 'deleted_user' + '.jpg',
                        }
    special_user_list = [hangman_bot_data, deleted_user_data]
    wd.set_data('special users', special_user_list)
