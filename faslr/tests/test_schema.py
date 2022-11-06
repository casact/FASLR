import sqlalchemy as sa

from faslr import schema
from faslr.schema import UserTable
from sqlalchemy.orm import sessionmaker

engine = sa.create_engine(
    'sqlite:///test_schema.db',
    echo=True
)

schema.Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()
connection = engine.connect()

new_user = UserTable(user_name="Gene")

session.add(new_user)
session.commit()

connection.close()
