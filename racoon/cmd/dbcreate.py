#!/usr/bin/env python
# encoding: utf-8

from oslo_config import cfg

from racoon.storage.connection import Connection
from racoon.storage import models
from racoon import service

from sqlalchemy import create_engine

# this is a global variable, always get the same CONF
# I can get all variable, as long as I register it
# before I query it. It can be register anywhere.
# every oslo with options.set_defaults method.
# The values in configuration filea can be assigned
# to CONF, as long as I call cfg.CONF(project=)
CONF = cfg.CONF

def create_db():
    service.prepare_service()
    url = CONF.database.connection
    db_conn = Connection(url)
    engine = db_conn.engine
    models.Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_db()


