from faslr.connection import FaslrConnection

from faslr.utilities import set_sqlite_pragma

def test_fk_pragma():

    fconn = FaslrConnection(
        db_path='sample.db'
    )
    set_sqlite_pragma(
        dbapi_connection=fconn.raw_connection,
        connection_record=None
    )
