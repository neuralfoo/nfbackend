from flask import Response
import json
import dbops

def authenticate(token):

    user = dbops.authenticate_user(token)

    return user


def check_params(params,dtypes,data):

    if data.keys() < params:

        return False

    for p,d in zip(params,dtypes):

        if type(data[p]) != d:
            return False

    return True


def invalid_param_values(value,possible_values):

    if value in possible_values:
        return False 
    else:
        return True


def return_200_response(body):

    success_response = Response(
                response=json.dumps(body),
                status=200,
                mimetype='application/json'
            )

    return success_response

def return_400_error(message):

    error_body = {"message":message}
    error_response = Response(
                response=json.dumps(error_body),
                status=400,
                mimetype='application/json'
            )

    return error_response


def return_401_error(message):

    error_body = {"message":message}
    error_response = Response(
                response=json.dumps(error_body),
                status=401,
                mimetype='application/json'
            )

    return error_response

# def return_422_error(message):

#   error_body = {"message":message}
#     error_response = Response(
#                 response=json.dumps(error_body),
#                 status=422,
#                 mimetype='application/json'
#             )

#     return error_response
