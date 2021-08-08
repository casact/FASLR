from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String
)

from sqlalchemy.orm import relationship

Base = declarative_base()


class ProjectTable(Base):
    __tablename__ = 'project'

    project_id = Column(
        Integer,
        primary_key=True
    )

    country_id = Column(
        Integer,
        ForeignKey('country.country_id')
    )
    state_id = Column(
        Integer,
        ForeignKey('state.state_id')
    )
    lob_id = Column(
        Integer,
        ForeignKey("lob.lob_id")
    )

    country = relationship(
        "CountryTable", back_populates="project"
    )

    state = relationship(
        "StateTable", back_populates="project"
    )

    lob = relationship(
        "LOBTable", back_populates="project"
    )

    def __repr__(self):
        return "<ProjectTable(" \
               "country_id='%s', " \
               "state_id='%s', " \
               "lob_id='%s', " \
               ")>" % (
                   self.country_id,
                   self.state_id,
                   self.lob_id
               )


class CountryTable(Base):
    __tablename__ = 'country'

    country_id = Column(
        Integer,
        primary_key=True
    )

    country_name = Column(String)

    state = relationship(
        "StateTable", back_populates="country"
    )

    project = relationship(
        "ProjectTable", back_populates="country"
    )

    lob = relationship(
        "LOBTable", back_populates="country"
    )

    def __repr__(self):
        return "CountryTable(" \
               "country_name='%s', " \
               ")>" % (
                   self.country_name
               )


class StateTable(Base):
    __tablename__ = 'state'

    state_id = Column(
        Integer,
        primary_key=True
    )

    country_id = Column(
        Integer,
        ForeignKey("country.country_id")
    )

    state_name = Column(String)

    country = relationship("CountryTable", back_populates="state")

    project = relationship("ProjectTable", back_populates="state")

    lob = relationship("LOBTable", back_populates="state")

    def __repr__(self):
        return "StateTable(" \
               "state_name='%s', " \
               ")>" % (
                   self.country_name
               )


class LOBTable(Base):
    __tablename__ = 'lob'

    lob_id = Column(
        Integer,
        primary_key=True
    )

    country_id = Column(
        Integer,
        ForeignKey('country.country_id')
    )

    state_id = Column(
        Integer,
        ForeignKey('state.state_id')
    )

    lob_type = Column(String)

    country = relationship(
        "CountryTable", back_populates="lob"
    )

    state = relationship(
        "StateTable", back_populates="lob"
    )

    project = relationship(
        "ProjectTable", back_populates="lob"
    )

    def __repr__(self):
        return "LOBTable(" \
               "lob_type='%s', " \
               ")>" % (
                   self.lob_type
               )

