#!/usr/bin/env python
# encoding: utf-8

import oslo_messaging

from oslo_config import cfg
from oslo_log import log

from racoon.dispatcher import manager

CONF = cfg.CONF
LOG = log.getLogger(__name__)

OPTS = [
    cfg.ListOpt('services',
                default=['compute'])
]
CONF.register_opts(OPTS, group='collector')

class SampleEndpoint(object):
    def __init__(self):
        self.services = cfg.CONF.collector.services
        self.manager = manager.DispatchManager(
            self.services)

    # this used to test
    def info(self, messages):
        try:
            self.manager.dispatch(messages)
        except Exception:
            return oslo_messaging.NotificationResult.REQUEUE
        #add exception requeue



