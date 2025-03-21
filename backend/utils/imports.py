from flask import Flask, jsonify, request
from utils.models import *
from utils import commons
from sqlalchemy import or_
from flask_restful import Api
from utils import routes
from flask_jwt_extended import JWTManager, create_access_token