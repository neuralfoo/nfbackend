from loguru import logger
import traceback 
import os
import dbops 
import datetime
import global_vars as g
import pandas as pd 

def add_testcase(testboardID,requestVariables,responseVariables):

	testcaseID = dbops.insert_accuracy_testcase(testboardID,requestVariables,responseVariables)

	if testcaseID == False:
		return False,"Seems like there is an error on our end, please contact support."

	return True,"Testcase added"




def import_testcases(testboardID,newfilepath):

	'''
	db collection format:
	"testboardID" : "61d8ad70f9e16c9c5772661b",
	"requestVariables" : "{ \"input\" : \"http://development.persist.signzy.tech/api/files/44943/download/GN0c6f50IiKPVP0rVpgQeuWLModVuz8eCYRZWaIt4hnlPDLreo.jpg\" } ",
	"responseVariables" : "{ \"prediction\":\"aadhaar\" } ",


	csv format:
	requestVariables, responseVariables
	... n rows
	
	'''

	try:
		testcases_df = pd.read_csv(newfilepath)
	except Exception as e:
		logger.error("Unable to read csv, invalid syntax")
		traceback.print_exc()
		return False,"Unable to read CSV"

	num_cols = len(testcases_df.columns)

	logger.info(f"Num columns in CSV: {num_cols}")

	if (num_cols != 2):

		logger.error("Unable to read csv, incorrect number of columns")
		traceback.print_exc()
		return False,"Unable to read csv, incorrect number of columns"

	testcases_numpy = testcases_df.values

	for row in testcases_numpy:

		if len(row) != 2:
			logger.error("row syntax incorrect")
			continue
		
		requestVariables = row[0]
		responseVariables = row[1]

		add_testcase(testboardID,requestVariables,responseVariables)


	return True, "Successfully imported testcases!"


def get_testcases(testboardID):

	try:
		testcases_list = dbops.list_accuracy_testcases(testboardID)

		for i in range(len(testcases_list)):
			testcases_list[i]["key"] = i+1
			testcases_list[i]["testcaseID"] = str(testcases_list[i]["_id"]) 
			del testcases_list[i]["_id"]

		return testcases_list,"success"
	except Exception as e:
		logger.error("Error while fetching test list")
		traceback.print_exc()
		return None,"Error while fetching test list"



def delete_testcase(testcaseID):

	try:
	    delete_result = dbops.delete_accuracy_testcase(testcaseID)
	    return delete_result,"Deleted testcase"

	except Exception as e:
		logger.error("Error while deleting testcase")
		traceback.print_exc()
		return False,"Error while deleting testcase"	    


def edit_testcase(testcaseID,responseVariables,requestVariables,userID):

	try:
	    edit_result = dbops.update_accuracy_testcase(testcaseID,responseVariables,requestVariables,userID)
	    return edit_result,"Edited testcase"

	except Exception as e:
		logger.error("Error while editing testcase")
		traceback.print_exc()
		return False,"Error while editing testcase"	    






