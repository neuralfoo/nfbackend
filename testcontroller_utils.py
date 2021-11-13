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

		accuracyTestID = dbops.insert_imageclassification_accuracytest(
			creatorID,
			testboard_snapshot,
			start_time,end_time,
			test_type,test_status,accuracy,confusion_matrix)

		retval = os.system(f"pm2 start imageclassification_accuracy_test_driver.py --interpreter python3.8 --name {accuracyTestID} --no-autorestart -- {accuracyTestID}")
		# print(retval)
		return True,"Accuracy test started"

	elif action == "stop":
		retval = os.system(f"pm2 delete {accuracyTestID}")
		# print(retval)
		return True,"Accuracy test stopped"


	return False,"Invalid action"



if __name__=="__main__":

	imageclassification_accuracy_testcontroller("61814c8bfd3f474d4bcc746c","start","6181345602a4b1e18cbe542f")










