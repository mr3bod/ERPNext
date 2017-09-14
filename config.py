import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SECRET_KEY= 'SomethingNotEntirelySecret'
TESTING= True
DEBUG= True
OIDC_CLIENT_SECRETS= os.path.join(basedir+'/app', 'client_secrets.json')
#oidc.discovery.discover_OP_information('https://staging-sso.stcs.com.sa/.well-known/openid-configuration')
OIDC_ID_TOKEN_COOKIE_SECURE= False
#OIDC_COOKIE_SECURE=False
#OIDC_REQUIRE_VERIFIED_EMAIL= False
#OIDC_OPENID_REALM= 'http://localhost:5000/oidc_callback'
