import dbops 
from loguru import logger
import traceback 
from bson.objectid import ObjectId

def create_testboard(data,user):

	try:

		if dbops.check_if_exists("testboards","apiName",data["apiName"]):
			message = "Testboard named '"+data["apiName"]+"' already exists."
			logger.error(message)
			return "",message

		testboard_id = dbops.insert_testboard(
			data["apiName"],
			data["apiType"],
			data["apiEnvironment"],
	    	user
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

def update_testboard(data,user):

	try:

		if dbops.check_if_exists("testboards","_id",ObjectId(data["testboardID"])) == False:
			message = "Testboard named '"+data["apiName"]+"' does not exist."
			logger.error(message)
			return "",message

		for d in data:

			if d == "testboardID":
				continue

			if d in ["apiName","apiType","apiEnvironment"]:

				r = dbops.update_collection("testboards",data["testboardID"],d,data[d])

				if r == False:
					return None,"Unable to update entities."		


		for request in data["apiRequests"]:

			if "requestID" not in request:

				request_id = dbops.insert_request(
					data["testboardID"] ,
					request["apiHeader"] ,
			    	request["apiHttpMethod"] ,
			    	request["apiEndpoint"] ,
			    	request["apiRequestBody"] ,
			    	request["apiResponseBody"] ,
			    	request["apiInputDataType"] ,
			    	request["apiRequestBodyType"] ,
			    	request["apiResponseBodyType"]
				)
				
				dbops.push_request_in_testboard(data["testboardID"],request_id)

			
			else:
				for keyname in request:
					if keyname == "requestID":
						continue

					dbops.update_collection("requests",request["requestID"],keyname,request[keyname])	

		dbops.update_collection("testboards",data["testboardID"],"apiLastUpdatedBy",user)	

		return data["testboardID"],"success"
	
	except Exception as e:
		logger.error(str(e))
		traceback.print_exc()
		return None,str(e)




def get_testboard(testboard_id):

	try:
		testboard_details = dbops.get_testboard(testboard_id)

		if testboard_details is not None:

			testboard_details["_id"] = str(testboard_details["_id"])

		return testboard_details,"success"
	
	except Exception as e:
		logger.error(str(e))
		traceback.print_exc()
		return None,str(e)




def list_testboard():

	try:
		testboard_details = dbops.fetch_item("testboards")

		if testboard_details is not None:

			testboard_details["_id"] = str(testboard_details["_id"])

		return testboard_details,"success"
	
	except Exception as e:
		logger.error(str(e))
		traceback.print_exc()
		return None,str(e)








