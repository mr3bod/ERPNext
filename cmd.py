from __future__ import unicode_literals

import os, sys, subprocess
import json
import requests
import datetime
from dateutil.relativedelta import relativedelta
#sys.path.insert(0, os.path.abspath(__file__ + "/../../../frappe"))
#import frappe
#from frappe.commands.site import use
#from frappe.commands.site import new_site

def new(site, db_password= 'admin', admin_password='admin', app='erpnext', users=None, expiry=None, space=None, emails=None, expired=False):
	#subprocess.call("cd ..", shell=True)
	try:
		cmd ='bench new-site --mariadb-root-password ' + db_password + ' --admin-password ' + admin_password + ' ' + site + ' && bench --site ' + site + ' install-app ' + app
		output = subprocess.check_call(cmd, stderr= subprocess.STDOUT, shell= True)
	except subprocess.CalledProcessError as e:
		return {"status":"error",
		"message":e.output}
	limits = set_limits(site, users, expiry, space, emails, expired)
	#os.system(cmd)
	return {"status": "success", "message": {"limits":limits} }

def delete(site, root_password= 'admin'):
	duration = +6
	data = get_limits(site)
	limits = data.get("limits")
	print "\n0"
	if limits is not None:
		print "\nf"
		expired = limits.get("expired")
		expiry = limits.get("expiry")
		if expired and expiry is not None:
			print "\nff"
			now = datetime.datetime.now()
			delete_date = datetime.datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S") + relativedelta(months = duration)
			print "\ndelete_date" + " " + delete_date.strftime('%m/%d/%Y') + "now " + now.strftime('%m/%d/%Y')
			if delete_date < now:
				print "\nfff"
				try:
					cmd ='bench drop-site --root-password '+ root_password + ' ' + site
					output = subprocess.check_call(cmd, stderr= subprocess.STDOUT, shell=True)
				except subprocess.CalledProcessError as e:
					return {"status":"error",
					"message":e.output}
				return {"status":"success"}
#new_user(site, admin_login, admin_password, first_name, last_name, user_name, new_password)
"""
def new_user(site,admin_login,admin_password, first_name, last_name, user_name, email, new_password, middle_name = "", user_image = "", email_signature= "", send_password_update_notification="0", time_zone="Asia/Riyadh", mobile_no="", location="", simultaneous_sessions="1", roles=["Employee"], docstatus="0", background_image="", phone="", login_after="0", language="ar", gender="", login_before="0", enabled="1"):
	req=None
	try:
		with requests.Session() as s:
			login = requests.post("http://" + site + "/api/method/login", data = {
			"usr":admin_login,
			"pwd":admin_password})
			headers = {"Content-Type": "application/json"}
			d= {
			"first_name":first_name,
			"email":email,
			}
			d = json.dumps(d)
			req = requests.post("http://" + site + "/api/resource/User", data = d , headers=headers)
	except Exception as e:
		return e.message
"""

def set_limits(site, users=None, expiry=None, space=None, emails=None, expired=False):
	#sys.path.insert(0, os.path.abspath(__file__ + "/../../../sites/"+site))
	upgrade_url = "http://localhost:5000/"

	data = get_limits(site, remove = True)

	data["limits"]["upgrade_url"]=upgrade_url
	data["limits"]["expired"]=expired
	if users is not None:
		data["limits"]["users"]=users
	if expiry is not None:
		data["limits"]["expiry"]=expiry
	if space is not None:
		data["limits"]["space"]=space
	if emails is not None:
		data["limits"]["emails"]=emails
	fil = get_conf(site)
	with open(fil, 'w') as f:
		json.dump(data, f, indent=4)
	return {"status":"success"}

def get_limits(site, remove = False):
	fil = get_conf(site)
	with open(fil, 'r') as f:
		data = json.load(f)
		if "limits" not in data:
			data["limits"] = {}
	if remove:
		os.remove(fil)
	return data
def get_conf(site):
	path = os.path.abspath(__file__ + "/../../../../sites/"+site)
	filename = "/site_config.json"
	fil = path+filename
	return fil
