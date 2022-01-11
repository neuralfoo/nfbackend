from loguru import logger
import traceback 
import os
import dbops 
import datetime
import global_vars as g
import utils



def functional_test_action(testboardID,action,authcode,testID=""):
	

	if action == "start":
		
		response_code = utils.hit_start_test_api(testboardID,"functionaltest",authcode)

		if response_code == 200:
			return True,"Functional test started"
		else:
			return False,"Error: unable to start test"

	elif action == "stop":

		response_code = utils.hit_stop_test_api(testboardID,testID,authcode)

		if response_code == 200:
			return True,"Functional test stopped"
		else:
			return False,"Error: unable to stop test"


	return False,"Invalid action"



def list_functional_tests(testboardID):

	try:
		test_list = dbops.list_tests(testboardID,test_type="functionaltest")
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



def get_functional_test_details(testID,testboardID):

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



