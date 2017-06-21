#!/usr/bin/env python
# encoding: utf-8

import cotyledon
from oslo_config import cfg

from racoon import collector
from racoon import service

CONF = cfg.CONF

def main():
    service.prepare_service()
    sm = cotyledon.ServiceManager()
    sm.add(collector.CollectorService, workers=CONF.collector.worker)
    sm.run()


if __name__ == "__main__":
    main()
