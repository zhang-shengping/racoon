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
        LOG.info('collect services: %s', self.services)
        self.manager = manager.DispatchManager(
            self.services)

    # this used to test
    def info(self, messages):
        try:
            # if the message is not the right type
            # it wont requeue and raise Exception
            # only if the message is right type
            # and something wrong it raise exception
            self.manager.dispatch(messages)
        except Exception:
            for m in messages:
                LOG.info('can not dispatch event %s',
                         m.get('event_type'))
                # cant see what exception
                # even do this
                # raise err

            # requeue the right type event
            return oslo_messaging.NotificationResult.REQUEUE
