'''
Author: Nikola Medimurac
This module contain ascii art used in the server
These are a set of functions that can be called and return a string made up of ascii art.
Currently only used for the hangman game to draw the different stages of the game but
future ascii arts should be included here as well
'''

def hangman(num_wrong):
    '''
    Takes in the number of wrong guesses made in a hangman game
    and returns the corresponding hangman drawing in ascii form
    as a string
    '''
    drawing = ' '
    if num_wrong == 1:
        drawing = "=========="
    elif num_wrong == 2:
        drawing = (" |      \n"
                   " |      \n"
                   " |      \n"
                   " |      \n"
                   "==========")
    elif num_wrong == 3:
        drawing = (" _____  \n"
                   " |      \n"
                   " |      \n"
                   " |      \n"
                   " |      \n"
                   "==========")
    elif num_wrong == 4:
        drawing = (" _____  \n"
                   " | . |   \n"
                   " |      \n"
                   " |      \n"
                   " |      \n"
                   "==========")
    elif num_wrong == 5:
        drawing = (" _____  \n"
                   " | . |  \n"
                   " | . O  \n"
                   " |      \n"
                   " |      \n"
                   "==========")
    elif num_wrong == 6:
        drawing = (" _____  \n"
                   " | . |  \n"
                   " | . O  \n"
                   " | . |  \n"
                   " |      \n"
                   "==========")
    elif num_wrong == 7:
        drawing = (" _____  \n"
                   " | . |  \n"
                   " | . O  \n"
                   " | . |  \n"
                   " | . .l \n"
                   "==========")
    elif num_wrong == 8:
        drawing = (" _____  \n"
                   " | . |  \n"
                   " | . O  \n"
                   " | . |  \n"
                   " | .l l \n"
                   "==========")
    elif num_wrong == 9:
        drawing = (" _____  \n"
                   " | . |  \n"
                   " | . O  \n"
                   " | . |--\n"
                   " | .l l \n"
                   "==========")
    elif num_wrong == 10:
        drawing = (" _____  \n"
                   " | . |  \n"
                   " | . O  \n"
                   " | --|--\n"
                   " | .l l \n"
                   "==========")
    return drawing
