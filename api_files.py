from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, render_template, redirect, request, make_response, session, abort, Blueprint, jsonify
from api_resources import File, Files


app = Flask(__name__)
api = Api(app)

api.add_resource(Files, '/api/users')
api.add_resource(File, '/api/users/<int:news_id>')
