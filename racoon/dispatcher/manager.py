#!/usr/bin/env python
# encoding: utf-8

import stevedore

from stevedore import dispatch
from oslo_log import log

class DispatchManager(object):

    def __init__(self, services=[]):
        self.services = services

    @property
    def manager(self):

        def _check_func(ext):
            return ext.name in self.services

        return dispatch.DispatchExtensionManager(
            namespace='racoon.dispatcher',
            check_func=_check_func,
            invoke_on_load=True
        )

    def dispatch(messages):

        def _filter_func(ext, message):
            event_type = message.get('event_type')
            prefix = event_type.split('.')[0]
            return prefix == ext.name

        # when success change to lambda
        def process_func(ext, message):
            ext.obj.dispatch(message)

        for m in messages:
            self.manager.map(_filter_func,
                             process_func, m)


