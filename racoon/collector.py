#!/usr/bin/env python
# encoding: utf-8

import cotyledon
from oslo_config import cfg
from oslo_log import log
import oslo_messaging

from racoon import dispatcher
from racoon import endpoint
from racoon import messaging

import time

LOG = log.getLogger(__name__)

class CollectorService(cotyledon.Service):
    """Listener to notification service"""
    def __init__(self, worker_id):
        super(CollectorService, self).__init__(worker_id)
        #dispatcher_managers = dispatcher.()
        self.event_listener = None

    def run(self):
        transport = messaging.get_transport()
        if transport:
            event_targets = messaging.get_targets(
                cfg.CONF.oslo_messaging_notifications.topics
            )
            self.event_listener = messaging.get_event_listener(
                transport, event_targets, [endpoint.SampleEndpoint()]
            )
            self.event_listener.start()

    def terminate(self):
        """
        kill listener
        """
        if self.event_listener:
            self.event_listener.stop()
            self.event_listener.wait()
        super(CollectorService, self).terminate()

if __name__ == "__main__":
    from racoon import service
    service.prepare_service()
    cs = CollectorService(1)
    cs.run()
