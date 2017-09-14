# ref: https://github.com/frappe/bench

1. Download the install script for linux
	wget https://raw.githubusercontent.com/frappe/bench/master/playbooks/install.py
2. install it (you need to be root in Ubuntu 16.04)
	sudo python install.py --production --user frappe
3. go to the Dir
	cd /home/frappe/frappe-bench
4. download ERPNext app
	bench get-app erpnext https://github.com/frappe/erpnext
5. make new app
	bench new-app commands
6. add __init__.py file in these dirs:
	 /home/frappe/frappe-bench/apps
	/home/frappe/frappe-bench/apps/commands
7. copy cmd.py from stash and paste it in the dir:
	/home/frappe/frappe-bench/apps/commands/commands/
8. replace the file limits.py from stash to the dir:
	/home/frappe/frappe-bench/apps/frappe/frappe


#flask-app
1- copy all the following files in the dir /home/frappe/frappe-bench/
	app
	config.py
	db_create.py
	db_migrate
	db_repository
	app.db
	requirements.txt
	run-redis.sh

2-install requirements.txt

3-open 3 terminals all at dir /home/frappe/frappe-bench/ and run
  1- ./run-redis.sh (you may not need this step)

  2- celery -A app.__init__.celery worker --loglevel=info

  3-export FLASK_APP=./app/__init__.py
    export FLASK_DEBUG=1 (ignore in production)
    flask run --host=0.0.0.0 --port=8080

### in app/tasks.py you need to change domain to the real domain ###
### you need to add the sitename.domain to /etc/hosts ###

