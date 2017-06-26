#!/usr/bin/env python
# encoding: utf-8

from oslo_config import cfg

from racoon.storage import Resource
from racoon.storage import connection as conn

METHOD_MAP = {
    'compute.instance.create.end':'compute_create'
}

ID_MAP = {
    'compute.instance.create.end':'instance_id'
}

class DispatcherBase(object):
    # we can define a map of method and database here

    def __init__(self):
        print cfg.CONF.database.connection
        self.conn = conn.get_conn_from_config(cfg.CONF)

    def get_method(self,event_type):
        pass

    def get_resource_id(self, payload, event_type):
        id_name = ID_MAP.get(event_type)
        resource_id = payload.get(id_name)
        return resource_id

    def get_attributes(self, payload):
        return "this is a test"

    def get_resource(self, message):
        payload = message.get('payload')
        metadata = message.get('metadata')
        event_type = message.get('event_type')

        res = {}
        if payload and metadata and event_type:
            res['message_id'] = payload.get('message_id')
            res['user_id'] = payload.get('user_id')
            res['resource_id'] = self.get_resource_id(
                payload, event_type)
            res['start_timestamp'] = metadata.get('timestamp')
            res['attributes'] = self.get_attributes(payload)

            return Resource(res)

    def dispatch(self, messages):
        for m in messages:
            res = self.get_resource(m)
            self.conn.add_resource(res)
