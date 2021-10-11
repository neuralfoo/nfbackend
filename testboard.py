from flask import Blueprint,request
import testboard_utils as functions
from loguru import logger
import global_vars as g 
import traceback 
import utils

profile = Blueprint('testboard', __name__)


@profile.route("/app/testboard/create",methods=["POST"])
def create_testboard():

    endpoint = "/app/testboard/create"

    try:

        user = utils.authenticate(request.headers.get('Authorization'))

        if user is None:
            logger.error("Invalid auth token sent for"+endpoint)
            return utils.return_401_error("Session expired. Please login again.")

        data = request.json
        
        if utils.check_params(
            {"apiName","apiType","apiEnvironment","apiHttpMethod",
            "apiEndpoint","apiRequestBody","apiResponseBody","apiInputDataType",
            "apiRequestBodyType","apiResponseBodyType"},[str]*10,data) == False:
            message = "Invalid params sent in request body for"+endpoint
            logger.error(message+":"+str(data))
            return utils.return_400_error(message)

        if utils.check_params(
            {"apiHeader"},[list],data) == False:
            message = "Invalid api header sent in request body for"+endpoint
            logger.error(message+":"+str(data))
            return utils.return_400_error(message)

        logger.info("Testboard creation attempt: "+str(data) + "by user "+user)
        
        check_values_list = [
            ["apiType",g.api_types],
            ["apiEnvironment",g.api_environments],
            ["apiHttpMethod",g.api_methods],
            ["apiInputDataType",g.api_input_data_types],
            ["apiRequestBodyType",g.api_request_body_type],
            ["apiResponseBodyType",g.api_response_body_type]
        ]

        for [param,possible_values] in check_values_list:
            if utils.invalid_param_values(data[param],possible_values):
                message = "Invalid value sent in "+param+" for "+endpoint
                logger.error(message+":"+str(data[param]))
                return utils.return_400_error(message)


        testboard_id,msg = functions.create_testboard(data,user)
        
        if testboard_id is None:
            message = "Unexpected error occurred."
            return utils.return_400_error(message)

        if testboard_id == "":
            return utils.return_400_error(msg)            

        return utils.return_200_response({"message":"success","status":200,"id":testboard_id})
    
        

    except Exception as e:

        message = "Unexpected error"
        logger.error(message+":"+str(e))
        traceback.print_exc()

        return utils.return_400_error(message)



@profile.route("/app/testboard/update",methods=["POST"])
def update_testboard():

    endpoint = "/app/testboard/update"

    try:

        user = utils.authenticate(request.headers.get('Authorization'))

        if user is None:
            logger.error("Invalid auth token sent for"+endpoint)
            return utils.return_401_error("Session expired. Please login again.")

        data = request.json
        
        if utils.check_params(
            {"_id","apiName","apiType","apiEnvironment","apiHttpMethod",
            "apiEndpoint","apiRequestBody","apiResponseBody","apiInputDataType",
            "apiRequestBodyType","apiResponseBodyType"},[str]*10,data) == False:
            message = "Invalid params sent in request body for"+endpoint
            logger.error(message+":"+str(data))
            return utils.return_400_error(message)

        if utils.check_params(
            {"apiHeader"},[list],data) == False:
            message = "Invalid api header sent in request body for"+endpoint
            logger.error(message+":"+str(data))
            return utils.return_400_error(message)

        logger.info("Testboard creation attempt: "+str(data) + "by user "+user)
        
        check_values_list = [
            ["apiType",g.api_types],
            ["apiEnvironment",g.api_environments],
            ["apiHttpMethod",g.api_methods],
            ["apiInputDataType",g.api_input_data_types],
            ["apiRequestBodyType",g.api_request_body_type],
            ["apiResponseBodyType",g.api_response_body_type]
        ]

        for [param,possible_values] in check_values_list:
            if utils.invalid_param_values(data[param],possible_values):
                message = "Invalid value sent in "+param+" for "+endpoint
                logger.error(message+":"+str(data[param]))
                return utils.return_400_error(message)


        testboard_id,msg = functions.update_testboard(data,user)
        
        if testboard_id is None:
            message = "Unexpected error occurred."
            return utils.return_400_error(message)

        if testboard_id == "":
            return utils.return_400_error(msg)            

        return utils.return_200_response({"message":"success","status":200,"id":testboard_id})
    
        

    except Exception as e:

        message = "Unexpected error"
        logger.error(message+":"+str(e))
        traceback.print_exc()

        return utils.return_400_error(message)



@profile.route("/app/testboard/get/<testboard_id>",methods=["GET"])
def get_testboard(testboard_id):

    endpoint = "/app/testboard/get/<testboard_id>"

    try:

        user = utils.authenticate(request.headers.get('Authorization'))

        if user is None:
            logger.error("Invalid auth token sent for"+endpoint)
            return utils.return_401_error("Session expired. Please login again.")

        logger.info("Testboard get attempt: "+testboard_id+" by user "+user)


        testboard_details,msg = functions.get_testboard(testboard_id)
        
        if testboard_details is None:
            message = "Unexpected error occurred."
            return utils.return_400_error(message)            

        return utils.return_200_response({"message":msg,"status":200,"testboard":testboard_details})
    
        

    except Exception as e:

        message = "Unexpected error"
        logger.error(message+":"+str(e))
        traceback.print_exc()

        return utils.return_400_error(message)