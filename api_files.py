from flask import Flask
from flask_restful import Api

from api_resources import Userget, Userlist

app = Flask(__name__)
api = Api(app)

api.add_resource(Userlist, '/api/users')
api.add_resource(Userget, '/api/users/<int:news_id>')
