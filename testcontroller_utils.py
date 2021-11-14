from loguru import logger
import traceback 
import os
import dbops 
import datetime


def get_snapshot_of_testboard(testboardID):

	testboard_details = dbops.get_testboard(testboardID)

	testboard_details["testboardID"] = str(testboard_details["_id"])
	del testboard_details["_id"]


	requests = []
	for requestID in testboard_details["apiRequests"]:
		request = dbops.get_request(requestID)
		request["requestID"] = str(request["_id"])
		del request["_id"]
		requests.append(request)

	testboard_details["requests"] = requests

	return testboard_details


def imageclassification_accuracy_testcontroller(testboardID,action,creatorID,accuracyTestID=""):
	
	if action == "start":
		
		testboard_snapshot 	= get_snapshot_of_testboard(testboardID)
		start_time 			= datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
		end_time 			= None
		accuracy 			= None
		confusion_matrix 	= None
		test_status 		= "running"
		test_type 			= "imageclassification_accuracytest"
		num_test_images 	= len(dbops.get_images_for_testboard(testboardID))

		accuracyTestID = dbops.insert_imageclassification_accuracytest(
			creatorID,
			testboard_snapshot,
			start_time,end_time,num_test_images,
			test_type,test_status,accuracy,confusion_matrix)

		retval = os.system(f"pm2 start imageclassification_accuracy_test_driver.py --interpreter python3.8 --name {accuracyTestID} --no-autorestart -- {accuracyTestID}")
		# print(retval)
		return True,"Accuracy test started"

	elif action == "stop":
		retval = os.system(f"pm2 delete {accuracyTestID}")
		# print(retval)
		dbops.update_test(testID,"testStatus","stopped")

		return True,"Accuracy test stopped"


	return False,"Invalid action"


def get_imageclassification_accuracytests(testboardID):

	try:
		test_list = dbops.list_tests(testboardID,test_type="imageclassification_accuracytest")

		for i in range(len(test_list)):
			test_list[i]["key"] = i+1
			test_list[i]["testID"] = str(test_list[i]["_id"]) 
			del test_list[i]["_id"]


			if type(test_list[i]["endTime"]) == str and type(test_list[i]["startTime"]) == str:
				end_time = datetime.datetime.strptime(test_list[i]["endTime"],"%d-%m-%Y %H:%M:%S")
				start_time = datetime.datetime.strptime(test_list[i]["startTime"],"%d-%m-%Y %H:%M:%S")

				diff = end_time - start_time

				duration = datetime.timedelta(seconds=diff.total_seconds())
				test_list[i]["duration"] = str(duration)
				
			else:
				test_list[i]["endTime"] = "-"
				test_list[i]["duration"] = "-"

		return test_list,"success"
	except Exception as e:
		logger.error("Error while fetching test list")
		traceback.print_exc()
		return None,"Error while fetching test list"



def delete_test(testID):

	try:
		result = dbops.delete_test(testID)
		dbops.delete_all_api_hits(testID)	
		return result,"Test deleted"
	except Exception as e:
		logger.error("Error while deleting test.")
		traceback.print_exc()
		return False,"Unexpected error, could not delete test."



if __name__=="__main__":

	imageclassification_accuracy_testcontroller("61814c8bfd3f474d4bcc746c","start","6181345602a4b1e18cbe542f")










