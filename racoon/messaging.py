#!/usr/bin/env python
# encoding: utf-8

from oslo_config import cfg
import oslo_messaging

DEFAULT_URL = "__default__"
TRANSPORTS = {}


def setup():
    oslo_messaging.set_transport_defaults('racoon')


def get_transport(url=None, cache=True):
    """Initialise the oslo_messaging layer."""
    global DEFAULT_URL, TRANSPORTS
    cache_key = url or DEFAULT_URL
    transport = TRANSPORTS.get(cache_key)
    if not transport:
        try:
            transport = oslo_messaging.get_notification_transport(
                cfg.CONF, url)
        except Exception:
            raise
        else:
            if cache:
                TRANSPORTS[cache_key] = transport
    return transport


def get_event_listener(transport, targets, endpoints,
                       allow_requeue=False,
                       batch_size=1, batch_timeout=None):
    # change blocking to threading later
    return oslo_messaging.get_batch_notification_listener(
        transport, targets, endpoints, executor='blocking',
        allow_requeue=allow_requeue,
        batch_size=batch_size, batch_timeout=batch_timeout)


def get_targets(topics=['event']):
    targets = [oslo_messaging.Target(topic=_topic)
               for _topic in topics]
    return targets


if __name__ == "__main__":
    from racoon import service
    service.prepare_service()
    transport = get_transport()
