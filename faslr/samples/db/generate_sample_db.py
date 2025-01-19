# Generates the example database (used for tutorials, testing)

import os
import sys
from os.path import dirname
faslr_path = dirname(dirname(dirname(dirname(os.path.realpath(__file__)))))
sys.path.append(faslr_path)

import faslr.utilities # noqa
import pandas as pd
import sqlalchemy as sa

from faslr import schema

from faslr.constants import SAMPLE_DB_NAME

from faslr.schema import (
    CountryTable,
    IndexTable,
    IndexValuesTable,
    LocationTable,
    StateTable,
    LOBTable,
    ProjectTable,
    ProjectViewTable,
    ProjectViewData
)

from faslr.utilities.sample import (
    XYZ_RATE_INDEX,
    XYZ_TREND_INDEX,
    XYZ_TORT_INDEX
)

from sqlalchemy.orm import sessionmaker
from uuid import uuid4

db_name = SAMPLE_DB_NAME

# If the sample database already exists, delete it.
try:
    os.remove(db_name)
except OSError:
    pass

# Create and connect to the database.
engine = sa.create_engine(
    'sqlite:///' + db_name,
    echo=True,
    connect_args={
        'check_same_thread': False
    }
)


schema.Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()
connection = engine.connect()

country_uuid = str(uuid4())
state_uuid = str(uuid4())
lob_uuid = str(uuid4())

new_country_project = ProjectTable(project_id=country_uuid)
new_state_project = ProjectTable(project_id=state_uuid)
new_lob_project = ProjectTable(project_id=lob_uuid)

new_country_location = LocationTable(hierarchy="country")
new_state_location = LocationTable(hierarchy="state")

session.add(new_country_project)
session.add(new_country_location)
session.add(new_lob_project)
session.add(new_state_project)
session.add(new_state_location)
session.flush()

new_country = CountryTable(
    location_id=new_country_location.location_id,
    country_name="USA",
    project_id=new_country_project.project_id
)

session.add(new_country)
session.flush()

new_state = StateTable(
    location_id=new_state_location.location_id,
    state_name="Texas",
    country_id=new_country.country_id,
    project_id=new_state_project.project_id
)

new_lob = LOBTable(
    lob_type="Auto",
    location_id=new_state_location.location_id,
    project_id=new_lob_project.project_id
)

path = os.path.dirname(os.path.abspath(__file__))
df_steady_state = pd.read_csv(os.path.join(path, "../friedland_us_auto_steady_state.csv"))

project_view = ProjectViewTable(
    name="Auto",
    description="Auto Steady State",
    origin="Accident Year",
    development="Calendar Year",
    columns="Paid Claims;Reported Claims",
    cumulative=True,
    project_id=new_lob_project.project_id
)

session.add(new_state)
session.add(new_lob)
session.add(project_view)
session.flush()

df_steady_state.columns = [
            'accident_year',
            'calendar_year',
            'paid_loss',
            'reported_loss'
]

df_steady_state['view_id'] = project_view.view_id

data_list = df_steady_state.to_dict('records')

obj_list = []
for record in data_list:
    data_obj = ProjectViewData(**record)
    obj_list.append(data_obj)

session.add_all(obj_list)

def insert_index(
        index: dict,
        scope: str  # 'Global' or 'Project'
) -> None:

    new_index = IndexTable(
        name=index['Name'][0],
        description=index['Description'][0],
        scope=scope
    )

    session.add(new_index)
    session.flush()

    df_index = pd.DataFrame(data={'year': index['Origin'], 'change': index['Change']})
    df_index['index_id'] = new_index.index_id

    change_list = df_index.to_dict('records')

    obj_list = []
    for record in change_list:
        data_obj = IndexValuesTable(**record)
        obj_list.append(data_obj)

    session.add_all(obj_list)


indexes_to_add = [
    XYZ_RATE_INDEX,
    XYZ_TREND_INDEX,
    XYZ_TORT_INDEX
]

for index in indexes_to_add:
    insert_index(
        index=index,
        scope='Global'
    )

session.commit()

session.close()
