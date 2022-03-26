from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    DateTime,
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

    lob_id = Column(
        Integer,
        ForeignKey("lob.lob_id")
    )

    user_id = Column(
        Integer,
        ForeignKey("user.user_id")
    )

    created_on = Column(
        DateTime,
        default=datetime.now
    )

    lob = relationship(
        "LOBTable", back_populates="project"
    )

    user = relationship(
        "UserTable", back_populates="project"
    )

    def __repr__(self):
        return "<ProjectTable(" \
               "lob_id='%s', " \
               "created_on='%s'" \
               ")>" % (
                   self.lob_id,
                   self.created_on
               )


class CountryTable(Base):
    __tablename__ = 'country'

    country_id = Column(
        Integer,
        primary_key=True
    )

    country_name = Column(String)

    project_tree_uuid = Column(
        String
    )

    state = relationship(
        "StateTable",
        back_populates="country",
        cascade="all, delete-orphan"
    )

    lob = relationship(
        "LOBTable", back_populates="country"
    )

    def __repr__(self):
        return "CountryTable(" \
               "country_name='%s', " \
               "project_tree_uuid='%s', " \
               ")>" % (
                   self.country_name,
                   self.project_tree_uuid
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

    project_tree_uuid = Column(String)

    country = relationship(
        "CountryTable",
        back_populates="state"
    )

    lob = relationship(
        "LOBTable",
        back_populates="state",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return "StateTable(" \
               "state_name='%s', " \
               "project_tree_uuid='%s', " \
               ")>" % (
                   self.country_name,
                   self.project_tree_uuid
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

    project_tree_uuid = Column(
        String
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
               "project_tree_uuid='%s', " \
               ")>" % (
                   self.lob_type,
                   self.project_tree_uuid
               )


class UserTable(Base):
    __tablename__ = 'user'

    user_id = Column(
        Integer,
        primary_key=True
    )

    project = relationship(
        "ProjectTable", back_populates="user"
    )

    def __repr__(self):
        return "UserTable(" \
               ")>" % (

               )
