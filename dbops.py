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
    		"parentemail":parentemail,
    		"signupdate":signupdate,
    		"auth":"",
    		"plan":"",
    		"billingID":""
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











