import os

# 3rd party modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# create and configure app with db
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'qbank.db')
app.secret_key = 'thisismysecretkey'
secretKey = app.secret_key
db = SQLAlchemy(app)
ma = Marshmallow(app)



# register controller routes
from qbank.apis.viewer import viewer
from qbank.apis.author import author
from qbank.apis.application import application
from qbank.apis.login import login

app.register_blueprint(viewer, url_prefix='/')
app.register_blueprint(author, url_prefix='/')
app.register_blueprint(application, url_prefix='/')
app.register_blueprint(login, url_prefix='/')