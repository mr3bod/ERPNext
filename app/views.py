from flask import redirect, request, jsonify, json
from app import app, db, oidc
from .models import Event, Token, Get_token
import requests, datetime
from datetime import timedelta
from .tasks import json_responds



@app.route('/')
def index():
    return 'Not logged in'


@app.route('/event', methods=['POST'])
def event():

    event = request.json

    #if event['id'] == '1':

        #return ('', 200)

    #u = Event(id = event['id'] , status="pinding", body= json.dumps(event))
    #db.session.add(u)
    #db.session.commit()

    token = Get_token()

    json_responds.apply_async((event, token), countdown=5)

    return '', 200
