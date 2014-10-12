from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
sleep_history = Table('sleep_history', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('sleep_start', DateTime),
    Column('sleep_end', DateTime),
    Column('quality', Float),
    Column('total_time', Time),
    Column('total_time_in_minutes', Integer),
    Column('wake_up_mood', Text),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['sleep_history'].columns['total_time_in_minutes'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['sleep_history'].columns['total_time_in_minutes'].drop()
