from loguru import logger
import traceback 
import os
import dbops 
import datetime
import global_vars as g
import utils



def functional_test_action(testboardID,action,creatorID,testID=""):
	
	if action == "start":
		
		testboard_snapshot 	= utils.get_snapshot_of_testboard(testboardID)
		start_time 			= datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
		end_time 			= None
		# accuracy 			= None
		# confusion_matrix 	= None
		passed_cases_count	= None
		failed_cases_count	= None
		total_cases_count	= len(dbops.list_testcases(testboardID))
		fail_reasons 		= None
		test_status 		= "running"
		test_type 			= "functionaltest"

		testID = dbops.insert_functionaltest(
			creatorID,
			testboard_snapshot,
			start_time,end_time,
			total_cases_count,passed_cases_count,failed_cases_count,
			fail_reasons,test_type,test_status)

		retval = os.system(f"pm2 start functionaltest_driver.py --interpreter python3.7 --name {testID} --no-autorestart -- {testID}")
		# print(retval)
		return True,"Functional test started"

	elif action == "stop":
		retval = os.system(f"pm2 delete {testID}")
		# print(retval)
		dbops.update_test(testID,"testStatus","stopped")

		return True,"Functional test stopped"


	return False,"Invalid action"




