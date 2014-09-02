#!/usr/bin/env python

"""
Settings node file handling
"""

import os
import json
import logging
from maya import cmds

from link.util.io.base import FileHandler
from link.config import Config

log = logging.getLogger(__name__)

"""
Example use:

h = SettingsFileHandler('data/settings/L_foot_0.json')
h.init_data("L_foot_0_settingsShape")
h.write()

h.read()

h.eval()
"""

class SettingsFileHandler(FileHandler):

    def __init__(self, relative_path):
        super(SettingsFileHandler, self).__init__(relative_path)

    def init_data(self, node):
        """
        Scan node for user defined attrs. Store settings node
        and all attrs and values.
        """

        attrs = cmds.listAttr(node, ud=True)

        data = {}
        data['node'] = node
        for attr in attrs:
            data['attrs'] = [attr, cmds.getAttr("%s.%s" % (node, attr))]

        self.set_data(data)

    def eval(self):
        """
        Try restore all settings back onto node if exist
        and not connected.
        """

        data = self.read()

        node = data['node']
        attrs = data['attrs']

        for attr_value in attrs:
            attr, value = attr_value
            full_path = "%s.%s" % (node, attr)

            if cmds.objExists(full_path):
                if not cmds.listConnections(full_path, source=True, d=False) or []:
                    cmds.setAttr(full_path, value)

