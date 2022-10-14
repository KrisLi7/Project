from werkzeug.exceptions import HTTPException


class AccessError(HTTPException):
    """ Raise AccessError in code 400 """
    code = 404
    message = 'No message specified'


class InputError(HTTPException):
    """ Raise InputError in code 400 """
    code = 400
    message = 'No message specified'
