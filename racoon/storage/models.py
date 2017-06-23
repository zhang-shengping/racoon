#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import Table, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

import datetime

_COMMON_TABLE_ARGS = {'mysql_charset': "utf8", 'mysql_engine': "InnoDB"}

class RacoonBase(object):
    __table_args__ = _COMMON_TABLE_ARGS
    # dont know why
    #__table_initialized__ = False

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        getattr(self, key)

    def update(self, values):
        for k, v in values:
            setattr(self, k, v)

Base = declarative_base(cls=RacoonBase)

class TimeTable(Base):
    __tablename__ = 'timetable'

    message_id = Column(String(255), index=True,
                        nullable=False, primary_key=True)
    resource_id = Column(String(255), index=True, nullable=False)
    start_timestamp= Column(DateTime(255), index=True,
                            nullable=False)
    end_timestamp= Column(DateTime(), index=True)
    attributes = Column(String(255))

