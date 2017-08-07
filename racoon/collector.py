#!/usr/bin/env python
# encoding: utf-8

import cotyledon
from oslo_config import cfg
from oslo_log import log

from racoon import endpoint
from racoon import messaging

LOG = log.getLogger(__name__)


class CollectorService(cotyledon.Service):

    def __init__(self, worker_id):
        super(CollectorService, self).__init__(worker_id)
        self.event_listener = None

    def run(self):
        transport = messaging.get_transport()
        if transport:
            event_targets = messaging.get_targets(
                cfg.CONF.oslo_messaging_notifications.topics
            )
            self.event_listener = messaging.get_event_listener(
                transport, event_targets,allow_requeue=True, 
                [endpoint.SampleEndpoint()]
            )
            LOG.info('start event listener')
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
