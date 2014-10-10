from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
sleep_history = Table('sleep_history', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('user_id', INTEGER),
    Column('timestamp', TIMESTAMP),
)

sleep_history = Table('sleep_history', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('sleep_start', DateTime),
    Column('sleep_end', DateTime),
    Column('quality', Float),
    Column('total_time', Time),
    Column('wake_up_mood', Text),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['sleep_history'].columns['timestamp'].drop()
    post_meta.tables['sleep_history'].columns['quality'].create()
    post_meta.tables['sleep_history'].columns['sleep_end'].create()
    post_meta.tables['sleep_history'].columns['sleep_start'].create()
    post_meta.tables['sleep_history'].columns['total_time'].create()
    post_meta.tables['sleep_history'].columns['wake_up_mood'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['sleep_history'].columns['timestamp'].create()
    post_meta.tables['sleep_history'].columns['quality'].drop()
    post_meta.tables['sleep_history'].columns['sleep_end'].drop()
    post_meta.tables['sleep_history'].columns['sleep_start'].drop()
    post_meta.tables['sleep_history'].columns['total_time'].drop()
    post_meta.tables['sleep_history'].columns['wake_up_mood'].drop()
