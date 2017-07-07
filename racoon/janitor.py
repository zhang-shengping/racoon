#!/usr/bin/env python
# encoding: utf-8

import cotyledon
import threading

from racoon.storage import connection

from oslo_config import cfg
from oslo_log import log
from oslo_utils import timeutils

CONF = cfg.CONF

LOG = log.getLogger(__name__)


class JanitorService(cotyledon.Service):

    def __init__(self, worker_id):
        super(JanitorService, self).__init__(worker_id)
        # this will keep set boolean atomic
        self.__shutdown = threading.Event()
        self.__shutdown_done = threading.Event()
        self.delay = cfg.CONF.collector.janitor_delay

    def run(self):
        while not self.__shutdown.is_set():
            with timeutils.StopWatch() as timer:
                # run job needs time
                self._run_job()
                # therefore janitor_delay - time used by run job
                self.__shutdown.wait(max(0, self.delay -
                                         timer.elapsed()))
        self.__shutdown_done.set()

    def _run_job(self):
        LOG.info('janitor clean resources')
        con = connection.get_conn_from_config(CONF)
        # get start and end time
        con.del_resource_by_duration(1)

    def terminate(self):
        self.__shutdown.set()
        LOG.info("Waiting ongoing processing to finish")
        self.__shutdown_done.wait()

if __name__ == "__main__":
    from racoon import service
    service.prepare_service()
    cs = JanitorService(1)
    cs.run()

