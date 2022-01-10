from loguru import logger
import traceback 
import os
import dbops 
import datetime
import global_vars as g
import utils


def delete_test(testID):

	try:
		result = dbops.delete_test(testID)
		dbops.delete_all_api_hits(testID)	
		return result,"Test deleted"
	except Exception as e:
		logger.error("Error while deleting test.")
		traceback.print_exc()
		return False,"Unexpected error, could not delete test."

def list_api_hits(testID,testboardID):

	try:
		test_details = dbops.get_test(testID)

		if test_details["testboard"]["testboardID"] != testboardID:
			return None,"Invalid request"

		hit_list = dbops.list_all_hits(testID)

		for i in range(len(hit_list)):
			hit_list[i]["key"] = i+1
			hit_list[i]["hitID"] = str(hit_list[i]["_id"]) 
			del hit_list[i]["_id"]

			hit_list[i]["totalResponseTime"] = str(hit_list[i]["totalResponseTime"])+"s"

		return hit_list,"success"

	except Exception as e:
		logger.error("Error while fetching test details")
		traceback.print_exc()
		return None,"Error while fetching test details"

def stop_test(testID):
	
	try:
		retval = os.system(f"pm2 delete {testID}")
		# print(retval)
		dbops.update_test(testID,"testStatus","stopped")

		return True,"Accuracy test stopped"

	except Exception as e:
		logger.error("Error while stopping test")
		traceback.print_exc()
		return False,"Error while stopping test"	