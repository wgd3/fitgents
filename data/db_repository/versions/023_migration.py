from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
excercise_list = Table('excercise_list', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('added_by', Integer),
    Column('date_added', Date),
    Column('name', String(length=50)),
    Column('type', String(length=50)),
)

excercise_history = Table('excercise_history', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('timestamp', DateTime),
    Column('time', Time),
    Column('distance', Float),
    Column('weight', Float),
    Column('set_number', Integer),
    Column('reps', Integer),
    Column('workout_number', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['excercise_list'].create()
    post_meta.tables['excercise_history'].columns['distance'].create()
    post_meta.tables['excercise_history'].columns['reps'].create()
    post_meta.tables['excercise_history'].columns['set_number'].create()
    post_meta.tables['excercise_history'].columns['time'].create()
    post_meta.tables['excercise_history'].columns['weight'].create()
    post_meta.tables['excercise_history'].columns['workout_number'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['excercise_list'].drop()
    post_meta.tables['excercise_history'].columns['distance'].drop()
    post_meta.tables['excercise_history'].columns['reps'].drop()
    post_meta.tables['excercise_history'].columns['set_number'].drop()
    post_meta.tables['excercise_history'].columns['time'].drop()
    post_meta.tables['excercise_history'].columns['weight'].drop()
    post_meta.tables['excercise_history'].columns['workout_number'].drop()
