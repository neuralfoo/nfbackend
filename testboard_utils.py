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
			data["apiHeader"],
	    	data["apiHttpMethod"],
	    	data["apiEndpoint"],
	    	data["apiRequestBody"],
	    	data["apiResponseBody"],
	    	data["apiInputDataType"],
	    	data["apiRequestBodyType"],
	    	data["apiResponseBodyType"],
	    	user)

		return testboard_id,"success"
	
	except Exception as e:
		logger.error(str(e))
		traceback.print_exc()
		return None,str(e)

def update_testboard(data,user):

	try:

		if dbops.check_if_exists("testboards","_id",ObjectId(data["_id"])) == False:
			message = "Testboard named '"+data["apiName"]+"' does not exist."
			logger.error(message)
			return "",message

		for d in data:

			if d == "_id":
				continue

			r = dbops.update_collection("testboards",data["_id"],d,data[d])
			if r == False:
				return None,"Unable to update entities."		

		dbops.update_collection("testboards",data["_id"],"apiLastUpdatedBy",user)	

		return data["_id"],"success"
	
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







