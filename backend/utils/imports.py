import os
# check if project initialized
if not os.path.exists('data/data.db'):
    print("Project not initialized\nRun init.py first\n\n")
    exit(0)

from flask import Flask, request, send_file
from utils.models import *
from utils import commons
from sqlalchemy import or_, event
from flask_restful import Api
from utils import routes
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from utils.http_response import Response
from utils.tasks import mail