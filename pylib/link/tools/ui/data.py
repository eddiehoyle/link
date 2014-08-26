#!/usr/bin/env python

"""
"""

from maya import cmds
from link.util.io.base import FileHandler

class DataManager(object):
    def __init__(self):
        self.setup_ui()

    def setup_ui(self):
        cls = self.__class__.__name__
        if cmds.window(cls, q=True, ex=True):
            cmds.deleteUI(cls)

        win = cmds.window(cls, s=False, tlb=True, title=cls, iconName='Short Name')

        cmds.columnLayout(win, adj=True)

        # Simple save and load
        cmds.button(label="Save", w=100, c=self.save_selected)
        cmds.button(label="Load", w=100, c=self.load_selected)

    def save_selected(self, *args):
        data = self._get_data(cmds.ls(sl=1))
        f = FileHandler("foot")
        f.write(data)

    def load_selected(self, *args):
        f = FileHandler("foot")
        data = f.read()
        for key, vector in data.items():
            cmds.setAttr("%s.translate" % key, *vector, type="float3")

    def _get_data(self, transforms):
        data = {}
        for node in transforms:
            data[node] = cmds.xform(node, q=True, t=True, ws=True)
        return data

    def show(self):
        cmds.showWindow(self.__class__.__name__)
