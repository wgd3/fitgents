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
    Column('fat_chest', Integer),
    Column('fat_abdominal', Integer),
    Column('fat_thigh', Integer),
    Column('fat_tricep', Integer),
    Column('fat_subscapular', Integer),
    Column('fat_suprailiac', Integer),
    Column('fat_midaxillary', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['body_history'].columns['fat_abdominal'].create()
    post_meta.tables['body_history'].columns['fat_chest'].create()
    post_meta.tables['body_history'].columns['fat_midaxillary'].create()
    post_meta.tables['body_history'].columns['fat_subscapular'].create()
    post_meta.tables['body_history'].columns['fat_suprailiac'].create()
    post_meta.tables['body_history'].columns['fat_thigh'].create()
    post_meta.tables['body_history'].columns['fat_tricep'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['body_history'].columns['fat_abdominal'].drop()
    post_meta.tables['body_history'].columns['fat_chest'].drop()
    post_meta.tables['body_history'].columns['fat_midaxillary'].drop()
    post_meta.tables['body_history'].columns['fat_subscapular'].drop()
    post_meta.tables['body_history'].columns['fat_suprailiac'].drop()
    post_meta.tables['body_history'].columns['fat_thigh'].drop()
    post_meta.tables['body_history'].columns['fat_tricep'].drop()
