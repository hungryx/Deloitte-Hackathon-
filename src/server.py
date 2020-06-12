'''
Author: Nikola Medimurac, Sam Agnihotri
Code for running the flask server
Contains all route defintions
'''

import sys
from json import dumps
import io
from flask import Flask, request, Response, abort
from flask_cors import CORS
from PIL import Image
import auth
import channel
import channels
import message
import user
import other
import standup
import server_helper as serv_help
import special_users
from error import InputError

# pylint: disable=missing-function-docstring
# pylint: disable=broad-except

def defaultHandler(err):    #pylint: disable=invalid-name
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Set port as a global variable so flask function can use it if needed
#global PORT

# ***************** Routes for images *************************
@APP.route("/profile_imgs/<pic_name>.jpg")
def image_server(pic_name):
    file = '../profile_imgs/' + pic_name
    try:
        im = Image.open(file) #pylint: disable=invalid-name
        im.thumbnail((256, 256), Image.ANTIALIAS)
        with io.BytesIO() as output:
            im.save(output, format="JPEG")
            contents = output.getvalue()
        return Response(contents, mimetype='image/jpeg')
    except IOError:
        abort(404)

# ************** Routes From Specifications *******************
@APP.route("/auth/login", methods=['POST'])
def login():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['email', 'password'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(auth.auth_login(
            data['email'], data['password']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/auth/logout", methods=['POST'])
def logout():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['token'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(auth.auth_logout(
            data['token']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/auth/register", methods=['POST'])
def register():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['email', 'password', 'name_first', 'name_last'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(auth.auth_register(
            data['email'], data['password'], data['name_first'], data['name_last']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/auth/passwordreset/request", methods=['POST'])
def request_reset():
    # Wrap it all in a try so if an exceptoin is raised its returned
    try:
        #Get data from request
        data = request.get_json()
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['email'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(auth.auth_passwordreset_request(
            data['email']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/auth/passwordreset/reset", methods=['POST'])
def password_reset():
    # Wrap it all in a try so if an exceptoin is raised its returned
    try:
        #Get data from request
        data = request.get_json()
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        #if (not isinstance(data, dict) or not
        #        serv_help.is_input_correct(data,
        #                                   ['code', 'password'])):
        #    return defaultHandler(InputError(description=
        #                                     "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(auth.auth_passwordreset_reset(
            data['reset_code'], data['new_password']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/channel/invite", methods=['POST'])
def invite():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        if data['channel_id'] and data['u_id']:
            data['channel_id'] = int(data['channel_id'])
            data['u_id'] = int(data['u_id'])
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['token', 'channel_id', 'u_id'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(channel.channel_invite(
            data['token'], data['channel_id'], data['u_id']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/channel/details", methods=['GET'])
def details():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        #data = request.get_json()
        data = request.args.to_dict()
        if data['channel_id']:
            data['channel_id'] = int(data['channel_id'])
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['token', 'channel_id'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(channel.channel_details(
            data['token'], data['channel_id'], PORT))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/channel/messages", methods=['GET'])
def messages():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        #data = request.get_json()
        data = request.args.to_dict()
        if data['channel_id'] and data['start']:
            data['channel_id'] = int(data['channel_id'])
            data['start'] = int(data['start'])
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['token', 'channel_id', 'start'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(channel.channel_messages(
            data['token'], data['channel_id'], data['start']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/channel/leave", methods=['POST'])
def leave():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['token', 'channel_id'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(channel.channel_leave(
            data['token'], data['channel_id']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/channel/join", methods=['POST'])
def join():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        if data['channel_id']:
            data['channel_id'] = int(data['channel_id'])
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['token', 'channel_id'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(channel.channel_join(
            data['token'], data['channel_id']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/channel/addowner", methods=['POST'])
def addowner():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        if data['channel_id'] and data['u_id']:
            data['channel_id'] = int(data['channel_id'])
            data['u_id'] = int(data['u_id'])
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['token', 'channel_id', 'u_id'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(channel.channel_addowner(
            data['token'], data['channel_id'], data['u_id']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/channel/removeowner", methods=['POST'])
def removeowner():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        if data['channel_id'] and data['u_id']:
            data['channel_id'] = int(data['channel_id'])
            data['u_id'] = int(data['u_id'])
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['token', 'channel_id', 'u_id'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(channel.channel_removeowner(
            data['token'], data['channel_id'], data['u_id']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/channels/list", methods=['GET'])
def clist():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        #data = request.get_json()
        data = request.args.to_dict()
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['token'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(channels.channels_list(
            data['token']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/channels/listall", methods=['GET'])
def listall():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        #data = request.get_json()
        data = request.args.to_dict()
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['token'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(channels.channels_listall(
            data['token']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/channels/create", methods=['POST'])
def create():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['token', 'name', 'is_public'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(channels.channels_create(
            data['token'], data['name'], data['is_public']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/message/send", methods=['POST'])
def send():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        if data['channel_id']:
            data['channel_id'] = int(data['channel_id'])
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['token', 'channel_id', 'message'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(message.message_send(
            data['token'], data['channel_id'], data['message']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/message/sendlater", methods=['POST'])
def sendlater():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        if data['channel_id']:
            data['channel_id'] = int(data['channel_id'])
            data['time_sent'] = int(data['time_sent'])
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['token', 'channel_id', 'message', 'time_sent'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(message.message_sendlater(
            data['token'], data['channel_id'], data['message'], data['time_sent']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/message/react", methods=['POST'])
def react():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        data['message_id'] = int(data['message_id'])
        data['react_id'] = int(data['react_id'])
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        #if (not isinstance(data, dict) or not
        #        serv_help.is_input_correct(data,
        #                                   ['token', 'message_id', 'react_id'])):
        #    return defaultHandler(InputError(description=
        #                                     "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(message.message_react(
            data['token'], data['message_id'], data['react_id']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/message/unreact", methods=['POST'])
def unreact():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        data['message_id'] = int(data['message_id'])
        data['react_id'] = int(data['react_id'])
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        #if (not isinstance(data, dict) or not
        #        serv_help.is_input_correct(data,
        #                                   ['token', 'message_id', 'react_id'])):
        #    return defaultHandler(InputError(description=
        #                                     "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(message.message_unreact(
            data['token'], data['message_id'], data['react_id']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/message/pin", methods=['POST'])
def pin():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        data['message_id'] = int(data['message_id'])
        print(data)
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        #if (not isinstance(data, dict) or not
        #        serv_help.is_input_correct(data,
        #                                   ['token', 'message_id'])):
        #    return defaultHandler(InputError(description=
        #                                     "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(message.message_pin(
            data['token'], data['message_id']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/message/unpin", methods=['POST'])
def unpin():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        data['message_id'] = int(data['message_id'])
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        #if (not isinstance(data, dict) or not
        #        serv_help.is_input_correct(data,
        #                                   ['token', 'message_id'])):
        #    return defaultHandler(InputError(description=
        #                                     "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(message.message_unpin(
            data['token'], data['message_id']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/message/remove", methods=['DELETE'])
def remove():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        data['message_id'] = int(data['message_id'])
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        #if (not isinstance(data, dict) or not
        #        serv_help.is_input_correct(data,
        #                                   ['token', 'message_id'])):
        #    return defaultHandler(InputError(description=
        #                                     "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(message.message_remove(
            data['token'], data['message_id']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/message/edit", methods=['PUT'])
def edit():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        if data['message_id']:
            data['message_id'] = int(data['message_id'])
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        #if (not isinstance(data, dict) or not
        #        serv_help.is_input_correct(data,
        #                                   ['token', 'message_id', 'message'])):
        #    return defaultHandler(InputError(description=
        #                                     "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(message.message_edit(
            data['token'], data['message_id'], data['message']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/user/profile", methods=['GET'])
def profile():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        #data = request.get_json()
        data = request.args.to_dict()
        # Since its coming back as an int for id
        if data['u_id']:
            data['u_id'] = int(data['u_id'])
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['token', 'u_id'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(user.user_profile(
            data['token'], data['u_id'], PORT))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/user/profile/setname", methods=['PUT'])
def profile_setname():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['token', 'name_first', 'name_last'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(user.user_profile_setname(
            data['token'], data['name_first'], data['name_last']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/user/profile/setemail", methods=['PUT'])
def profile_setemail():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['token', 'email'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(user.user_profile_setemail(
            data['token'], data['email']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/user/profile/sethandle", methods=['PUT'])
def profile_sethandle():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['token', 'handle_str'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(user.user_profile_sethandle(
            data['token'], data['handle_str']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/user/profile/uploadphoto", methods=['POST'])
def profile_uploadphoto():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if not isinstance(data, dict):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(user.user_profile_uploadphoto(
            data['token'], data['img_url'], int(data['x_start']), int(data['y_start']),
            int(data['x_end']), int(data['y_end'])))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/users/all", methods=['GET'])
def uall():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        #data = request.get_json()
        data = request.args.to_dict()
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['token'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(other.users_all(
            data['token']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/search", methods=['GET'])
def search():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        #data = request.get_json()
        data = request.args.to_dict()
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['token', 'query_str'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(other.search(
            data['token'], data['query_str']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/standup/start", methods=['POST'])
def start():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        data['channel_id'] = int(data['channel_id'])
        data['length'] = int(data['length'])
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['token', 'channel_id', 'length'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(standup.standup_start(
            data['token'], data['channel_id'], data['length']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/standup/active", methods=['GET'])
def active():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        data = request.args.to_dict()
        if data['channel_id']:
            data['channel_id'] = int(data['channel_id'])
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['token', 'channel_id'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(standup.standup_active(
            data['token'], data['channel_id']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/standup/send", methods=['POST'])
def ssend():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        data['channel_id'] = int(data['channel_id'])
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['token', 'channel_id', 'message'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(standup.standup_send(
            data['token'], data['channel_id'], data['message']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/admin/userpermission/change", methods=['POST'])
def change():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        data['u_id'] = int(data['u_id'])
        data['permission_id'] = int(data['permission_id'])
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['token', 'u_id', 'permission_id'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(other.admin_user_permission_change(
            data['token'], data['u_id'], data['permission_id']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/admin/user/remove", methods=['POST'])
def u_remove():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Get data from request
        data = request.get_json()
        data['u_id'] = int(data['u_id'])
        # Check correct data was given and that the data read is a dictionary,
        # if not raise an InputError
        if (not isinstance(data, dict) or not
                serv_help.is_input_correct(data,
                                           ['token', 'u_id'])):
            return defaultHandler(InputError(description=
                                             "Incorrect input fields or input types given"))
        # Call the corresponding function and return the result
        return dumps(other.admin_user_remove(
            data['token'], data['u_id']))
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

@APP.route("/workspace/reset", methods=['POST'])
def reset():
    # Wrap it all in a try so if an exception is raised its returned
    try:
        # Call the corresponding function and return the result
        return dumps(other.workspace_reset())
    except Exception as err:
        # Pass the exception to the handler function given
        return defaultHandler(err)

if __name__ == "__main__":
    # First thing to do when starting server is to restore its state
    # Read in data saved in memory
    serv_help.load_stored_data()
    # Reset timers for active standups and message send laters, as well as finish active ones
    serv_help.check_messages_to_send()
    serv_help.check_standups_active()
    # Start the server updater thread which keeps repeating every second
    # currently this just saves the servers data to a file every second
    serv_help.run_updater_thread()
    # Start the server on the given port
    if len(sys.argv) == 2:
        PORT = int(sys.argv[1])
    else:
        PORT = 8080
    # Update the special users data
    special_users.create_special_users(PORT)
    APP.run(port=PORT)
    #APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
