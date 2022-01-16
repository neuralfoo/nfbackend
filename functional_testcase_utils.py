from loguru import logger
import traceback 
import os
import dbops 
import datetime
import global_vars as g
import pandas as pd

def add_testcase(testboardID,testcase_name,requests):


	testcaseID = dbops.insert_functional_testcase(testboardID,testcase_name,requests)

	if testcaseID == False:
		return False,"Seems like there is an error on our end, please contact support."

	return True,"Testcase added"



def import_testcases(testboardID,newfilepath):

	'''
	db collection format:
	"testboardID" : "61bcc4a36d890e964a9d647b",
	"testcaseName" : "Testing support for PDF file",
	"requests" : [
		{
			"requestBody" : "{\n  \"task\": \"indianIdCard\",\n  \"essentials\": {\n    \"files\": [\n      \"https://preproduction-persist.signzy.tech/api/files/15292311/download/fbfae9ab7d914f229119549bccf905239951af5d8d074923aa9f95c88354ffb1.pdf\"\n    ]\n  }\n}",
			"responseBody" : "{\n  \"essentials\": {\n    \"files\": [\n      \"${ignore-string}$\"\n    ]\n  },\n  \"id\": \"${ignore-string}$\",\n  \"patronId\": \"${ignore-string}$\",\n  \"task\": \"indianIdCard\",\n  \"result\": [\n    {\n      \"status\": \"successful\",\n      \"classification\": {\n        \"status\": \"success\",\n        \"idType\": \"passport\",\n        \"message\": \"Successfully completed.\"\n      }\n    }\n  ]\n}",
			"responseTime" : "0",
			"responseCode" : "201"
		}
	],


	csv format:
	name, (request body, response code, response body, response time)...repeat n requests

	'''


	try:
		testcases_df = pd.read_csv(newfilepath)
	except Exception as e:
		logger.error("Unable to read csv, invalid syntax")
		traceback.print_exc()
		return False,"Unable to read CSV"

	num_cols = len(testcases_df.columns)

	print(num_cols)

	if (num_cols - 1) % 4 != 0:

		logger.error("Unable to read csv, incorrect number of columns")
		traceback.print_exc()
		return False,"Unable to read csv, incorrect number of columns"

	testcases_numpy = testcases_df.values

	for row in testcases_numpy:

		# logger.info(row)

		if (len(row) - 1) % 4 != 0:
			logger.error("row syntax incorrect")
			continue
			
		num_requests = int((len(row)-1)/4)

		requests = []

		for i in range(num_requests):

			requests.append({
				"requestBody"  : row[(i*4)+1],
				"responseCode" : int(row[(i*4)+2]),
				"responseBody" : row[(i*4)+3],
				"responseTime" : row[(i*4)+4],
			})

		testcase_name = row[0]

		add_testcase(testboardID,testcase_name,requests)

	return True, "Successfully imported testcases!"


def get_testcases(testboardID):

	try:
		testcases_list = dbops.list_functional_testcases(testboardID)

		for i in range(len(testcases_list)):
			testcases_list[i]["key"] = i+1
			testcases_list[i]["testcaseID"] = str(testcases_list[i]["_id"]) 
			del testcases_list[i]["_id"]

			j = 1
			for r in testcases_list[i]["requests"]:
				testcases_list[i]["requestBody"+str(j)]  = r["requestBody"]
				testcases_list[i]["responseCode"+str(j)] = r["responseCode"]
				testcases_list[i]["responseBody"+str(j)] = r["responseBody"]
				testcases_list[i]["responseTime"+str(j)] = r["responseTime"]
				j+=1

			del testcases_list[i]["requests"]


		return testcases_list,"success"
	except Exception as e:
		logger.error("Error while fetching test list")
		traceback.print_exc()
		return None,"Error while fetching test list"



def delete_testcase(testcaseID):

	try:
	    delete_result = dbops.delete_functional_testcase(testcaseID)
	    return delete_result,"Deleted testcase"

	except Exception as e:
		logger.error("Error while deleting testcase")
		traceback.print_exc()
		return False,"Error while deleting testcase"	    


def edit_testcase(testcaseID,testcaseName,testcaseValues,userID):

	try:
	    edit_result = dbops.update_functional_testcase(testcaseID,testcaseName,testcaseValues,userID)
	    return edit_result,"Edited testcase"

	except Exception as e:
		logger.error("Error while editing testcase")
		traceback.print_exc()
		return False,"Error while editing testcase"	    






