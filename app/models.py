from app import db
from flask import json
import datetime, requests


class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False

class Event(db.Model):
    id = db.Column(db.String(28), primary_key = True)
    status = db.Column(db.String(28))
    body = db.Column(db.String(10000))

class Token(db.Model):
    id = db.Column(db.String(28), primary_key = True)
    expires_in = db.Column(db.DateTime)
    body = db.Column(db.String(10000))

def send_request():
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    url='https://staging-sso.stcs.com.sa/token'
    token = requests.post(url, data={'client_id':'052c6a54-023e-4423-afdb-9b44dae8fc00',
            'client_secret':'APiXVlkqqzTYJK2lJl44zKvhUM0Fux9CjsSQV2sC-f8hBRt-VqWBn3wMWc_fbbBngyoydgP2a0l7YFUcmFr8I7I',
            'grant_type':'client_credentials'}, headers=headers)

    token = token.json()
    expire_in = datetime.datetime.now() + datetime.timedelta(token['expires_in'])

    Token.query.delete()

    u = Token(id = token['access_token'] , expires_in= expire_in, body= json.dumps(token))
    db.session.add(u)
    db.session.commit()

    print "new token is created"
    return token


def Get_token():
    now = datetime.datetime.now()
    tokens = Token.query.all()

    if tokens == []:
        token = send_request()

    else:
        for t in tokens:
            if now > t.expires_in:
                print "token is refreshed"
                token = send_request()

            else:
                print "using old token"
                token = json.loads(t.body)

    print "sending"
    #print token
    return token
