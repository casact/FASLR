from faslr.schema import (
    LocationTable
)

from sqlalchemy.orm import Session


def delete_country(
        country_id: int,
        session: Session
) -> None:

    country = session.query(LocationTable).filter(LocationTable.location_id == country_id).one()
    session.delete(country)
    session.commit()
