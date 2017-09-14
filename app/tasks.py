from flask import redirect, request, jsonify, json
from app import app, celery
from celery import Celery
from .models import switch
from apps.commands.commands import cmd
import requests

domain = ".domain"

@celery.task
def json_responds(event, token):
    with app.app_context():

        def send_result(status, ref_number, message= " ", landing_page_url= "http://95.177.140.114:8080/", management_page_url= "http://95.177.140.114:8080/"):
            respones = {
                       "status": status,
                       "message": message,
                       "ref_number": ref_number,
                       "landing_page_url": landing_page_url,
                       "management_page_url": management_page_url
                       }
            event_id = event['id']
            #print event_id
            #print token['access_token']
            # event_id = 'f46aa78d-1bcb-46cd-8178-53a60a3c55c8'
            headers = {'Authorization': 'Bearer '+token['access_token'], "Content-Type": "application/json"}
            url='https://staging-marketplace.stcs.com.sa/v1/events/' + event_id+'/'
            r = requests.put(url, json.dumps(respones), headers=headers)
            print r

        eventType = event['type']
        for case in switch(eventType):

            if case('subscription.created'):
                #new(site, db_password= 'admin', admin_password='admin', app='erpnext', users=None, expiry=None, space=None, emails=None, expired=False)
                site = event.get('data').get('name') + domain
                res = cmd.new(site)
                send_result(res.get("status"), "1", message= res.get("message"), landing_page_url = "http://95.177.140.114", management_page_url = "http://95.177.140.114")
                return res
                break

            if case('subscription.canceled'):
                site = event.get('data').get('name') + domain
                expiry = event.get('data').get('end_date')
                expired = True
                res = cmd.set_limits(site, expired = expired, expiry = expiry)
                print res.get('message')+ "\n"+ res.get('status')
                send_result(res.get("status"), "1", message= res.get("message")+" ")
                break
            if case('subscription.plan.changed'):
                site = ""
                users=None
                expiry=None
                space=None
                emails=None
                res = cmd.set_limits(site, users, expiry, space, emails)
                break
            if case('subscription.addon.attached'):
                print 4
                break
            if case('subscription.addon.canceled'):
                print 5
                break
            if case('subscription.user.added'):
                print 6
                break
            if case('subscription.user.removed'):
                print 7
                break
            if case('subscription.user.roles.changed'):
                print 8
                break
            if case('account.suspended'):
                print 9
                break
            if case('account.resumed'):
                print 10
                break
            if case('account.trial.first.suspended'):
                print 11
                break
            if case('account.trial.second.suspended'):
                print 12
                break
            if case('account.trial.final.suspended'):
                print 13
                break
            if case('account.billing.activated'):
                print 14
                break
            if case('account.terminated'):
                print 15
                break
            if case('webhook.test'):
                #cmd.delete("site2.domain")
                send_result("success", "1")
                break
            if case('event.expired'):
                print 17
                break
            if case(): # default, could also just omit condition or 'if True'
                print "something else!"
