#!/usr/bin/env python

"""
"""

from link.util.control.control import Control
from maya import cmds
from link.build.modules.parts.part import Part

class Simple(Part):
    '''Basic Simple control with no hierarchy'''

    def __init__(self, position, description):
        super(Simple, self).__init__(position, description)

    def create_controls(self):
        """Create controls"""

        for index, joint in enumerate(self.joints):
            ctl = Control(self.position, self.description, index)
            ctl.create()
            ctl.set_style("square")
            ctl.joint = joint

            # Lock attrs
            ctl.lock_vis()

            # Append control
            self.controls[ctl.name] = ctl

        return self.controls

    def test_create(self):
        cmds.file(new=True, force=True)

        joints = joint.create_chain(1, 'X', 3)
        self.set_joints(joints)
        self.create()


