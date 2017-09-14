import os
from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from flask.ext.oidc import OpenIDConnect
from flask_oidc.discovery import discover_OP_information
from config import basedir
from celery import Celery


app = Flask(__name__)
data = discover_OP_information('https://staging-sso.stcs.com.sa')
data = {"web":data}
data["web"].update({"auth_uri": "https://test/auth",
                    "client_id": "MyClient",
                    "client_secret": "MySecret",
                    "redirect_uris": ["http://localhost:5000/oauth2callback"],
                    "token_uri": "https://test/token",
                    })

with open('client_secrets.json', 'w') as f:
     json.dump(data, f)

app.config.from_object('config')
db = SQLAlchemy(app)
oidc = OpenIDConnect(app, os.path.join(basedir, 'tmp'))

celery = Celery(app, backend='redis://', broker='redis://localhost:6379/0', include=['app.tasks'])



from app import views, models
