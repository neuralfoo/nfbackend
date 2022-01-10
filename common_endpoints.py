from flask import Blueprint,request
import common_endpoints_utils as functions
from loguru import logger
import global_vars as g 
import traceback  
import utils
from bson.objectid import ObjectId

# import time

profile = Blueprint('common_endpoints', __name__)


@profile.route("/app/testcontroller/test/delete",methods=["POST"])
def delete_test():

    endpoint = "/app/testcontroller/test/delete"

    try:

        userID,organizationID = utils.authenticate(request.headers.get('Authorization'))

        if userID is None:
            logger.error("Invalid auth token sent for"+endpoint)
            return utils.return_401_error("Session expired. Please login again.")

        logger.info(f"test DELETE attempt by user {userID}")

        data = request.json

        if utils.check_params(["testID","testboardID"],[str,str],data) == False:
            message = "Invalid params sent in request body for "+endpoint
            logger.error(message+":"+str(data))
            return utils.return_400_error(message)

        testID = data["testID"]
        testboardID = data["testboardID"]

        access_granted,msg = utils.check_permissions("testboards",ObjectId(testboardID),userID)
        if not access_granted:
            logger.error(f"Invalid access rights for {endpoint} by {userID}")
            return utils.return_403_error("You do not have access priviliges for this page.")

        result,msg = functions.delete_test(testID)
        
        if result == False:
            logger.error(msg)
            return utils.return_400_error(msg)

        return utils.return_200_response({"message":msg,"status":200})


    except Exception as e:

        message = "Unexpected error"
        logger.error(message+":"+str(e))
        traceback.print_exc()

        return utils.return_400_error(message)



@profile.route("/app/testcontroller/test/hitlist",methods=["POST"])
def get_api_hits():

    endpoint = "/app/testcontroller/test/hitlist"

    try:

        userID,organizationID = utils.authenticate(request.headers.get('Authorization'))

        if userID is None:
            logger.error("Invalid auth token sent for"+endpoint)
            return utils.return_401_error("Session expired. Please login again.")

        logger.info(f"test api hit LIST attempt by user {userID}")

        data = request.json

        if utils.check_params(["testboardID","testID"],[str,str],data) == False:
            message = "Invalid params sent in request body for "+endpoint
            logger.error(message+":"+str(data))
            return utils.return_400_error(message)

        testboardID = data["testboardID"]
        testID = data["testID"]

        access_granted,msg = utils.check_permissions("testboards",ObjectId(testboardID),userID)
        if not access_granted:
            logger.error(f"Invalid access rights for {endpoint} by {userID}")
            return utils.return_403_error("You do not have access priviliges for this page.")

        api_hits,msg = functions.list_api_hits(testID,testboardID)
        
        if api_hits is None:
            logger.error(msg)
            return utils.return_400_error(msg)

        return utils.return_200_response({"message":msg,"status":200,"hits":api_hits})


    except Exception as e:

        message = "Unexpected error"
        logger.error(message+":"+str(e))
        traceback.print_exc()

        return utils.return_400_error(message)


#  this is an internal endpoint, not supposed to be hit by users
@profile.route(g.stop_test_url,methods=["POST"])
def stop_test():

    endpoint = g.stop_test_url

    try:

        #### request authentication ####
        userID,organizationID = utils.authenticate(request.headers.get('Authorization'))
        if userID is None:
            logger.error("Invalid auth token sent for"+endpoint)
            return utils.return_401_error("Session expired. Please login again.")


        #### request body sanity checks ####
        data = request.json
        
        if utils.check_params(
            ["testID"],[str],data) == False:
            message = "Invalid params sent in request body for "+endpoint
            logger.error(message+":"+str(data))
            return utils.return_400_error(message)

        #### sanity checks completed and we can now proceed to run stop the test ####

        testID = data["testID"]

        access_granted,msg = utils.check_permissions("testboards",ObjectId(testboardID),userID)
        if not access_granted:
            logger.error(f"Invalid access rights for {endpoint} by {userID}")
            return utils.return_403_error("You do not have access priviliges for this page.")


        logger.info(f"Test controller stop test attempt: "+str(data) + "by user "+userID)


        result,msg = functions.stop_test(testID)
        
        if result == False:
            message = "Unexpected error occurred."
            return utils.return_400_error(message)

        logger.info(f"Test successfully stopped")

        return utils.return_200_response({"message":msg,"status":200})
    

    except Exception as e:

        message = "Unexpected error"
        logger.error(message+":"+str(e))
        traceback.print_exc()

        return utils.return_400_error(message)


