from loguru import logger
import traceback 
import os
import dbops 
import datetime
import global_vars as g

def add_testcase(testboardID,testcase_name,requests,userID):


	testcaseID = dbops.insert_functional_testcase(testboardID,testcase_name,requests,userID)

	if testcaseID == False:
		return False,"Seems like there is an error on our end, please contact support."

	return True,"Testcase added"
