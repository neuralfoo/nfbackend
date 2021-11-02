import pymongo
import string
import secrets
import datetime 
from loguru import logger
from bson.objectid import ObjectId


myclient = pymongo.MongoClient("mongodb://localhost:27017/")

db = myclient["neuralfoo"]

'''
db.users.createIndex( { "email": 1 }, { unique: true } )
db.tokens.createIndex( { "token": 1 }, { unique: true } )
'''

def insert_user(firstName,lastName,email,password,signupdate,organization,role="",parentemail=""):

    try:
        organizationID = insert_organization(organization)

        users = db["users"]
        user = {
        		"firstName": firstName,
                "lastName": lastName, 
        		"email":email, 
        		"password": password,
        		"role":role,
        		"parentEmail":parentemail,
                "organizationID":organizationID,
        		"signupDate":signupdate,
                "disabled":False
        		}
        
        r = users.insert_one(user)
        insert_plan(userID = str(r.inserted_id),plan = "free",billingID = "",billingDate = signupdate,amount = "0")
        insert_token(userID = str(r.inserted_id),token = "")

    except Exception as e:
        logger.error("Error while inserting user into db "+str(e))
        return False

    return str(r.inserted_id)

def insert_plan(userID,plan,billingID,billingDate,amount):

    billings = db["billings"]
    bill = {
            "userID":userID,
            "plan":plan,
            "billingID":billingID,
            "billingDate":billingDate,
            "amount":amount
            }
    try:
        r = billings.insert_one(bill)
    except Exception as e:
        logger.error("Error while inserting plan into db "+str(e))
        return False

    return str(r.inserted_id)


def insert_organization(organization):

    coll = db["organizations"]
    doc = {
            "organization":organization
    }
    try:
        r = coll.insert_one(doc)
    except Exception as e:
        logger.error("Error while inserting plan into db "+str(e))
        return False

    return str(r.inserted_id)

def insert_token(userID,token):

    try:
        collection = db["tokens"]
        doc = {
                "userID":userID,
                "token":token
            }

    
        r = collection.insert_one(doc)
    except Exception as e:
        logger.error("Error while inserting auth token into db "+str(e))
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


    try:

        salt = secrets.choice(["#$%^&*<>","=!@#&*<>","=!@$%^>"])
        alphabet = string.ascii_letters + string.digits + salt
        token = ''.join(secrets.choice(alphabet) for i in range(1024))

        while ( check_if_exists("tokens","token",token) ):

            salt = secrets.choice(["#$%^&*<>","=!@#&*<>","=!@$%^>"])
            alphabet = string.ascii_letters + string.digits + salt
            token = ''.join(secrets.choice(alphabet) for i in range(1024))


        users = db["users"]
        user = { "password": password, "email":email }

        tokens = db["tokens"]
        newtoken = { "$set": { "token": token } }

        u = users.find_one(user,{"_id"})
        r = tokens.update_one({"userID":str(u["_id"])},newtoken)

    except Exception as e:
        logger.error("Error while updating auth token into db "+str(e))
        return None
    
    return token

def get_organization(userID):

    users = db["users"]
    result = users.find_one({"_id":ObjectId(userID)})
    if result:
        return result['organizationID']
    return None    


def authenticate_user(token):

    tokens = db["tokens"]
    result = tokens.find_one({"token":token})
    if result:
        return result['userID']
    return None

def validate_token(token):

    tokens = db["tokens"]
    t = tokens.find_one({"token":token})
    if t:
        return True
    return False

def insert_testboard(apiName,apiType,apiEnvironment,visibility,userID,organizationID):

    creationTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    testboards = db["testboards"]
    testboard = {
            "apiName": apiName, 
            "apiType": apiType, 
            "apiEnvironment":apiEnvironment,
            "apiCreationDate":creationTime,
            "apiCreationDate":creationTime,
            "apiStatus":"ready",
            "apiLastRunOn":"-",
            "apiRequests":[],
            "creatorID":userID,
            "organizationID":organizationID,
            "collaboratorIDs":[userID],
            "apiLastUpdatedBy":userID,
            "visibility":visibility
            }
    try:
        r = testboards.insert_one(testboard)
    except Exception as e:
        logger.error("Error while inserting testboard into db "+str(e))
        return False

    return str(r.inserted_id)



def insert_request(testboardID,apiHeader,apiHttpMethod,apiEndpoint,apiRequestBody,
    apiResponseBody,apiInputDataType,apiRequestBodyType,apiResponseBodyType):


    creationTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    requests = db["requests"]
    request = {
            "testboardID":testboardID ,
            "apiHttpMethod":apiHttpMethod ,
            "apiEndpoint":apiEndpoint ,
            "apiRequestBody":apiRequestBody ,
            "apiResponseBody":apiResponseBody ,
            "apiInputDataType":apiInputDataType ,
            "apiRequestBodyType":apiRequestBodyType ,
            "apiResponseBodyType":apiResponseBodyType ,
            "apiHeader":apiHeader
            }
    try:
        r = requests.insert_one(request)
    except Exception as e:
        logger.error("Error while inserting request into db "+str(e))
        return False

    return str(r.inserted_id)


def push_request_in_testboard(testboardID,requestID):

    coll = db["testboards"]
    
    query = { "_id": ObjectId(testboardID) }
    
    entity = { "$push": { "apiRequests" : requestID } }

    try:
        r = coll.update(query,entity)
    except Exception as e:
        logger.error("Error while pushing request into testboard collection. "+str(e))
        return False
    
    return True



def clear_all_requests(testboardID):

    try:
        requests = db["requests"]
        requests.delete_many({"testboardID":testboardID})
        return True

    except Exception as e:
        logger.error("Error while deleting requests related to testboard. "+str(e))
        traceback.print_exc()
        return False


def update_collection(collection,id,field,value):

    coll = db[collection]
    
    query = { "_id": ObjectId(id) }
    
    entity = { "$set": { field : value } }

    try:
        r = coll.update_one(query,entity)
    except Exception as e:
        logger.error("Error while updating db "+str(e))
        return False
    
    return True


def get_testboard(testboardID):

    testboards = db["testboards"]
    details = testboards.find({"_id":ObjectId(testboardID)})
    details = list(details)
    if len(details)>0:
        return details[0]

    logger.error("db find returned no results")
    return None

def get_request(requestID):

    requests = db["requests"]
    details = requests.find({"_id":ObjectId(requestID)})
    details = list(details)
    if len(details)>0:
        return details[0]
    logger.error("db find returned no results")
    return None

def list_testboards(userID,organizationID):

    '''
    List all testboards such that userID is either in collaboratorIDs 
    or belong to the organizationID and are pulic
    '''

    testboards = db["testboards"]
    
    results = testboards.find({
        "$or":[
            {
                "collaboratorIDs":{ 
                    "$in" : [userID] 
                }
            },
            {
                "organizationID":organizationID,
                "visibility":"public"
            }
        ]
    })

    return list(results)
    


def fetch_item(collection,field=None,value=None):

    coll = db[collection]
    rows = []

    if field is None:
        rows = coll.find({})
    else:
        rows = coll.find({field:value})

    return list(rows)



def fetch_item_with_projection(collection,projection,field=None,value=None):

    coll = db[collection]

    if field is None:
        rows = coll.find({},projection)
    else:
        rows = coll.find({field:value},projection)

    return list(rows)







