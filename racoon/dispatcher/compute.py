#!/usr/bin/env python
# encoding: utf-8

from racoon.dispatcher import DispatcherBase
from racoon.storage import Resource

METHOD_MAP = {
    'compute.instance.create.end':'create',
    'compute.instance.delete.end':'delete',
    'compute.instance.resize.confirm.end':'resize',
}

ATTR_MAP = {}

class ComDispatcher(DispatcherBase):
    def __init__(self):
        super(ComDispatcher, self).__init__()

        self.method_map = METHOD_MAP
        self.attr_map =  ATTR_MAP

    def init_resource(self, message):
        payload = message.get('payload')
        metadata = message.get('metadata')

        res = {}
        if payload and metadata and event_type:
            res['message_id'] = payload.get('message_id')
            res['user_id'] = payload.get('user_id')
            res['project_id'] = payload.get('project_id')
            res['resource_id'] = payload.get('instance_id')
            res['start_timestamp'] = metadata.get('timestamp')
            res['attributes'] = self._get_attributes(payload)

        return Resource(res)

    def _get_attributes(self, payload):
        pass

    def create(self, resource, *args, **kwargs):
        pass

    def delete(self, resource, *args, **kwargs):
        pass

    def resize(self, resource, *args, **kwargs):
        pass

    def test(self):
        print 'hello'
