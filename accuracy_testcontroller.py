import utils
import traceback  
import global_vars as g 
from loguru import logger
from bson.objectid import ObjectId
from flask import Blueprint,request
import accuracy_testcontroller_utils as functions


profile = Blueprint('accuracy_testcontroller', __name__)


@profile.route("/app/testcontroller/accuracytest/action",methods=["POST"])
def accuracy_testcontroller_action():

    endpoint = "/app/testcontroller/accuracytest/action"

    try:

        #### request authentication ####
        userID,organizationID = utils.authenticate(request.headers.get('Authorization'))
        if userID is None:
            logger.error("Invalid auth token sent for"+endpoint)
            return utils.return_401_error("Session expired. Please login again.")


        #### request body sanity checks ####
        data = request.json
        
        if utils.check_params(
            ["testboardID","action","accuracyTestID"],[str,str,str],data) == False:
            message = "Invalid params sent in request body for "+endpoint
            logger.error(message+":"+str(data))
            return utils.return_400_error(message)


        check_values_list = [
            ["action",g.testcontroller_actions]
        ]

        for [param,possible_values] in check_values_list:
            if utils.invalid_param_values(data[param],possible_values):
                message = "Invalid value sent in "+param+" for "+endpoint
                logger.error(message+":"+str(data[param]))
                return utils.return_400_error(message)

        #### sanity checks completed and we can now proceed to run accuracy test ####

        action = data["action"]
        testboardID = data["testboardID"]
        accuracyTestID = data["accuracyTestID"]


        access_granted,msg = utils.check_permissions("testboards",ObjectId(testboardID),userID)
        if not access_granted:
            logger.error(f"Invalid access rights for {endpoint} by {userID}")
            return utils.return_403_error("You do not have access priviliges for this page.")


        logger.info(f"Test controller {action} accuracy test attempt: "+str(data) + "by user "+userID)

        authcode = request.headers.get('Authorization')
        result,msg = functions.accuracy_testcontroller(testboardID,action,userID,authcode,accuracyTestID)
        
        if result == False:
            message = "Unexpected error occurred."
            return utils.return_400_error(message)

        logger.info(f"Accuracy test successfully {action}ed")

        return utils.return_200_response({"message":msg,"status":200})
    

    except Exception as e:

        message = "Unexpected error"
        logger.error(message+":"+str(e))
        traceback.print_exc()

        return utils.return_400_error(message)




@profile.route("/app/testcontroller/accuracytest/list",methods=["POST"])
def accuracy_testcontroller_list():

    endpoint = "/app/testcontroller/accuracytest/list"

    try:

        userID,organizationID = utils.authenticate(request.headers.get('Authorization'))

        if userID is None:
            logger.error("Invalid auth token sent for"+endpoint)
            return utils.return_401_error("Session expired. Please login again.")

        logger.info(f"Image classification Accuracy test LIST attempt by user {userID}")

        data = request.json

        if utils.check_params(["testboardID"],[str],data) == False:
            message = "Invalid params sent in request body for "+endpoint
            logger.error(message+":"+str(data))
            return utils.return_400_error(message)

        testboardID = data["testboardID"]

        access_granted,msg = utils.check_permissions("testboards",ObjectId(testboardID),userID)
        if not access_granted:
            logger.error(f"Invalid access rights for {endpoint} by {userID}")
            return utils.return_403_error("You do not have access priviliges for this page.")

        test_list,msg = functions.accuracy_testcontroller_list(testboardID)
        
        if test_list is None:
            logger.error(msg)
            return utils.return_400_error(msg)

        return utils.return_200_response({"message":msg,"status":200,"tests":test_list})


    except Exception as e:

        message = "Unexpected error"
        logger.error(message+":"+str(e))
        traceback.print_exc()

        return utils.return_400_error(message)



@profile.route("/app/testcontroller/accuracytest/details",methods=["POST"])
def accuracy_testcontroller_details():

    endpoint = "/app/testcontroller/accuracytest/details"

    try:

        userID,organizationID = utils.authenticate(request.headers.get('Authorization'))

        if userID is None:
            logger.error("Invalid auth token sent for"+endpoint)
            return utils.return_401_error("Session expired. Please login again.")

        logger.info(f"Image classification Accuracy test LIST attempt by user {userID}")

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

        test_details,msg = functions.accuracy_testcontroller_details(testID,testboardID)
        
        if test_details is None:
            logger.error(msg)
            return utils.return_400_error(msg)

        return utils.return_200_response({"message":msg,"status":200,"test":test_details})


    except Exception as e:

        message = "Unexpected error"
        logger.error(message+":"+str(e))
        traceback.print_exc()

        return utils.return_400_error(message)










