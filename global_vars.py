api_types = ["imageclassification","imagesegmentation","objectdetection","generalapi","aimlapi"]
api_environments = ["development","staging","preproduction","production"]
api_methods = ["GET","POST","PUT","DELETE"]
api_input_data_types = ["url","file","base64","none"]
api_request_body_type = ["json","formData","binary","none"]
api_response_body_type = ["json","rawText"]
api_visibility = ["public","private"]
api_named_types = {
	"imageclassification":"Image Classification",
	"imagesegmentation":"Image Segmentation",
	"objectdetection":"Object Detection",
	"generalapi":"General API",
	"aimlapi":"AI/ML API"
}
testcontroller_actions = ["start","stop"]



stop_test_url = "/app/testcontroller/test/stop"