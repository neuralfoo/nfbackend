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
		
		testboard_snapshot 	= utils.get_snapshot_of_testboard(testboardID)
		start_time 			= datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
		end_time 			= None
		average_accuracy 	= None
		all_accuracy		= None
		test_status 		= "running"
		test_type 			= "accuracytest"
		num_test_cases 		= len(dbops.list_accuracy_testcases(testboardID))
		machineid 			= os.environ['MACHINE_ID']
		remarks 			= ""
		passed_cases_count 	= 0
		failed_cases_count 	= 0

		accuracyTestID = dbops.insert_accuracytest(
			creatorID,testboard_snapshot,
			start_time,end_time,
			num_test_cases,test_type,test_status,
			average_accuracy,all_accuracy,
			passed_cases_count,failed_cases_count
			machineid,remarks)

		retval = os.system(f"pm2 start accuracytest_driver.py --interpreter python3.8 --name {accuracyTestID} --no-autorestart -- {accuracyTestID}")
		# print(retval)
		return True,"Accuracy test started"

	elif action == "stop":

		response_code = utils.hit_stop_test_api(accuracyTestID,authcode)

		if response_code == 200:
			return True,"Accuracy test stopped"
		else:
			return True,"Error: unable to stop test"

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





def get_imageclassification_accuracytest_details(testID,testboardID):

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
