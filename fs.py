from flask import Blueprint,request

import json
import dbops 
from loguru import logger
import traceback
import datetime 
import utils
import os
from werkzeug.utils import secure_filename


profile = Blueprint('fs', __name__)


@profile.route("/app/fs/image/upload",methods=["POST"])
def image_upload_to_testboard():

    try:
        endpoint = "/app/fs/image/upload"
        userID,organizationID = utils.authenticate(request.headers.get('Authorization'))

        if userID is None:
            logger.error("Invalid auth token sent for "+endpoint)
            return utils.return_401_error("Session expired. Please login again.")


        logger.info("Image file UPLOAD attempt: "+str(userID))

        if 'file' not in request.files:
            message = "file missing in request"
            logger.error(message)
            return utils.return_400_error(message)  
        
        file = request.files['file']

        filename = secure_filename(file.filename)
        file.save(os.path.join("./trove/tmp/", filename))

        body = {
            "result":"success",
        }

        logger.info("Image file UPLOAD successful: "+str(userID))

        return utils.return_200_response(body)
    
    except Exception as e:

        message = "Unexpected error"
        logger.error(message+":"+str(e))
        traceback.print_exc()

        return utils.return_400_error(message)