#!/usr/bin/env python
# encoding: utf-8

import stevedore

from stevedore.dispatch import DispatchExtensionManager
from oslo_log import log

LOG = log.getLogger(__name__)

class DispatchManager(object):

    def __init__(self, services=[]):
        self.services = services
        self.manager = DispatchExtensionManager(
            namespace='racoon.dispatcher',
            check_func=lambda ext: ext.name in self.services,
            invoke_on_load=True,
            propagate_map_exceptions=True
        )

    def dispatch(self, messages):

        def _filter_func(ext, message):
            event_type = message.get('event_type')
            prefix = event_type.split('.')[0]
            return prefix == ext.name

        # # when success change to lambda
        def process_func(ext, message):
            ext.obj.dispatch(message)

        for m in messages:
            LOG.info("here is here")
            self.manager.map(_filter_func,
                             process_func, m)


