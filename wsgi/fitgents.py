import os

if not 'OPENSHIFT_POSTGRESQL_DB_URL' in os.environ:
	SQLALCHEMY_DATABASE_URI = 'postgresql://adminvvg3utl:h7Q8GAk2msm1@127.0.0.1:5432/fitgents'
	SQLALCHEMY_MIGRATE_REPO = os.path.abspath(os.path.dirname(__file__)) + '/../data/db_repository'

else:
	SQLALCHEMY_DATABASE_URI = os.environ['OPENSHIFT_POSTGRESQL_DB_URL']
	SQLALCHEMY_MIGRATE_REPO = '/var/lib/openshift/543420d2500446f95b00026b/app-root/data/db_repository'

SQLALCHEMY_ECHO = False
SECRET_KEY = 'teh_secret'
DEBUG = True
