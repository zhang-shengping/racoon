#!/usr/bin/env python
# encoding: utf-8

from oslo_log import log
from stevedore.dispatch import DispatchExtensionManager

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
            # filter out unvalid event
            return all([prefix == ext.name,
                        ext.obj.vaild_message(message)])

        # # when success change to lambda
        def process_func(ext, message):
            ext.obj.dispatch(message)

        for m in messages:
            try:
                self.manager.map(_filter_func,
                                 process_func, m)
            except Exception:
                LOG.debug("can not dipatch message %s", m)
                raise
