#!/usr/bin/env python
# encoding: utf-8

from oslo_config import cfg
from oslo_log import log

from racoon import messaging

LOG = log.getLogger(__name__)
COLL_WORKER = cfg.IntOpt('worker',
                         default=1,
                         min=1)

cfg.CONF.register_opt(COLL_WORKER, 'collector')


def prepare_service():
    log.register_options(cfg.CONF)
    log_level = cfg.CONF.default_log_levels
    log.set_defaults(
        default_log_levels=log_level
    )

    cfg.CONF(project='racoon')

    log.setup(cfg.CONF, 'raccon')
    messaging.setup()
    LOG.info('initiated services')
