#!/usr/bin/env python
# encoding: utf-8

import oslo_messaging

from racoon import dispatcher as disp

class SampleEndpoint(object):
    def __init__(self, manager=None):
        self.manager = manager
        # 先加载一个 manager 包含多个模块
        # 然后从manager 中选取不同对象。
        self.dispatcher = disp.DispatcherBase()

    # this used to test
    def info(self, messages):
        try:
            self.dispatcher.dispatch(messages)
        except Exception:
            return oslo_messaging.NotificationResult.REQUEUE
        print 'end'

        #add exception requeue



