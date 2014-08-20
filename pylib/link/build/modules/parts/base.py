#!/usr/bin/env python

"""
"""

from link import util
from link.util.control.control import Control
from maya import cmds
from link.build.modules.parts.simple import Simple

class Base(Simple):
    '''Basic FK control with no hierarchy'''

    def __init__(self, position, description):
        super(Base, self).__init__(position, description)

    def create_controls(self):
        """Create controls"""

        top_ctl = Control("C", "global", 0)
        top_ctl.create()
        top_ctl.set_style("square")
        top_ctl.lock_scales()

        sec_ctl = Control("C", "global", 1)
        sec_ctl.create()
        sec_ctl.set_style("square")
        sec_ctl.lock_scales()

        cmds.parent(sec_ctl.grp, top_ctl.ctl)

        return self.controls

    def connect_controls(self):
        pass

    def match_controls(self):
        pass


    def test_create(self):
        cmds.file(new=True, force=True)

        self.create()
