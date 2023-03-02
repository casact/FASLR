from faslr.utilities.gui import open_item_tab

from sqlalchemy import event
from sqlalchemy.engine import Engine

from faslr.utilities.chainladder import (
    fetch_latest_diagonal,
    fetch_origin,
    table_from_tri
)

from faslr.utilities.sample import (
    load_sample
)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
