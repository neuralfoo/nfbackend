from flask import Flask

from flask_cors import CORS

import auth
import testboard 
import user 
import organization
import fs 

app = Flask(__name__)

CORS(app)

app.register_blueprint(auth.profile)
app.register_blueprint(testboard.profile)
app.register_blueprint(user.profile)
app.register_blueprint(organization.profile)
app.register_blueprint(fs.profile)

















