from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
users = Table('users', pre_meta,
    Column('user_id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=50)),
    Column('start_weight', DOUBLE_PRECISION(precision=53)),
    Column('start_bf', DOUBLE_PRECISION(precision=53)),
    Column('age', INTEGER),
    Column('_password', BYTEA),
    Column('_salt', VARCHAR(length=120)),
    Column('email', VARCHAR(length=50)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['users'].columns['start_bf'].drop()
    pre_meta.tables['users'].columns['start_weight'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['users'].columns['start_bf'].create()
    pre_meta.tables['users'].columns['start_weight'].create()
