import os
import sqlalchemy as sa
import schema

from sqlalchemy.orm import sessionmaker

if not os.path.exists('db'):
    os.makedirs('db')
engine = sa.create_engine(
    'sqlite:///db/test.db',
    echo=True
)
session = sessionmaker(bind=engine)
schema.Base.metadata.create_all(engine)
session = session()
connection = engine.connect()
