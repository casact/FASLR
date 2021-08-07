from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String
)

Base = declarative_base()


class ProjectTable(Base):
    __tablename__ = 'projects'

    project_id = Column(
        Integer,
        primary_key=True
    )

    country = Column(String)
    state = Column(String)
    line_of_business = Column(String)

    def __repr__(self):
        return "<ProjectTable(" \
               "country='%s', " \
               "state='%s', " \
               "line_of_business='%s', " \
               ")>" % (
                self.country,
                self.state,
                self.line_of_business
                )
