from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Boolean,
    Column,
    Float,
    DateTime,
    Integer,
    ForeignKey,
    String,
)

from sqlalchemy.orm import (
    relationship
)

Base = declarative_base()


class LocationTable(Base):
    __tablename__ = 'location'

    location_id = Column(
        Integer,
        primary_key=True
    )

    hierarchy = Column(
        String
    )

    country = relationship(
        "CountryTable",
        back_populates="location",
        cascade="all, delete"
    )

    state = relationship(
        "StateTable",
        back_populates='location',
        cascade="all, delete"
    )

    lob = relationship(
        "LOBTable",
        back_populates="location",
        cascade="all, delete"
    )

    def __repr__(self):
        return "LocationTable(" \
               "hierarchy='%s'" \
               ")>" % (
                   self.hierarchy
               )


class CountryTable(Base):
    __tablename__ = 'country'

    country_id = Column(
        Integer,
        primary_key=True
    )

    project_id = Column(
        String,
        ForeignKey('project.project_id')
    )

    location_id = Column(
        Integer,
        ForeignKey(
            'location.location_id',
            ondelete="CASCADE"
        )
    )

    country_name = Column(String)

    location = relationship(
        "LocationTable",
        back_populates="country"
    )

    state = relationship(
        "StateTable",
        back_populates="country",
        cascade="all, delete"
    )

    project = relationship(
        "ProjectTable",
        back_populates="country",
        cascade="all, delete"
    )

    def __repr__(self):
        return "CountryTable(" \
               "project_id='%s', " \
               "location_id='%s', " \
               "country_name='%s', " \
               "project_id='%s'" \
               ")>" % (
                   self.project_id,
                   self.location_id,
                   self.country_name,
                   self.project_id
               )


class StateTable(Base):
    __tablename__ = 'state'

    state_id = Column(
        Integer,
        primary_key=True
    )

    location_id = Column(
        Integer,
        ForeignKey(
            "location.location_id",
            ondelete="CASCADE"
        )
    )

    country_id = Column(
        Integer,
        ForeignKey(
            "country.country_id",
            ondelete="CASCADE"
        )
    )

    project_id = Column(
        String,
        ForeignKey('project.project_id')
    )

    state_name = Column(String)

    country = relationship(
        "CountryTable",
        back_populates="state"
    )

    location = relationship(
        "LocationTable",
        back_populates="state",
        cascade="all, delete"
    )

    project = relationship(
        "ProjectTable",
        back_populates="state",
        cascade="all, delete"
    )

    def __repr__(self):
        return "StateTable(" \
               "location_id='%s'" \
               "country_id='%s', " \
               "location_id='%s', " \
               "state_name='%s', " \
               "project_id='%s', " \
               ")>" % (
                   self.location_id,
                   self.country_id,
                   self.location_id,
                   self.state_name,
                   self.project_id
               )


class LOBTable(Base):
    __tablename__ = 'lob'

    lob_id = Column(
        Integer,
        primary_key=True
    )

    lob_type = Column(String)

    location_id = Column(
        Integer,
        ForeignKey(
            'location.location_id',
            ondelete="CASCADE"
        )
    )

    project_id = Column(
        String,
        ForeignKey('project.project_id')
    )

    location = relationship(
        "LocationTable",
        back_populates='lob'
    )

    project = relationship(
        "ProjectTable",
        back_populates="lob",
        cascade='all, delete'
    )

    def __repr__(self):
        return "LOBTable(" \
               "lob_type='%s', " \
               "location_id='%s', " \
               "project_id='%s'" \
               ")>" % (
                   self.lob_type,
                   self.location_id,
                   self.project_id
               )


class ProjectTable(Base):
    __tablename__ = 'project'

    project_id = Column(
        String,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("user.user_id")
    )

    created_on = Column(
        DateTime,
        default=datetime.now
    )

    country = relationship(
        "CountryTable",
        back_populates="project"
    )

    state = relationship(
        "StateTable",
        back_populates="project"
    )

    lob = relationship(
        "LOBTable",
        back_populates="project"
    )

    user = relationship(
        "UserTable",
        back_populates="project"
    )

    project_view = relationship(
        "ProjectViewTable",
        back_populates="project"
    )

    index = relationship(
        "IndexViewTable",
        back_populates='project'
    )

    def __repr__(self):
        return "ProjectTable(" \
               "user_id='%s', " \
               "created_on='%s'" \
               ")>" % (
                   self.user_id,
                   self.created_on
               )


class UserTable(Base):
    __tablename__ = 'user'

    user_id = Column(
        Integer,
        primary_key=True
    )

    user_name = Column(
        String
    )

    project = relationship(
        "ProjectTable",
        back_populates="user"
    )

    def __repr__(self):
        return "UserTable(" \
               ")>" % (

               )


class ProjectViewTable(Base):
    __tablename__ = 'project_view'

    view_id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String
    )

    description = Column(
        String
    )

    created = Column(
        DateTime,
        default=datetime.now
    )

    modified = Column(
        DateTime,
        default=datetime.now
    )

    origin = Column(
        String
    )

    development = Column(
        String
    )

    columns = Column(
        String
    )

    cumulative = Column(
        Boolean
    )

    project_id = Column(
        String,
        ForeignKey("project.project_id")
    )

    project = relationship(
        "ProjectTable",
        back_populates="project_view"
    )

    def __repr__(self):
        return "ProjectViewsTable(" \
               "name='%s', " \
               "description='%s', " \
               "created='%s', " \
               "modified='%s', " \
               "project_id='%s'" \
               ")>" % (
                   self.name,
                   self.description,
                   self.created,
                   self.modified,
                   self.project_id
               )


class ProjectViewData(Base):
    __tablename__ = 'project_view_data'

    record_id = Column(
        Integer,
        primary_key=True
    )

    view_id = Column(
        Integer,
        ForeignKey('project_view.view_id')
    )

    accident_year = Column(
        Integer
    )

    calendar_year = Column(
        Integer
    )

    paid_loss = Column(
        Float
    )

    reported_loss = Column(
        Float
    )

    case_outstanding = Column(
        Float
    )


class IndexTable(Base):
    __tablename__ = 'index'

    index_id = Column(
        Integer,
        primary_key=True
    )

    description = Column(
        String
    )

    scope = Column(
        String # should be 'project' or 'global'
    )

    project_id = Column(
        Integer,
        ForeignKey('project.project_id')
    )

    project = relationship(
        'ProjectTable',
        back_populates='index'
    )

    def __repr__(self):
        return "IndexTable(" \
            "description='%s', " \
            "scope='%s', " \
            "project_id='%s'" \
            ")>" % (
               self.description,
               self.scope,
               self.project_id
            )


class IndexValuesTable(Base):
    __tablename__ = 'index_values'

    value_id = Column(
        Integer,
        primary_key=True
    )

    index_id = Column(
        Integer,
        ForeignKey('index.index_id')
    )

    year = Column(
        Integer
    )

    change = Column(
        Float
    )

    def __repr__(self):
        return "IndexValueTable(" \
               "index_id='%s', " \
               "year='%s', " \
               "change='%s'" \
               ")>" % (
                   self.index_id,
                   self.year,
                   self.change
               )
