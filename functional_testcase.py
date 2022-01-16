from flask import Blueprint,request
import functional_testcase_utils as functions
from loguru import logger
import global_vars as g 
import traceback  
import utils
from bson.objectid import ObjectId
import fs_utils
import os
import filetype
# import time

profile = Blueprint('functional_testcase', __name__)


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
            ["testboardID","testcaseName","testcaseValues"],[str,str,list],data) == False:
            message = "Invalid params sent in request body for "+endpoint
            logger.error(message+":"+str(data))
            return utils.return_400_error(message)

        for requestdata in data["testcaseValues"]:
            if utils.check_params(
                ["requestBody","responseBody","responseTime","responseCode"],[str,str,str,str],requestdata) == False:
                message = "Invalid params sent in request body for "+endpoint
                logger.error(message+":"+str(data))
                return utils.return_400_error(message)


        #### sanity checks completed and we can now proceed to run accuracy test ####

        testCaseName = data["testcaseName"]
        testboardID = data["testboardID"]
        requests = data["testcaseValues"]


        access_granted,msg = utils.check_permissions("testboards",ObjectId(testboardID),userID)
        if not access_granted:
            logger.error(f"Invalid access rights for {endpoint} by {userID}")
            return utils.return_403_error("You do not have access priviliges for this page.")


        logger.info(f"Test controller add testcase for funcational test attempt: "+str(data) + "by user "+userID)

        result,msg = functions.add_testcase(testboardID,testCaseName,requests)
        
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



@profile.route("/app/testcontroller/functionaltest/testcase/update",methods=["POST"])
def functional_testcontroller_testcase_update():

    endpoint = "/app/testcontroller/functionaltest/testcase/update"

    try:

        #### request authentication ####
        userID,organizationID = utils.authenticate(request.headers.get('Authorization'))
        if userID is None:
            logger.error("Invalid auth token sent for"+endpoint)
            return utils.return_401_error("Session expired. Please login again.")


        #### request body sanity checks ####
        data = request.json
        
        if utils.check_params(
            ["testboardID","testcaseID","testcaseName","testcaseValues"],[str,str,str,list],data) == False:
            message = "Invalid params sent in request body for "+endpoint
            logger.error(message+":"+str(data))
            return utils.return_400_error(message)

        for requestdata in data["testcaseValues"]:
            if utils.check_params(
                ["requestBody","responseBody","responseTime","responseCode"],[str,str,str,str],requestdata) == False:
                message = "Invalid params sent in request body for "+endpoint
                logger.error(message+":"+str(data))
                return utils.return_400_error(message)


        #### sanity checks completed and we can now proceed to run accuracy test ####

        testCaseName = data["testcaseName"]
        testboardID = data["testboardID"]
        testcaseID = data["testcaseID"]
        requests = data["testcaseValues"]

        access_granted,msg = utils.check_permissions("testboards",ObjectId(testboardID),userID)
        if not access_granted:
            logger.error(f"Invalid access rights for {endpoint} by {userID}")
            return utils.return_403_error("You do not have access priviliges for this page.")


        logger.info(f"Test controller UPDATE testcase for funcational test attempt: "+str(data) + "by user "+userID)

        result,msg = functions.edit_testcase(testcaseID,testCaseName,requests,userID)
        
        if result == False:
            message = "Unexpected error occurred."
            return utils.return_400_error(message)

        logger.info("Functional test case UPDATED.")

        return utils.return_200_response({"message":msg,"status":200})
    

    except Exception as e:

        message = "Unexpected error"
        logger.error(message+":"+str(e))
        traceback.print_exc()

        return utils.return_400_error(message)





@profile.route("/app/testcontroller/functionaltest/testcase/delete",methods=["POST"])
def functional_testcontroller_testcase_delete():

    endpoint = "/app/testcontroller/functionaltest/testcase/delete"

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


        logger.info(f"Test controller delete testcase for funcational test attempt: "+str(data) + "by user "+userID)

        result,msg = functions.delete_testcase(testcaseID)
        
        if result == False:
            message = "Unexpected error occurred."
            return utils.return_400_error(message)

        logger.info("Functional test case deleted.")

        return utils.return_200_response({"message":msg,"status":200})
    

    except Exception as e:

        message = "Unexpected error"
        logger.error(message+":"+str(e))
        traceback.print_exc()

        return utils.return_400_error(message)




@profile.route("/app/testcontroller/functionaltest/testcase/list",methods=["POST"])
def functional_testcontroller_testcase_list():

    endpoint = "/app/testcontroller/functionaltest/testcase/list"

    try:

        userID,organizationID = utils.authenticate(request.headers.get('Authorization'))

        if userID is None:
            logger.error("Invalid auth token sent for"+endpoint)
            return utils.return_401_error("Session expired. Please login again.")

        logger.info(f"Functional test cases LIST attempt by user {userID}")

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

        return utils.return_200_response({"message":msg,"status":200,"tests":testcase_list})


    except Exception as e:

        message = "Unexpected error"
        logger.error(message+":"+str(e))
        traceback.print_exc()

        return utils.return_400_error(message)


@profile.route("/app/testcontroller/functionaltest/testcase/import",methods=["POST"])
def functional_testcontroller_testcase_import():

    endpoint = "/app/testcontroller/functionaltest/testcase/import"

    try:

        userID,organizationID = utils.authenticate(request.headers.get('Authorization'))

        if userID is None:
            logger.error("Invalid auth token sent for"+endpoint)
            return utils.return_401_error("Session expired. Please login again.")

        logger.info(f"Functional test cases IMPORT attempt by user {userID}")

        
        data = dict(request.form)

        if utils.check_params(["testboardID"],[str],data) == False:
            message = "Invalid params sent in request body for "+endpoint
            logger.error(message+":"+str(data))
            return utils.return_400_error(message)

        testboardID = data["testboardID"]
    
        access_granted,msg = utils.check_permissions("testboards",ObjectId(testboardID),userID)
        if not access_granted:
            logger.error(f"Invalid access rights for {endpoint} by {userID}")
            return utils.return_403_error("You do not have access priviliges for this page.")

        if 'file' not in request.files:
            message = "file missing in request"
            logger.error(message)
            return utils.return_400_error(message)  
        
        file = request.files['file']

        if file.filename.split(".")[-1].lower() != "csv":
            logger.error("functional testcases import : not a csv file")
            return utils.return_400_error("Not a CSV file")  


        filepath,filename = fs_utils.get_new_filename("./trove/","")
        file.save(filepath)
        kind = "csv"
        newfilepath,newfilename = fs_utils.get_new_filename("./trove/",kind)
        os.system("mv "+filepath+" "+newfilepath)

        result,msg = functions.import_testcases(testboardID,newfilepath)
        
        if result == False:
            logger.error(msg)
            return utils.return_400_error(msg)

        return utils.return_200_response({"message":msg,"status":200})


    except Exception as e:

        message = "Unexpected error"
        logger.error(message+":"+str(e))
        traceback.print_exc()

        return utils.return_400_error(message)






