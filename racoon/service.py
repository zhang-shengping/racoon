#!/usr/bin/env python
# encoding: utf-8

from oslo_config import cfg
from oslo_log import log

from racoon import messaging

COLL_WORKER = cfg.IntOpt('worker',
                         default=1,
                         min=1)

cfg.CONF.register_opt(COLL_WORKER, 'collector')

def prepare_service():

    log.register_options(cfg.CONF)

    cfg.CONF(project='racoon')
    messaging.setup()


