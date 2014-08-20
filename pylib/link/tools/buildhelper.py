#!/usr/bin/env python

from functools import partial
from maya import cmds
from link.modules.parts import fk, ik, ikfk
from link.util import python

class PartTests(object):
    def __init__(self):
        self.setup_ui()

    def setup_ui(self):
        cls = self.__class__.__name__
        if cmds.window(cls, q=True, ex=True):
            cmds.deleteUI(cls)

        win = cmds.window(cls, s=False, tlb=True, title=cls, iconName='Short Name')

        cmds.columnLayout(win, adj=True)

        # Parts
        cmds.button(label="FkChain", w=100, c=self.test_FkChain)
        cmds.button(label="IkRp", w=100, c=self.test_FIkRp)
        cmds.button(label="IkFk", w=100, c=self.test_FIkFk)

    def test_FkChain(self, *args):
        fk.FkChain("L", "arm").test_create()

    def test_FIkRp(self, *args):
        ik.IkRp("L", "arm").test_create()

    def test_FIkFk(self, *args):
        ikfk.IkFk("L", "arm").test_create()

    def show(self):
        cmds.showWindow(self.__class__.__name__)
