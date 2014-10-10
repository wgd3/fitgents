from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
body_history = Table('body_history', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('timestamp', Date),
    Column('weight', Float),
    Column('bodyfat', Float),
    Column('lean_muscle', Float),
    Column('circ_chest', Float),
    Column('circ_waist', Float),
    Column('circ_thigh', Float),
    Column('circ_neck', Float),
    Column('circ_upperarm', Float),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['body_history'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['body_history'].drop()
