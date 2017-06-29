#!/usr/bin/env python
# encoding: utf-8

from oslo_config import cfg
from oslo_log import log

from racoon.storage import Resource
from racoon.storage import connection as conn

LOG = log.getLogger(__name__)

class DispatcherBase(object):
    # we can define a map of method and database here

    def __init__(self):
        self.conn = conn.get_conn_from_config(cfg.CONF)
        self.method_map = {}
        self.attr_map = {}

    def _get_method(self, event_type, resource):
        meth = self.method_map.get(event_type)
        if meth:
            LOG.info('get method <%s> for event <%s>',
                     meth, event_type)
            return getattr(self, meth)

    def get_resource_id(self, payload, event_type):
        id_name = ID_MAP.get(event_type)
        resource_id = payload.get(id_name)
        return resource_id

    def _get_attributes(self, payload):
         pass

    def init_resource(self, message):
        pass

    def vaild_message(self, message):
        return message.get('event_type') in self.method_map

    def dispatch(self, message):
        res = self.init_resource(message)
        LOG.info('get resource %s', res)

        meth = self._get_method(message.get('event_type'),
                                   res)
        if meth:
            meth(res, **message)
