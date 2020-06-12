'''
Author: Nikola Medimurac
This module contains all the different type of message commands that can be used
A message command is a message that had the form /<command> <args>
This has been done in this way to easily allow future commands to be added
as well as reducing the liklihood of breaking existing code by adding new commands
Current commands include:
    - hangman
    - guess
'''

import wikiquote
import website_data as wd
import ascii_art
import message_helper as mes_help
from error import InputError

def message_command_caller(message, channel_id):
    '''
    Calling this function will take the message and call the corresponding
    function as well as pass the arguements to it
    This is done so if new commands are added the message function does not need any changes
    and this only needs to be modified slighlty in an easy way
    This function takes in the message and returns True if command was called, else returns False
    '''
    # Get the data for the channel the game is beeing called in
    wd.get_data_with_id('channel data', channel_id)
    # First check that the message begins with /
    if message[0] != '/':
        return False
    message_parts = message.split(" ", 1)
    command = message_parts[0][1:]
    if len(message_parts) > 1:
        args = message.split(" ", 1)[1]
    else:
        args = ""
    # Now try call the corresponding function and raise the error if one occurs
    try:
        # Call hangman command
        if command == 'hangman':
            message_command_hangman(channel_id)
            return True
        # Call guess command
        if command == 'guess':
            message_command_guess(args, channel_id)
            return True
    except Exception as err:
        raise err
    return False


def message_command_hangman(channel_id):
    '''
    Function for beginning a game of hangman
    This involves generating a random phrase, updating memory to reflect the
    game state and posting a message by the hangman bot
    This takes in no arguements and returns nothing
    '''
    # Get the data for the channel
    channel_data = wd.get_data_with_id('channel data', channel_id)
    # Check if there is already an active game. this would mean the word is not None
    if channel_data['hangman word'] is not None:
        raise InputError(description="Hangman game already active")
    # Get a quote for the game from wikiquote and make lettes capitals
    word = wikiquote.random_titles(max_titles=1)[0].upper()
    # if the word only contains numbers then find another word
    while word.isnumeric():
        word = wikiquote.random_titles(max_titles=1)[0].upper()
    # Setup memory to initialise the game
    channel_data['hangman guesses'] = []
    channel_data['hangman word'] = word
    # Update memory to reflect new game state
    wd.set_data_with_id('channel data', channel_id, channel_data)
    # Build the mesaage indicating the game has started
    starting_message = 'Welcome to hangman!\n\n'
    for char in word:
        if char.isalpha():
            starting_message += '_ '
        elif char == ' ':
            starting_message += '   '
        else:
            starting_message += char
    # Print the message indicating the start of the game
    mes_help.create_message_special_user(100000, channel_id, starting_message)

def message_command_guess(guess, channel_id): #pylint: disable=too-many-branches
    '''
    Function to make guesses during a game of hangman
    This will update the game state and trigger the hangman bot
    to post a message to refelct the game state change
    This function takes in the guess and returns nothing
    '''
    # Get the data for the channel
    channel_data = wd.get_data_with_id('channel data', channel_id)
    # Check if there is not an active game. this would mean the word is None
    if channel_data['hangman word'] is None:
        raise InputError(description="Hangman game already active")
    # Get the guess and check its a valid input
    if len(guess) != 1 or not guess.isalpha():
        raise InputError(description="Guess must be a single letter")
    # Convert guess to a capital letter if it is not
    guess = guess.upper()
    # Get the word and guess list
    word = channel_data['hangman word']
    guesses = channel_data['hangman guesses']
    # Check if the letter has already been guessed already
    if guess in guesses:
        raise InputError(description="Letter already guessed")
    # Add letter to list of guesses and update in memory
    guesses.append(guess)
    wd.set_data_with_id('channel data', channel_id, channel_data)
    # Sort letters into correct and incorrect list
    correct_guesses = []
    incorrect_guesses = []
    for letter in guesses:
        if letter in word:
            correct_guesses.append(letter)
        else:
            incorrect_guesses.append(letter)
    # Build message to be printed
    # Start by adding the word being guessed
    message = ' '
    for letter in word:
        if letter in correct_guesses:
            message += letter
        elif letter == ' ':
            message += '   '
        else:
            # Only add space before if previous was _
            if message[-1] != '_':
                message += '_'
            else:
                message += ' _'
    # Check if the game should be ended, its easier to check it here after the message is made
    # Check if the player won the game
    if '_' not in message:
        message = "yay you won!\n" + message
        # Update memory to reflect game is over
        channel_data['hangman word'] = None
        channel_data['hangman guesses'] = []
        wd.set_data_with_id('channel data', channel_id, channel_data)
    # Check if the player has lost the game
    if len(incorrect_guesses) == 10:
        message = "Oh no you killed the man :(\n" + word
        # Update memory to reflect game is over
        channel_data['hangman word'] = None
        channel_data['hangman guesses'] = []
        wd.set_data_with_id('channel data', channel_id, channel_data)
    # Now add the drawing of the hangman
    message += '\n\n'
    message += ascii_art.hangman(len(incorrect_guesses))
    # Now add the list of incorrect guesses
    message += '\nIncorrect guesses:'
    for letter in incorrect_guesses:
        message += (' ' + letter)
    mes_help.create_message_special_user(100000, channel_id, message)
