from loguru import logger
import traceback 
import os
import dbops 
import datetime


def webhook_save_request(testboardID,testType,data,method):

	try:
		timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
		
		testboard = dbops.get_testboard(testboardID)

		if testboard is not None:
			hitID = dbops.insert_webhook_hit(testboardID,testType,data,method,timestamp)
			return hitID,"success"

		logger.error("testboardID is invalid")
		return None,"webhook error"
	
	except Exception as e:

		logger.error(e)
		traceback.print_exc()
		return None,"webhook error"