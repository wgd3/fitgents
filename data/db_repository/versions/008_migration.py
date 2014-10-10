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
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['users'].columns['is_admin'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['users'].columns['is_admin'].drop()
