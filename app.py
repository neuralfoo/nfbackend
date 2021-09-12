from flask import Flask,request
import json
import dbops 
from loguru import logger
import traceback
import datetime 
import utils

app = Flask(__name__)

@app.route("/login",methods=["POST"])
def login():

    try:

        data = request.json

        if utils.check_params({"email","password"},[str,str],data) == False:
            message = "Invalid params sent in request body"
            logger.error(message+":"+str(data))
            return utils.return_400_error(message)

        logger.info("Login attempt: "+str(data))
        
        combo_exists = dbops.check_if_exists("users",field="email",value=data["email"],field2="password",value2=data["password"])

        if combo_exists:
            token = dbops.create_auth_token(data["email"],data["password"])
            body = {"token":token}
            return utils.return_200_response(body)
        

        return utils.return_401_error("Authorization Failed")

    except Exception as e:

        message = "Unexpected error"
        logger.error(message+":"+str(e))
        traceback.print_exc()

        return utils.return_400_error(message)
        



@app.route("/signup",methods=["POST"])
def signup():

    try:

        data = request.json

        if utils.check_params({"email","password","name"},[str,str,str],data) == False:
            message = "Invalid params sent in request body"
            logger.error(message+":"+str(data))
            return utils.return_400_error(message)
            

        logger.info("Sign up request received:"+str(data))

        email_exists = dbops.check_if_exists(collection="users",field="email",value=data["email"],field2=None,value2=None)

        if email_exists :
            message = "Email id is already registered "
            logger.error(message+str(data))
            return utils.return_400_error(message)

        signupdatetime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        userid = dbops.insert_user(data["name"],data["email"],data["password"],signupdatetime,role="",parentemail="")
        
        body = {"userid":str(userid)}

        return utils.return_200_response(body)

    except Exception as e:

        message = "Unexpected error"
        logger.error(message+":"+str(e))
        traceback.print_exc()

        return utils.return_400_error(message)


















