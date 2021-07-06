from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer
)

Base = declarative_base()


class ProjectTable(Base):
    __tablename__ = 'projects'

    project_id = Column(
        Integer,
        primary_key=True
    )

    def __repr__(self):
        return "<ProjectTable(" \
               ")>" % (
                )
