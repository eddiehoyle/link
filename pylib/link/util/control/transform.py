#!/usr/bin/env python

from maya import cmds

class Transform(object):
    """
    """

    def __init__(self, name):
        self.name = name
        self.node = None

    def create(self):
        self.node = cmds.createNode("transform", name=self.name)
