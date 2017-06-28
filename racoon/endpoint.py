#!/usr/bin/env python
# encoding: utf-8

import oslo_messaging

from oslo_config import cfg
from oslo_log import log

from racoon.dispatcher import manager

CONF = cfg.CONF

OPTS = [
    cfg.ListOpt('services',
                default=['compute'])
]

CONF.register_opt(OPTS, 'collector')

class SampleEndpoint(object):
    def __init__(self, manager=None):
        self.services = cfg.CONF.collector.services
        self.manager = manager.DispatchManager(
            self.services)

    # this used to test
    def info(self, messages):
        try:
            self.manager.dispatch(messages)
        except Exception:
            return oslo_messaging.NotificationResult.REQUEUE
        print 'end'

        #add exception requeue



