#!/usr/bin/env python
# encoding: utf-8

from oslo_config import cfg
from oslo_log import log

from racoon import messaging

CONF = cfg.CONF
LOG = log.getLogger(__name__)

OPTS = [
    cfg.IntOpt('worker',
               default=1,
               min=1),

    cfg.IntOpt('janitor_delay',
               default = 7200),
]

CONF.register_opts(OPTS, 'collector')

def prepare_service():
    log.register_options(CONF)
    log_level = CONF.default_log_levels
    log.set_defaults(
        default_log_levels=log_level
    )

    CONF(project='racoon')

    log.setup(CONF, 'raccon')
    messaging.setup()
    LOG.info('initiated services')
