#!/usr/bin/env python
# encoding: utf-8

from oslo_log import log
from racoon.dispatcher import DispatcherBase
from racoon.storage import Resource

METHOD_MAP = {
    'compute.instance.create.end': 'create',
    'compute.instance.delete.end': 'delete',
    # 'compute.instance.resize.confirm.end': 'resize',
}

ATTR_MAP = {}

LOG = log.getLogger(__name__)


class ComDispatcher(DispatcherBase):
    def __init__(self):
        super(ComDispatcher, self).__init__()

        self.method_map = METHOD_MAP
        self.attr_map = ATTR_MAP

    def init_resource(self, message):

        payload = message.get('payload')
        metadata = message.get('metadata')
        res = {}

        res['user_id'] = payload.get('user_id')
        res['project_id'] = payload.get('tenant_id')
        res['resource_id'] = payload.get('instance_id')
        res['message_id'] = metadata.get('message_id')
        res['timestamp'] = metadata.get('timestamp')
        res['attributes'] = self._get_attributes(payload)

        # insert some log here
        return Resource(res)

    def _get_attributes(self, payload):
        attrs = {}
        attrs['instance_flavor_id'] = payload.get('instance_flavor_id')
        return attrs

    def create(self, resource, *args, **kwargs):
        LOG.info('start a resource %s', resource)
        self.conn.resource_start(resource)

    def delete(self, resource, *args, **kwargs):
        LOG.info('end a resource %s', resource)
        self.conn.resource_end(resource)

    def resize(self, resource, *args, **kwargs):
        pass

    def test(self):
        pass
