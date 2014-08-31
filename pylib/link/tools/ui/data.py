#!/usr/bin/env python

"""
"""

from maya import cmds
from link.util.io.part import PartFileHandler
from link.util.io.settings import SettingsFileHandler
import logging
log = logging.getLogger(__name__)

class PartDataManager(object):
    def __init__(self):
        self.setup_ui()

    def setup_ui(self):
        cls = self.__class__.__name__
        if cmds.window(cls, q=True, ex=True):
            cmds.deleteUI(cls)

        win = cmds.window(cls, s=False, tlb=True, title=cls, iconName='Short Name')

        cmds.columnLayout(win, adj=True)

        # Simple save and load
        cmds.textField('key_field', w=100, text="L_foot_0")
        cmds.button(label="Save Part", w=100, c=self.save_selected_part)
        cmds.button(label="Load Part", w=100, c=self.load_selected_part)
        cmds.separator()
        cmds.button(label="Save Settings", w=100, c=self.save_selected_settings)
        cmds.button(label="Load Settings", w=100, c=self.load_selected_settings)

    # --------------------------------------------------------------------- #
    # Parts
    # --------------------------------------------------------------------- #

    def save_selected_part(self, *args):
        data = self._get_part_data(cmds.ls(sl=1))
        key = self._get_key()
        PartFileHandler(key).write(data)

    def load_selected_part(self, *args):
        key = self._get_key()
        data = PartFileHandler(key).read()
        for key, vector in data.items():
            cmds.setAttr("%s.translate" % key, *vector, type="float3")

    # --------------------------------------------------------------------- #
    # Settings
    # --------------------------------------------------------------------- #

    def save_selected_settings(self, *args):
        settings_node = cmds.ls(sl=1)
        if settings_node:
            data = self._get_settings_data(settings_node[0])
            key = self._get_key()
            SettingsFileHandler(key).write(data)

    def load_selected_settings(self, *args):
        key = self._get_key()
        data = SettingsFileHandler(key).read()
        for full_attr, value in data.items():
            cmds.setAttr(full_attr, value)

    # --------------------------------------------------------------------- #
    # Collections
    # --------------------------------------------------------------------- #

    def _get_part_data(self, transforms):
        data = {}
        for node in transforms:
            data[node] = cmds.xform(node, q=True, t=True, ws=True)
        return data

    def _get_settings_data(self, settings_node):
        data = {}
        attrs = cmds.listAttr(settings_node, ud=True)
        for attr in attrs:
            key = "%s.%s" % (settings_node, attr)
            data[key] = cmds.getAttr("%s.%s" % (settings_node, attr))
        return data

    def _get_key(self):
        key = cmds.textField('key_field', q=True, text=True)
        if not key:
            raise ValueError("No part key")
        print 'key', key
        return key

    def show(self):
        cmds.showWindow(self.__class__.__name__)
