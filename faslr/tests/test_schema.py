import sqlalchemy as sa

from faslr import schema

engine = sa.create_engine(
    'sqlite:///test_schema.db',
    echo=True
)

schema.Base.metadata.create_all(engine)
connection = engine.connect()

