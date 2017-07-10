#!/usr/bin/env python
# encoding: utf-8

import threading

import cotyledon
from oslo_config import cfg
from oslo_log import log

from racoon import collector
from racoon import service
from racoon import janitor

CONF = cfg.CONF
LOG = log.getLogger(__name__)


def main():
    service.prepare_service()
    sm = cotyledon.ServiceManager()
    sm.add(collector.CollectorService, workers=CONF.collector.worker)
    sm.add(janitor.JanitorService, workers=1)
    sm.run()


if __name__ == "__main__":
    main()
