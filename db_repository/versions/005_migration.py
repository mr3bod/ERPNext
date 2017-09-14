from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
token = Table('token', post_meta,
    Column('id', String(length=28), primary_key=True, nullable=False),
    Column('expires_in', DateTime),
    Column('body', String(length=10000)),
)

event = Table('event', post_meta,
    Column('id', String(length=28), primary_key=True, nullable=False),
    Column('status', String(length=28)),
    Column('body', String(length=10000)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['token'].columns['expires_in'].create()
    post_meta.tables['event'].columns['status'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['token'].columns['expires_in'].drop()
    post_meta.tables['event'].columns['status'].drop()
