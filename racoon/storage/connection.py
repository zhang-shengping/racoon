#!/usr/bin/env python
# encoding: utf-8

import datetime

from oslo_config import cfg
from oslo_log import log
from oslo_db import api
from oslo_db.sqlalchemy import session as db_session

from racoon import storage

class Connection(storage.BaseConnection):

    def __init__(self, url):
        opts = dict(cfg.CONF.database.items())
        self._engine_facade = db_session.EngineFacade(url, **opts)

    @property
    def engine(self):
        return self._engine_facade.get_engine()




