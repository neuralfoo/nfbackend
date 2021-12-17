from flask import Blueprint,request
import functionaltest_utils as functions
from loguru import logger
import global_vars as g 
import traceback  
import utils
from bson.objectid import ObjectId

# import time

profile = Blueprint('functionaltest', __name__)


@profile.route("/app/testcontroller/functionaltest/testcase/add",methods=["POST"])
def functional_testcontroller_testcase_add():

    endpoint = "/app/testcontroller/functionaltest/testcase/add"

    try:

        #### request authentication ####
        userID,organizationID = utils.authenticate(request.headers.get('Authorization'))
        if userID is None:
            logger.error("Invalid auth token sent for"+endpoint)
            return utils.return_401_error("Session expired. Please login again.")


        #### request body sanity checks ####
        data = request.json
        
        if utils.check_params(
            ["testboardID","testCaseName","requests"],[str,str,list],data) == False:
            message = "Invalid params sent in request body for "+endpoint
            logger.error(message+":"+str(data))
            return utils.return_400_error(message)

        for request in data["requests"]:
            if utils.check_params(
                ["requestBody","responseBody","responseTime","responseCode"],[str,str,str,str],request) == False:
                message = "Invalid params sent in request body for "+endpoint
                logger.error(message+":"+str(data))
                return utils.return_400_error(message)


        #### sanity checks completed and we can now proceed to run accuracy test ####

        testCaseName = data["testCaseName"]
        testboardID = data["testboardID"]
        requests = data["requests"]


        access_granted,msg = utils.check_permissions("testboards",ObjectId(testboardID),userID)
        if not access_granted:
            logger.error(f"Invalid access rights for {endpoint} by {userID}")
            return utils.return_403_error("You do not have access priviliges for this page.")


        logger.info(f"Test controller add testcase for funcational test attempt: "+str(data) + "by user "+userID)

        result,msg = functions.add_testcase(testboardID,testCaseName,requests,userID)
        
        if result == False:
            message = "Unexpected error occurred."
            return utils.return_400_error(message)

        logger.info("Functional test case added.")

        return utils.return_200_response({"message":msg,"status":200})
    

    except Exception as e:

        message = "Unexpected error"
        logger.error(message+":"+str(e))
        traceback.print_exc()

        return utils.return_400_error(message)









