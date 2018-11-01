from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import *
import pymysql
import os

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:xiaoxin@127.0.0.1:3306/movie"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)



from app.home.views import bp as home_bp
from app.admin.views import bp as admin_bp

app.register_blueprint(home_bp)
app.register_blueprint(admin_bp)


