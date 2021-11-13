from flask import Blueprint,request
import testcontroller_utils as functions
from loguru import logger
import global_vars as g 
import traceback  
import utils
from bson.objectid import ObjectId

# import time

profile = Blueprint('testcontroller', __name__)


@profile.route("/app/testcontroller/imageclassification/accuracytest/action",methods=["POST"])
def imageclassification_accuracy_testcontroller():

    endpoint = "/app/testcontroller/imageclassification/accuracytest/action"

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


        #### sanity checks completed and we can now proceed to insert data into DB ####

        action = data["action"]
        testboardID = data["testboardID"]
        accuracyTestID = data["accuracyTestID"]

        logger.info(f"Test controller {action} accuracy test attempt: "+str(data) + "by user "+userID)


        result,msg = functions.imageclassification_accuracy_testcontroller(testboardID,action,userID,accuracyTestID)
        
        if result == False:
            message = "Unexpected error occurred."
            return utils.return_400_error(message)

        logger.info(f"Accuracy test successfilly {action}ed")

        return utils.return_200_response({"message":msg,"status":200})
    

    except Exception as e:

        message = "Unexpected error"
        logger.error(message+":"+str(e))
        traceback.print_exc()

        return utils.return_400_error(message)
