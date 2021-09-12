from flask import Flask

import auth

app = Flask(__name__)

app.register_blueprint(auth.profile)

















