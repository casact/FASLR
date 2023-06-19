# import sqlalchemy as sa
#
# from faslr import schema
# from faslr.schema import UserTable, CountryTable, LocationTable
# from sqlalchemy.orm import sessionmaker
#
# engine = sa.create_engine(
#     'sqlite:///test_schema.db',
#     echo=True
# )
#
# schema.Base.metadata.create_all(engine)
# session = sessionmaker(bind=engine)()
# connection = engine.connect()
#
# country_text = 'USA'
# country_query = session.query(CountryTable).filter(CountryTable.country_name == country_text)
#
# session.query(LocationTable)
# session.commit()
#
# connection.close()

from faslr.schema import (
    CountryTable,
    LocationTable,
    StateTable,
    LOBTable,
    ProjectTable,
    UserTable,
    ProjectViewTable,
    ProjectViewData,
    IndexTable,
    IndexValuesTable
)

def test_country_table() -> None:
    country_table = CountryTable()

    repr(country_table)

def test_location_table() -> None:
    location_table = LocationTable()

    repr(location_table)

def test_state_table() -> None:
    state_table = StateTable()

    repr(state_table)

def test_lob_table() -> None:

    lob_table = LOBTable()

    repr(lob_table)

def test_project_table() -> None:

    project_table = ProjectTable()

    repr(project_table)

def test_user_table() -> None:

    user_table = UserTable()

    repr(user_table)

def test_project_view_table() -> None:

    project_view_table = ProjectViewTable()

    repr(project_view_table)

def test_project_view_data() -> None:

    project_view_data = ProjectViewData()

    repr(project_view_data)

def test_index_table() -> None:

    index_table = IndexTable()

    repr(index_table)

def test_index_values_table() -> None:

    index_values_table = IndexValuesTable()

    repr(index_values_table)
