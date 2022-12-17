from flask import Flask
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
# from flask_login import LoginManager

app = Flask(__name__)   

from app import routes