from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
users = Table('users', post_meta,
    Column('user_id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=50)),
    Column('email', String(length=50)),
    Column('age', Integer),
    Column('_password', LargeBinary(length=120)),
    Column('_salt', String(length=120)),
    Column('is_admin', Boolean),
    Column('goal_weight', Float),
    Column('goal_bodyfat', Float),
    Column('sign_up_date', Date),
    Column('calorie_goal', Integer),
    Column('verified_email', Boolean),
    Column('greek_wrist', Float),
    Column('greek_chest', Float),
    Column('greek_forearm', Float),
    Column('greek_waist', Float),
    Column('greek_thigh', Float),
    Column('greek_hip', Float),
    Column('greek_calf', Float),
    Column('greek_bicep', Float),
    Column('greek_neck', Float),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['users'].columns['greek_bicep'].create()
    post_meta.tables['users'].columns['greek_calf'].create()
    post_meta.tables['users'].columns['greek_chest'].create()
    post_meta.tables['users'].columns['greek_forearm'].create()
    post_meta.tables['users'].columns['greek_hip'].create()
    post_meta.tables['users'].columns['greek_neck'].create()
    post_meta.tables['users'].columns['greek_thigh'].create()
    post_meta.tables['users'].columns['greek_waist'].create()
    post_meta.tables['users'].columns['greek_wrist'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['users'].columns['greek_bicep'].drop()
    post_meta.tables['users'].columns['greek_calf'].drop()
    post_meta.tables['users'].columns['greek_chest'].drop()
    post_meta.tables['users'].columns['greek_forearm'].drop()
    post_meta.tables['users'].columns['greek_hip'].drop()
    post_meta.tables['users'].columns['greek_neck'].drop()
    post_meta.tables['users'].columns['greek_thigh'].drop()
    post_meta.tables['users'].columns['greek_waist'].drop()
    post_meta.tables['users'].columns['greek_wrist'].drop()
