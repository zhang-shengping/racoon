#!/usr/bin/env python
# encoding: utf-8

import datetime
import cotyledon
import threading

from racoon.storage import connection

from oslo_config import cfg
from oslo_log import log
from oslo_utils import timeutils

CONF = cfg.CONF

LOG = log.getLogger(__name__)


# 自开始，每个小时选一次，选在一个小时前中存在或者创建的数据
# 即 end_timestamp == Nonne, end_timestamp >= now - one_hour_ago
# 分类，分发 (分发的值给设置的start timestamp 为一个小时前，结束的时间为现在)
# 注意这里不存在漏掉的问题，漏掉也是在当前时间刚刚创建的消息。
# 可以考虑加 1 秒的偏移值
class SearcherService(cotyledon.Service):

    def __init__(self, worker_id):
        super(SearcherService, self).__init__(worker_id)
        # this will keep set boolean atomic
        self.__shutdown = threading.Event()
        self.__shutdown_done = threading.Event()
        self.delay = cfg.CONF.collector.searcher_delay

    def run(self):
        while not self.__shutdown.is_set():
            with timeutils.StopWatch() as timer:
                # therefore self.delay - time used by run job
                self.__shutdown.wait(max(0, self.delay -
                                         timer.elapsed()))
                # wait a while then collect
                self._run_job()

        self.__shutdown_done.set()

    def _run_job(self):
        LOG.info('search resources')
        con = connection.get_conn_from_config(CONF)
        # get start and end time
        end_timestamp = self._get_past()
        resources = con.get_resource_by_timestamp(end_timestamp)
        for r in resources:
            print r.resource_id
        print len(resources)

    def _get_past(self):
        start = datetime.datetime.utcnow()
        end = start - datetime.timedelta(
            seconds=self.delay)
        # end = end.strftime('%Y-%m-%dT%H:%M:%SZ')
        end = end.strftime('%Y-%m-%d %H:%M:%S')
        return end

    def terminate(self):
        self.__shutdown.set()
        LOG.info("Waiting ongoing processing to finish")
        self.__shutdown_done.wait()

if __name__ == "__main__":
    from racoon import service
    service.prepare_service()
    cs = SearcherService(1)
    cs.run()

