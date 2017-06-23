#!/usr/bin/env python
# encoding: utf-8

class SampleEndpoint(object):
    def __init__(self, manager=None):
        self.manager = manager

    def sample(self, messages):
        print messages
        print

    # this used to test
    def info(self, messages):
        print messages
        print

