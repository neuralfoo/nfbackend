from flask import Flask
from flask_cors import CORS

import fs 
import auth 
import user
import webhook
import testboard
import organization
import common_endpoints
import accuracy_testcase
import functional_testcase
import accuracy_testcontroller 
import functional_testcontroller
import imageclassification_testcontroller

app = Flask(__name__)

CORS(app)

app.register_blueprint(fs.profile)
app.register_blueprint(auth.profile)
app.register_blueprint(user.profile)
app.register_blueprint(webhook.profile)
app.register_blueprint(testboard.profile)
app.register_blueprint(organization.profile)
app.register_blueprint(common_endpoints.profile)
app.register_blueprint(accuracy_testcase.profile)
app.register_blueprint(functional_testcase.profile)
app.register_blueprint(accuracy_testcontroller.profile)
app.register_blueprint(functional_testcontroller.profile)
app.register_blueprint(imageclassification_testcontroller.profile)

