from flask import Blueprint,request
import accuracy_testcase_utils as functions
from loguru import logger
import global_vars as g 
import traceback  
import utils
from bson.objectid import ObjectId

# import time

profile = Blueprint('accuracy_testcase', __name__)


@profile.route("/app/testcontroller/accuracytest/testcase/add",methods=["POST"])
def accuracy_testcontroller_testcase_add():

    endpoint = "/app/testcontroller/accuracytest/testcase/add"

    try:

        #### request authentication ####
        userID,organizationID = utils.authenticate(request.headers.get('Authorization'))
        if userID is None:
            logger.error("Invalid auth token sent for"+endpoint)
            return utils.return_401_error("Session expired. Please login again.")


        #### request body sanity checks ####
        data = request.json
        
        if utils.check_params(
            ["testboardID","requestVariables","responseVariables"],[str,str,str],data) == False:
            message = "Invalid params sent in request body for "+endpoint
            logger.error(message+":"+str(data))
            return utils.return_400_error(message)


        #### sanity checks completed and we can now proceed to run accuracy test ####

        testboardID = data["testboardID"]
        responseVariables = data["responseVariables"]
        requestVariables = data["requestVariables"]

        access_granted,msg = utils.check_permissions("testboards",ObjectId(testboardID),userID)
        if not access_granted:
            logger.error(f"Invalid access rights for {endpoint} by {userID}")
            return utils.return_403_error("You do not have access priviliges for this page.")


        logger.info(f"Test controller add testcase for accuracy test attempt: "+str(data) + "by user "+userID)

        result,msg = functions.add_testcase(testboardID,requestVariables,responseVariables,userID)
        
        if result == False:
            message = "Unexpected error occurred."
            return utils.return_400_error(message)

        logger.info("accuracy test case added.")

        return utils.return_200_response({"message":msg,"status":200})
    

    except Exception as e:

        message = "Unexpected error"
        logger.error(message+":"+str(e))
        traceback.print_exc()

        return utils.return_400_error(message)



@profile.route("/app/testcontroller/accuracytest/testcase/update",methods=["POST"])
def accuracy_testcontroller_testcase_update():

    endpoint = "/app/testcontroller/accuracytest/testcase/update"

    try:

        #### request authentication ####
        userID,organizationID = utils.authenticate(request.headers.get('Authorization'))
        if userID is None:
            logger.error("Invalid auth token sent for"+endpoint)
            return utils.return_401_error("Session expired. Please login again.")


        #### request body sanity checks ####
        data = request.json
        
        if utils.check_params(
            ["testboardID","testcaseID","requestVariables","responseVariables"],[str,str,str,str],data) == False:
            message = "Invalid params sent in request body for "+endpoint
            logger.error(message+":"+str(data))
            return utils.return_400_error(message)


        #### sanity checks completed and we can now proceed to run accuracy test ####

        
        testboardID = data["testboardID"]
        testcaseID = data["testcaseID"]
        responseVariables = data["responseVariables"]
        requestVariables = data["requestVariables"]

        access_granted,msg = utils.check_permissions("testboards",ObjectId(testboardID),userID)
        if not access_granted:
            logger.error(f"Invalid access rights for {endpoint} by {userID}")
            return utils.return_403_error("You do not have access priviliges for this page.")


        logger.info(f"Test controller UPDATE testcase for accuracy test attempt: "+str(data) + "by user "+userID)

        result,msg = functions.edit_testcase(testcaseID,responseVariables,requestVariables,userID)
        
        if result == False:
            message = "Unexpected error occurred."
            return utils.return_400_error(message)

        logger.info("accuracy test case UPDATED.")

        return utils.return_200_response({"message":msg,"status":200})
    

    except Exception as e:

        message = "Unexpected error"
        logger.error(message+":"+str(e))
        traceback.print_exc()

        return utils.return_400_error(message)





@profile.route("/app/testcontroller/accuracytest/testcase/delete",methods=["POST"])
def accuracy_testcontroller_testcase_delete():

    endpoint = "/app/testcontroller/accuracytest/testcase/delete"

    try:
        #### request authentication ####
        userID,organizationID = utils.authenticate(request.headers.get('Authorization'))
        if userID is None:
            logger.error("Invalid auth token sent for"+endpoint)
            return utils.return_401_error("Session expired. Please login again.")


        #### request body sanity checks ####
        data = request.json
        
        if utils.check_params(
            ["testboardID","testcaseID"],[str,str],data) == False:
            message = "Invalid params sent in request body for "+endpoint
            logger.error(message+":"+str(data))
            return utils.return_400_error(message)


        #### sanity checks completed and we can now proceed to process the request ####

        testcaseID = data["testcaseID"]
        testboardID = data["testboardID"]

        access_granted,msg = utils.check_permissions("testboards",ObjectId(testboardID),userID)
        if not access_granted:
            logger.error(f"Invalid access rights for {endpoint} by {userID}")
            return utils.return_403_error("You do not have access priviliges for this page.")


        logger.info(f"Test controller delete testcase for accuracy test attempt: "+str(data) + "by user "+userID)

        result,msg = functions.delete_testcase(testcaseID)
        
        if result == False:
            message = "Unexpected error occurred."
            return utils.return_400_error(message)

        logger.info("accuracy test case deleted.")

        return utils.return_200_response({"message":msg,"status":200})
    

    except Exception as e:

        message = "Unexpected error"
        logger.error(message+":"+str(e))
        traceback.print_exc()

        return utils.return_400_error(message)




@profile.route("/app/testcontroller/accuracytest/testcase/list",methods=["POST"])
def accuracy_testcontroller_testcase_list():

    endpoint = "/app/testcontroller/accuracytest/testcase/list"

    try:

        userID,organizationID = utils.authenticate(request.headers.get('Authorization'))

        if userID is None:
            logger.error("Invalid auth token sent for"+endpoint)
            return utils.return_401_error("Session expired. Please login again.")

        logger.info(f"accuracy test cases LIST attempt by user {userID}")

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

        testcase_list,msg = functions.get_testcases(testboardID)
        
        if testcase_list is None:
            logger.error(msg)
            return utils.return_400_error(msg)

        return utils.return_200_response({"message":msg,"status":200,"testcases":testcase_list})


    except Exception as e:

        message = "Unexpected error"
        logger.error(message+":"+str(e))
        traceback.print_exc()

        return utils.return_400_error(message)









