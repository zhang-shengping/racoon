#!/usr/bin/env python
# encoding: utf-8

from oslo_config import cfg

from racoon.storage import Resource
from racoon.storage import connection as conn

class DispatcherBase(object):
    # we can define a map of method and database here

    def __init__(self):
        self.conn = conn.get_conn_from_config(cfg.CONF)
        self.method_map = {}
        self.attr_map = {}

    def _get_method(self, event_type, resource):
        meth = self.method_map.get(event_type)
        return getattr(self, meth)

    def get_resource_id(self, payload, event_type):
        id_name = ID_MAP.get(event_type)
        resource_id = payload.get(id_name)
        return resource_id

     def _get_attributes(self, payload):
         pass

    def init_resource(self, message):
        pass

    def dispatch(self, messages):
        for m in messages:
            res = self.init_resource(m)
            meth = self._get_method(m.get('event_type'),
                                   res)
            if meth:
                meth(res)
