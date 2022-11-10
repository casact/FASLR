import sqlalchemy as sa

from faslr import schema
from faslr.schema import UserTable, CountryTable, LocationTable, StateTable, LOBTable, ProjectTable
from sqlalchemy.orm import sessionmaker
from uuid import uuid4

engine = sa.create_engine(
    'sqlite:///test_schema.db',
    echo=True,
    connect_args={'check_same_thread': False}
)

from sqlalchemy.engine import Engine
from sqlalchemy import event


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


schema.Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()
connection = engine.connect()


country_uuid = str(uuid4())
new_country_project = ProjectTable(project_id=country_uuid)
new_country_location = LocationTable(hierarchy="country")
new_state_location = LocationTable(hierarchy="state")

session.add(new_country_project)
session.add(new_country_location)
session.add(new_state_location)
session.flush()


new_country = CountryTable(
    location_id=new_country_location.location_id,
    country_name="USA",
    project_id=new_country_project.project_id
)

new_state = StateTable(location_id=new_state_location.location_id, state_name="Texas")
new_lob = LOBTable(lob_type="Auto", location_id=2)


session.add(new_country)
session.add(new_state)
session.add(new_lob)

session.commit()
session.close()

old_country = session.query(LocationTable).filter(LocationTable.location_id == 1).one()
old_state = session.query(LocationTable).filter(LocationTable.location_id == 2).one()

session.delete(old_country)
session.delete(old_state)
session.commit()
session.close()
