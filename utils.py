from flask import Response
import json
import dbops
from loguru import logger
import global_vars as g
import requests
import random
import machines


def hit_start_test_api(testboardID,testType,authcode):

    # future: use min tests scheduling to get machineid to schedule test on 
    machineid = random.choice(list(machines.machine2ip.keys()))

    machineip = machines.machine2ip[machineid]

    url = machineip+g.start_test_url

    payload = json.dumps({
      "testType": testType,
      "testboardID": testboardID
    })

    headers = {
      'Authorization': authcode,
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return int(response.status_code)

def hit_stop_test_api(testboardID,testID,authcode):

    test_details = dbops.get_test(testID)

    if test_details is None:
        logger.error("Test does not exist")
        return 0

    machineid = test_details["machineID"]

    machineip = machines.machine2ip[machineid]

    url = machineip+g.stop_test_url

    payload = json.dumps({
      "testID": testID,
      "testboardID": testboardID
    })
    headers = {
      'Authorization': authcode,
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return int(response.status_code)


def get_snapshot_of_testboard(testboardID):

    testboard_details = dbops.get_testboard(testboardID)

    testboard_details["testboardID"] = str(testboard_details["_id"])
    del testboard_details["_id"]


    request_list = []
    for requestID in testboard_details["apiRequests"]:
        request = dbops.get_request(requestID)
        request["requestID"] = str(request["_id"])
        del request["_id"]
        request_list.append(request)

    testboard_details["requests"] = request_list

    return testboard_details


def check_ownership(collection,collectionID,userID):

    r = dbops.fetch_item_with_projection(collection,["creatorID"],field="_id",value=collectionID)

    if len(r) == 0:
        msg = "Collection ID is invalid"
        logger.error(msg)
        return False,msg

    if userID == r[0]["creatorID"]:

        msg = f'{userID} is owner of {collectionID} on {collection}'
        logger.info(msg)
        return True,msg

    msg = f'{userID} is not owner of {collectionID} on {collection}'
    logger.info(msg)

    return False,msg


def check_permissions(collection,collectionID,userID):

    r = dbops.fetch_item_with_projection(collection,["collaboratorIDs","visibility"],field="_id",value=collectionID)

    if len(r) == 0:
        msg = "Collection ID is invalid"
        logger.error(msg)
        return False,msg



    if (userID in r[0]["collaboratorIDs"]) or (r[0]["visibility"] == "public"):

        msg = f'{userID} has valid permissions for {collectionID} on {collection}'
        logger.info(msg)
        return True,msg

    msg = f'{userID} does not have valid permissions for {collectionID} on {collection}'
    logger.error(msg)

    return False,msg


def authenticate(token):

    userID = dbops.authenticate_user(token)

    if userID is None:
        return None,None

    organizationID = dbops.get_organization(userID)

    if organizationID is None:
        logger.error("UserID exists but OrganizationID is deleted.")
        return None,None

    return userID,organizationID


def check_params(params,dtypes,data):

    if all (k in data for k in params) == False:
        logger.error("All parameters not present")

        return False

    for p,d in zip(params,dtypes):

        if type(data[p]) != d:
            logger.error("Error in ",p,d)
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

def return_404_error():

    error_response = Response(status=404)

    return error_response

# def return_422_error(message):

#   error_body = {"message":message}
#     error_response = Response(
#                 response=json.dumps(error_body),
#                 status=422,
#                 mimetype='application/json'
#             )

#     return error_response
