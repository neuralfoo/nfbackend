import pymongo
import string
import secrets
import datetime 
from loguru import logger
from bson.objectid import ObjectId

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

db = myclient["neuralfoo"]


def insert_user(name,email,password,signupdate,role="",parentemail=""):

    users = db["users"]
    user = {
    		"name": name, 
    		"email":email, 
    		"password": password,
    		"role":role,
    		"parentEmail":parentemail,
    		"sigupDate":signupdate,
    		"auth":"",
    		"plan":"",
    		"billingID":"",
            "disabled":False
    		}
    try:
        r = users.insert_one(user)
    except Exception as e:
        logger.error("Error while inserting user into db. "+str(e))
        return False

    return str(r.inserted_id)


def check_if_exists(collection,field,value,field2=None,value2=None):

    coll = db[collection]

    rows = []

    if field2 is None:
        rows = coll.find({field:value})
    else:
        rows = coll.find({field:value,field2:value2})



    if len(list(rows)) > 0:
        return True 
    else:
        return False



def create_auth_token(email,password):

    alphabet = string.ascii_letters + string.digits + "=!@#$%^&*<>"
    token = ''.join(secrets.choice(alphabet) for i in range(512))

    users = db["users"]
    
    user = { "password": password, "email":email }
    
    newtoken = { "$set": { "auth": token } }

    try:
        r = users.update_one(user,newtoken)
    except Exception as e:
        logger.error("Error while updating auth token into db. "+str(e))
        return None
    
    return token


def authenticate_user(token):

    users = db["users"]
    result = db.users.find_one({"auth":token})
    if result:
        return result['email']
    return None


def insert_testboard(apiName,apiType,apiEnvironment,apiHeader,
    apiHttpMethod,apiEndpoint,apiRequestBody,apiResponseBody,
    apiInputDataType,apiRequestBodyType,apiResponseBodyType,user):


    creationTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    testboards = db["testboards"]
    testboard = {
            "apiName": apiName, 
            "apiType": apiType, 
            "apiEnvironment":apiEnvironment ,
            "apiHttpMethod":apiHttpMethod ,
            "apiEndpoint":apiEndpoint ,
            "apiRequestBody":apiRequestBody ,
            "apiResponseBody":apiResponseBody ,
            "apiInputDataType":apiInputDataType ,
            "apiRequestBodyType":apiRequestBodyType ,
            "apiResponseBodyType":apiResponseBodyType ,
            "apiHeader":apiHeader,
            "apiCreationDate":creationTime,
            "apiCreator":user
            }
    try:
        r = testboards.insert_one(testboard)
    except Exception as e:
        logger.error("Error while inserting testboard into db. "+str(e))
        return False

    return str(r.inserted_id)


def update_collection(collection,id,field,value):

    coll = db[collection]
    
    query = { "_id": ObjectId(id) }
    
    entity = { "$set": { field : value } }

    try:
        r = coll.update_one(query,entity)
    except Exception as e:
        logger.error("Error while updating db. "+str(e))
        return False
    
    return True


def get_testboard(testboard_id):

    testboards = db["testboards"]
    details = db.testboards.find({"_id":ObjectId(testboard_id)})
    details = list(details)
    if len(details)>0:
        return details[0]
    return None














