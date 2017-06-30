#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

# import datetime

_COMMON_TABLE_ARGS = {'mysql_charset': "utf8", 'mysql_engine': "InnoDB"}


class RacoonBase(object):
    __table_args__ = _COMMON_TABLE_ARGS
    # dont know why
    # __table_initialized__ = False

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        print key
        getattr(self, key)

    def update(self, values):
        for k, v in values:
            setattr(self, k, v)


Base = declarative_base(cls=RacoonBase)


class TimeTable(Base):
    __tablename__ = 'timetable'

    message_id = Column(String(255), index=True,
                        primary_key=True)
    resource_id = Column(String(255), index=True)
    user_id = Column(String(255), index=True)
    project_id = Column(String(255), index=True)
    start_timestamp = Column(DateTime(255), index=True)
    end_timestamp = Column(DateTime(), index=True)
    attributes = Column(String(255))
