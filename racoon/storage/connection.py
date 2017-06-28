#!/usr/bin/env python
# encoding: utf-8

import datetime

from oslo_config import cfg
from oslo_log import log
from oslo_db import api
from oslo_db.sqlalchemy import session as db_session

from racoon import storage
from racoon.storage import models

def get_conn_from_config(conf):
    url = conf.database.connection
    return Connection(url)

class Connection(storage.BaseConnection):

    def __init__(self, url):
        opts = dict(cfg.CONF.database.items())
        self._engine_facade = db_session.EngineFacade(url, **opts)

    @property
    def engine(self):
        return self._engine_facade.get_engine()

    @property
    def session(self):
        return self._engine_facade.get_session()

    def add_resource(self, resource):
        print resource
        with self.session.begin():
             timetable = models.TimeTable(
                 message_id = resource.message_id,
                 resource_id = resource.resource_id,
                 user_id = resource.user_id,
                 project_id = resource.project_id,
                 start_timestamp = resource.start_timestamp,
                 end_timestamp = resource.end_timestamp,
                 attributes = resource.attributes
             )

             self.session.add(timetable)
        print "end **************"










