import dbops 
from loguru import logger
import traceback 
from bson.objectid import ObjectId
import utils
import global_vars as g 

def create_testboard(data,userID,organizationID):

	try:

		if dbops.check_if_exists("testboards","apiName",data["apiName"]):
			message = "Testboard named '"+data["apiName"]+"' already exists."
			logger.error(message)
			return "",message

		testboard_id = dbops.insert_testboard(
			data["apiName"],
			data["apiType"],
			data["apiEnvironment"],
			data["visibility"],
	    	userID,
			organizationID
	    )

		for r in data["apiRequests"]:
			request_id = dbops.insert_request(
				testboard_id ,
				r["apiHeader"] ,
		    	r["apiHttpMethod"] ,
		    	r["apiEndpoint"] ,
		    	r["apiRequestBody"] ,
		    	r["apiResponseBody"] ,
		    	r["apiInputDataType"] ,
		    	r["apiRequestBodyType"] ,
		    	r["apiResponseBodyType"]
			)

			dbops.push_request_in_testboard(testboard_id,request_id)

		return testboard_id,"success"
	
	except Exception as e:
		logger.error(str(e))
		traceback.print_exc()
		return None,str(e)




def update_testboard(data,userID):

	try:

		testboardID = data["testboardID"]

		if dbops.check_if_exists("testboards","_id",ObjectId(testboardID)) == False:
			message = "Testboard with ID '"+testboardID+"' does not exist."
			logger.error(message)
			return "",message

		for d in data:
			if d in ["apiName","apiType","apiEnvironment"]:
				r = dbops.update_collection("testboards",testboardID,d,data[d])
				if r == False:
					return None,"Unable to update entities"		

		ownership,msg = utils.check_ownership("testboards",ObjectId(testboardID),userID)

		if ownership:
			r = dbops.update_collection("testboards",testboardID,"visibility",data["visibility"])
			if r == False:
				return None,"Unable to update visibility"


		cleared = dbops.clear_all_requests(testboardID)

		if not cleared:
			return None, "Unable to remove existing requests"


		r = dbops.update_collection("testboards",testboardID,"apiRequests",[])
		if r == False:
			return None,"Unable to update apiRequests"

		for request in data["apiRequests"]:

			request_id = dbops.insert_request(
				testboardID ,
				request["apiHeader"] ,
		    	request["apiHttpMethod"] ,
		    	request["apiEndpoint"] ,
		    	request["apiRequestBody"] ,
		    	request["apiResponseBody"] ,
		    	request["apiInputDataType"] ,
		    	request["apiRequestBodyType"] ,
		    	request["apiResponseBodyType"]
			)

			dbops.push_request_in_testboard(testboardID,request_id)

			# else:
			# 	for keyname in request:
			# 		if keyname == "requestID":
			# 			continue
			# 		dbops.update_collection("requests",request["requestID"],keyname,request[keyname])	

		dbops.update_collection("testboards",testboardID,"apiLastUpdatedBy",userID)	

		return testboardID,"success"
	
	except Exception as e:
		logger.error(str(e))
		traceback.print_exc()
		return None,str(e)




def get_testboard(testboard_id):

	try:
		testboard_details = dbops.get_testboard(testboard_id)

		if testboard_details is None:
			return None,"testboard not found"

		testboard_details["testboardID"] = str(testboard_details["_id"])
		del testboard_details["_id"]

		api_requests = []
		for reqID in testboard_details["apiRequests"]:
			req_data = dbops.get_request(reqID)
			req_data["requestID"] = str(req_data["_id"])
			del req_data["_id"]
			api_requests.append(req_data)


		testboard_details["apiRequests"] = api_requests

		return testboard_details,"success"
	
	except Exception as e:
		logger.error(str(e))
		traceback.print_exc()
		return None,str(e)




def list_testboard(userID,organizationID):

	try:
		testboard_list = dbops.list_testboards(userID,organizationID)

		for i in range(len(testboard_list)):
			testboard_list[i]["testboardID"] = str(testboard_list[i]["_id"])
			del testboard_list[i]["_id"]
			testboard_list[i]["key"] = i+1
			testboard_list[i]["apiType"] = g.api_named_types[testboard_list[i]["apiType"]]

			creator = dbops.fetch_user_details(testboard_list[i]["creatorID"])
			if creator is not None:
				testboard_list[i]["creator"] = creator["firstName"]				

		return testboard_list,"success"
	
	except Exception as e:
		logger.error(str(e))
		traceback.print_exc()
		return None,str(e)








