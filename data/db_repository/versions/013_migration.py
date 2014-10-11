from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
food_history = Table('food_history', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('user_id', INTEGER),
    Column('timestamp', TIMESTAMP),
    Column('calories', INTEGER),
    Column('fat', INTEGER),
    Column('notes', VARCHAR(length=300)),
    Column('protein', INTEGER),
    Column('cheat_day', BOOLEAN),
    Column('carbohydrates', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['food_history'].columns['carbohydrates'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['food_history'].columns['carbohydrates'].create()
