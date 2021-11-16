import dbops 
from loguru import logger
import traceback 
from bson.objectid import ObjectId
import utils
import global_vars as g 
import fs_utils
import json
import requests
from requests_toolbelt import MultipartEncoder
import re
import os
import time

def extract_requests_from_testboard(testboard_details):

	request_list = []

	for request_details in testboard_details["requests"]:
		
		response_variable_dict = {}
		response_json = json.loads(request_details["apiResponseBody"])


		'''
		Add for RawText and Form data
		'''

		if request_details["apiResponseBodyType"] == "json":
			response_variable_dict = parse_json_template(response_variable_dict,[],response_json)
			# print("output variables:",response_variable_dict)
			# exit()

		request_list.append({
			"method":request_details["apiHttpMethod"],
			"endpoint":request_details["apiEndpoint"],
			"requestBody":request_details["apiRequestBody"],
			"responseBody":response_variable_dict,
			"inputDataType":request_details["apiInputDataType"],
			"requestBodyType":request_details["apiRequestBodyType"],
			"responseBodyType":request_details["apiResponseBodyType"],
			"headers":request_details["apiHeader"]})


	return request_list



def convert_headers_to_dict(headers):

	d = {}
	for row in headers:
		d[row[0]] = row[1]

	return d



def parse_json_template(template_dict,template_path,template_object):

	# print(template_dict,template_path,template_object)

	if type(template_object) == dict:

		for key in template_object:

			if type(template_object[key]) == str:

				m = re.findall("\${.*}\$",template_object[key])

				if m:
					variable_name = m[0][2:-2]
					template_dict[variable_name] = template_path + [["key",key]]

			elif type(template_object[key]) == dict or type(template_object[key]) == list:
				
				new_dict = parse_json_template(template_dict,template_path+ [["key",key]],template_object[key])
				template_dict = {**template_dict, **new_dict}

	elif type(template_object) == list:

		for index,item in enumerate(template_object):

			if type(item) == str:

				m = re.findall("\${.*}\$",item)

				if m:
					variable_name = m[0][2:-2]
					template_dict[variable_name] = template_path + [["index",index]]

			elif type(item) == dict or type(item) == list:
				
				new_dict = parse_json_template(template_dict,template_path+ [["index",index]],template_object[index])
				template_dict = {**template_dict, **new_dict}

	return template_dict


def extract_variables_from_response(template_dictionary,response):

	variable_dict = {}

	for key in template_dictionary:

		# print("extracting for",key)

		var = response

		for path in template_dictionary[key]:

			if path[0] == "key":
				var = var[path[1]]

			elif path[0] == "index":
				var = var[path[1]]

		variable_dict[key] = var

	# print(variable_dict)

	return variable_dict

def place_variables_in_request_json(request_string,variables):

	'''
		variables is a dict 
		variables["input"] = value of input
		
	'''
	# print(variables)
	for v in variables:
		m = "${"+v+"}$" in request_string
		if m:
			request_string = re.sub("\${"+v+"}\$",variables[v],request_string)

	return json.loads(request_string)


def api_runner(imageID,request_list):

	input_image_data = dbops.get_image_details(imageID)


	gt = input_image_data["annotation"]

	filename = input_image_data["filename"]

	if type(gt) != str:

		final_output = {
			"imageID":imageID,
			"filename":filename,
			"groundTruth":gt,
			"prediction":None,
			"result":False,
			"response":None,
			"imageUrl":f"/app/fs/image/{imageID}/{filename}",
			"confidence":None
		}
		return final_output

	global_variables_dict = {}

	input_image_url = input_image_data["imageUrl"]

	global_variables_dict["input"] = input_image_url

	total_response_time = 0.0

	individual_response_times = []

	request_outputs = {}

	i = 1
	for r in request_list:

		headers = convert_headers_to_dict(r["headers"])

		response  = None

		if r["inputDataType"] == "url":

			input_data = None
			if r["requestBodyType"] == "json":
				input_data = place_variables_in_request_json(r["requestBody"],global_variables_dict)


				start_time = time.monotonic()

				response = requests.request(method=r["method"],
					url=r["endpoint"],
					json=input_data,
					headers=headers
					)

				end_time = time.monotonic()

				diff = round(end_time-start_time,3)
				total_response_time += diff
				individual_response_times.append(diff)


		if r["inputDataType"] == "file":

			downloaded_file = fs_utils.download_from_fs(input_image_url)
			file_name = input_image_url.split("/")[-1]

			with open(downloaded_file, 'rb') as binary_data:
				multipart_data = MultipartEncoder(
		            fields={
		                # a file upload field
		                'file': (file_name, binary_data, input_image_data["fileType"])
		            }
		        )

				headers['Content-Type'] = multipart_data.content_type

				start_time = time.monotonic()

				response = requests.request(method=r["method"],url=r["endpoint"], data=multipart_data,
                                 headers=headers)

				end_time = time.monotonic()

				diff = round(end_time-start_time,3)
				total_response_time += diff
				individual_response_times.append(diff)

				os.remove(downloaded_file)

		if r["responseBodyType"] == "json":

			# print(response.json())

			try:
				output_dict = extract_variables_from_response(r["responseBody"],response.json())
				global_variables_dict = {**global_variables_dict, **output_dict}
			except Exception as e:

				logger.error(e)
				traceback.print_exc()

			request_outputs["request"+str(i)] = response.json()


		i+=1

	prediction = None

	if "prediction" in global_variables_dict:
		# if global_variables_dict["prediction"] == input_image_data["annotation"]:
		prediction = global_variables_dict["prediction"]


	confidence = "-"

	if "confidence" in global_variables_dict:
		confidence = round(float(global_variables_dict["confidence"]),2)


	final_output = {
		"imageID":imageID,
		"filename":filename,
		"groundTruth":gt,
		"prediction":prediction,
		"result":prediction==gt,
		"response":request_outputs,
		"imageUrl":f"/app/fs/image/{imageID}/{filename}",
		"confidence":confidence,
		"totalResponseTime":total_response_time,
		"requestResponseTimes":individual_response_times
	}

	# print("global_variables_dict:",global_variables_dict)
	# print(final_output)

	return final_output





# if __name__=="__main__":

# 	request_list = extract_requests_from_testboard(testboardID="61814c8bfd3f474d4bcc746c")
# 	api_runner("61880e6dbd16d9ea5d14fc2d",request_list)


