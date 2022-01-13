from flask import Blueprint,request
import webhook_utils as functions
from loguru import logger
import global_vars as g 
import traceback  
import utils
from bson.objectid import ObjectId

# import time

profile = Blueprint('webhook', __name__)


@profile.route("/app/webhook/<testType>/<testboardID>",methods=["POST"])
def open_webhook(testType,testboardID):

    endpoint = f"/app/webhook/{testType}/{testboardID}"

    try:


        logger.info(f"Webhook request received on {endpoint}")
        
        if testType not in ["accuracy","functional"]:
            logger.error(f"Invalid testType:{testType}")
            return utils.return_400_error("Invalid endpoint")

        data = request.get_data(as_text=True)

        logger.info(f"Data:{data}")
        
        hitID,msg = functions.webhook_save_request(testboardID,testType,data,"POST")
        
        if hitID is None:
            logger.error(msg)
            return utils.return_400_error(msg)

        logger.info(f"webhook request received, hitID: {hitID}")

        return utils.return_200_response({"message":msg,"status":200})


    except Exception as e:

        message = "Unexpected error"
        logger.error(message+":"+str(e))
        traceback.print_exc()

        return utils.return_400_error(message)