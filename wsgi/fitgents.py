import os

if not 'OPENSHIFT_POSTGRESQL_DB_URL' in os.environ:
	SQLALCHEMY_DATABASE_URI = 'postgresql://adminvvg3utl:h7Q8GAk2msm1@127.0.0.1:5432/fitgents'
	SQLALCHEMY_MIGRATE_REPO = os.path.abspath(os.path.dirname(__file__)) + '/../data/db_repository'

else:
	SQLALCHEMY_DATABASE_URI = os.environ['OPENSHIFT_POSTGRESQL_DB_URL']
	SQLALCHEMY_MIGRATE_REPO = os.environ['OPENSHIFT_DATA_DIR'] + '/db_repository'

SQLALCHEMY_ECHO = False
SECRET_KEY = '179428949761744668011701279644222272035'
DEBUG = True

## Mail config
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
