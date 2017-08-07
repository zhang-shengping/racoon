#!/usr/bin/env python
# encoding: utf-8

import datetime

from oslo_config import cfg

from racoon import service
from racoon.storage.connection import Connection
from racoon.storage import models


# this is a global variable, always get the same CONF
# I can get all variable, as long as I register it
# before I query it. It can be register anywhere.
# every oslo with options.set_defaults method.
# The values in configuration filea can be assigned
# to CONF, as long as I call cfg.CONF(project=)
CONF = cfg.CONF


def get_resources():
    service.prepare_service()
    url = CONF.database.connection
    conn = Connection(url)
    start = '2017-07-26 08:37:00'
    end = '2017-07-31 00:51:00'
    tformat = '%Y-%m-%d %H:%M:%S'

    delay = datetime.timedelta(seconds=10)
    start_time = datetime.datetime.strptime(start, tformat)
    end_time = datetime.datetime.strptime(end, tformat)
   
    print 'end'
    print end_time + delay
    
    
    #resources = conn.get_resource_by_duration(start, end)
    #for x in [resource.end_timestamp for resource in resources]:
    #    print x


if __name__ == '__main__':
    get_resources()
