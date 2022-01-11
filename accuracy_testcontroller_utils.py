import os
import utils
import dbops 
import json
import datetime
import machines
import requests
import traceback 
import global_vars as g
from loguru import logger


def accuracy_testcontroller(testboardID,action,creatorID,authcode,accuracyTestID=""):
	
	if action == "start":
		
		response_code = utils.hit_start_test_api(testboardID,"accuracytest",authcode)

		if response_code == 200:
			return True,"Accuracy test started"
		else:
			return False,"Error: unable to start test"

	elif action == "stop":

		response_code = utils.hit_stop_test_api(accuracyTestID,authcode)

		if response_code == 200:
			return True,"Accuracy test stopped"
		else:
			return False,"Error: unable to stop test"

	return False,"Invalid action"


def accuracy_testcontroller_list(testboardID):

	try:
		test_list = dbops.list_tests(testboardID,test_type="accuracytest")
		test_list.reverse()

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





def accuracy_testcontroller_details(testID,testboardID):

	try:
		test_details = dbops.get_test(testID)

		if test_details["testboard"]["testboardID"] != testboardID:
			return None,"Invalid request"

		test_details["testID"] = str(test_details["_id"]) 
		del test_details["_id"]

		test_details["testboard"]["apiTypeName"] = g.api_named_types[test_details["testboard"]["apiType"]]

		if type(test_details["endTime"]) == str and type(test_details["startTime"]) == str:
			end_time = datetime.datetime.strptime(test_details["endTime"],"%d-%m-%Y %H:%M:%S")
			start_time = datetime.datetime.strptime(test_details["startTime"],"%d-%m-%Y %H:%M:%S")

			diff = end_time - start_time

			duration = datetime.timedelta(seconds=diff.total_seconds())
			test_details["duration"] = str(duration)
			
		else:
			test_details["endTime"] = "-"
			test_details["duration"] = "-"


		# test_details["testboard"]["apiEnvironment"] = "preproduction"

		return test_details,"success"

	except Exception as e:
		logger.error("Error while fetching test details")
		traceback.print_exc()
		return None,"Error while fetching test details"





# if __name__=="__main__":
# 	imageclassification_accuracy_testcontroller("61814c8bfd3f474d4bcc746c","start","6181345602a4b1e18cbe542f")
