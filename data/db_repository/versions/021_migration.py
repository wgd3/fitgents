from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
sleep_history = Table('sleep_history', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('user_id', INTEGER),
    Column('quality', DOUBLE_PRECISION(precision=53)),
    Column('sleep_end', TIMESTAMP),
    Column('sleep_start', TIMESTAMP),
    Column('total_time', TIME),
    Column('wake_up_mood', TEXT),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['sleep_history'].columns['total_time'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['sleep_history'].columns['total_time'].create()
