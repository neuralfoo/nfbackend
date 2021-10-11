from flask import Flask

from flask_cors import CORS

import auth
import testboard 

app = Flask(__name__)

CORS(app)

app.register_blueprint(auth.profile)
app.register_blueprint(testboard.profile)

















