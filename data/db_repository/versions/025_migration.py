from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
excercise_history = Table('excercise_history', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('user_id', INTEGER),
    Column('timestamp', TIMESTAMP),
    Column('distance', DOUBLE_PRECISION(precision=53)),
    Column('reps', INTEGER),
    Column('set_number', INTEGER),
    Column('time', TIME),
    Column('weight', DOUBLE_PRECISION(precision=53)),
    Column('workout_number', INTEGER),
    Column('excercise_id', INTEGER),
)

excercise_history = Table('excercise_history', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('timestamp', DateTime),
    Column('excercise_id', Integer),
    Column('time', Time),
    Column('distance', Float),
    Column('weight', Float),
    Column('set_number', Integer),
    Column('reps', Integer),
    Column('notes', String(length=300)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['excercise_history'].columns['workout_number'].drop()
    post_meta.tables['excercise_history'].columns['notes'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['excercise_history'].columns['workout_number'].create()
    post_meta.tables['excercise_history'].columns['notes'].drop()
