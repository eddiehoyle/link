#!/usr/bin/env python

"""
"""

from maya import cmds
from link.util.io.part import PartFileHandler
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
        self.part_field = cmds.textField(w=100, text="L_foot_0")
        cmds.button(label="Save Part", w=100, c=self.save_selected)
        cmds.button(label="Load Part", w=100, c=self.load_selected)

    def save_selected(self, *args):
        data = self._get_data(cmds.ls(sl=1))
        key = self._get_key()
        f = PartFileHandler(key)
        f.write(data)

    def load_selected(self, *args):
        key = self._get_key()
        f = PartFileHandler(key)
        data = f.read()
        for key, vector in data.items():
            cmds.setAttr("%s.translate" % key, *vector, type="float3")

    def _get_data(self, transforms):
        data = {}
        for node in transforms:
            data[node] = cmds.xform(node, q=True, t=True, ws=True)
        return data

    def _get_key(self):
        key = cmds.textField(self.part_field, q=True, text=True)
        if not key:
            raise ValueError("No part key")
        return key

    def show(self):
        cmds.showWindow(self.__class__.__name__)
