#!/usr/bin/env python
# encoding: utf-8

import tenacity

from oslo_config import cfg
from oslo_db import options as db_options

OPTS = [
    cfg.StrOpt('connection',
               secret=True)
]

db_options.set_defaults(cfg.CONF)

def get_connection_from_config(conf):
    # provide configuration file
    # 还是从Connection 中取得self._engine_facade.get_engine()
    pass

# this class maybe move to some other file later
class BaseConnection(object):
    def __init__(self, url):
        pass

    def get_reosource_by_id(self, resource_id):
        pass

    def add_resources(self, resources):
        """
        accept a list of resources,
        and persist them
        """
        pass

    def add_resource(self, resource):
        pass

    def update_resource(self, resource):
        pass

    def delete_resource_by_id(self, resource):
        pass

    def clear_expired_resources(self):
        """
        check the end_timestamp if expired
        """
        pass

    def renew_resource(self, resource):
        """
        check the resource which it has no end_timestamp,
        then update that resource.
        """
        pass
