from faslr.utilities.gui import open_item_tab

from sqlalchemy import event
from sqlalchemy.engine import Engine

from faslr.utilities.chainladder import (
    fetch_cdf,
    fetch_latest_diagonal,
    fetch_origin,
    fetch_ultimate,
    table_from_tri
)

from faslr.utilities.collections import (
    subset_dict
)

from faslr.utilities.sample import (
    auto_bi_olep,
    load_sample,
    tort_index,
    ppa_loss_trend,
    ppa_premium_trend
)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
