from faslr.utilities.queries import delete_country

from faslr.connection import FaslrConnection


def test_delete_country(sample_db: str) -> None:

    f_connection = FaslrConnection(
        db_path=sample_db
    )

    delete_country(
        country_id=1,
        session=f_connection.session
    )
