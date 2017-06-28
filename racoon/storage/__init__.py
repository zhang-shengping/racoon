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

class Resource(object):
    def __init__(self, data):
        self.message_id = data.get('message_id')
        self.user_id = data.get('user_id')
        self.project_id = data.get('project_id')
        self.resource_id = data.get('resource_id')
        self.start_timestamp = data.get('start_timestamp')
        self.end_timestamp = data.get('end_timestamp')
        self.attributes = data.get('attributes')

    def __rper__(self):
        return ("<SampleFilter("
                " message_id: %s,"
                " user_id: %s,"
                " project_id: %s,"
                " resource_id: %s,"
                " start_timestamp: %s,"
                " end_timestamp: %s,"
                " attributes: %s)>" %
                (self.message_id,
                 self.user_id,
                 self.project_id,
                 self.resource_id,
                 self.start_timestamp,
                 self.end_timestamp,
                 self.attributes))

