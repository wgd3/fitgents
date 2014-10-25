from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
excercise_history = Table('excercise_history', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('user_id', INTEGER),
    Column('timestamp', TIMESTAMP),
    Column('distance', Float),
    Column('reps', INTEGER),
    Column('set_number', INTEGER),
    Column('time', TIME),
    Column('weight', Float),
    Column('excercise_id', INTEGER),
    Column('notes', VARCHAR(length=300)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['excercise_history'].columns['time'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['excercise_history'].columns['time'].create()
