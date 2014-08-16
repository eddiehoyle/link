#!/usr/bin/env python

from link.util import name, xform, constraint
from link.util import common, joint
from link import util
from link.util.control.control import Control
from maya import cmds
from link.build.modules.parts.simple import Simple

import logging
log = logging.getLogger(__name__)

class FkChain(Simple):
    """Hierarchical FK chain"""

    def __init__(self, position, description):
        super(FkChain, self).__init__(position, description)

        self.description = "%sFk" % description
        
        # Fk joints
        self.fk_joints = []

    def _duplicate_joints(self):
        """Create a duplicate FK joint chain to drive rig"""

        # Create new joints
        self.fk_joints = util.joint.duplicate_joints(self.joints, "fk")

        # Add to setups
        self.setups.extend(self.fk_joints)

    def create_controls(self):
        """Create controls"""

        # Create duplicate joint chain
        self._duplicate_joints()

        # Create simple controls
        super(FkChain, self).create_controls()

        for key, ctl in self.controls.items():
            ctl.set_style("circle")

            ctl.lock_translates()
            ctl.lock_scales()

        return self.controls

    def connect_controls(self):
        """Connect controls"""

        # Connect controls to fk joints
        for key, src_jnt, fk_jnt in zip(self.controls.keys(), self.joints, self.fk_joints):

            ctl = self.controls[key]
            cmds.orientConstraint(ctl.ctl, fk_jnt, mo=True)
            
            con = cmds.parentConstraint(fk_jnt, src_jnt, mo=True)
            cmds.setAttr("%s.interpType" % con[0], 2)

            # Store attrs
            ctl.fk_joint = fk_jnt
            ctl.joint = src_jnt
            ctl.constraint = con[0]

    def omit_last_control(self):
        """Delete last control"""

        if self.controls:
            last = self.get_control(-1)
            log.warning("Omitting last FK control: %s" % last.name)
            cmds.delete(last.grp)
            del self.controls[last.name]

    def parent_controls(self):
        """Hierarchy"""

        for key, ctl in self.controls.items():
            index = name.get_index(key)
            child_ctl = self.controls.get(name.set_index(key, index + 1), None)
            if child_ctl:
                cmds.parent(child_ctl.grp, ctl.ctl)

    def add_stretch(self):
        """Stretch is driven by translateX in object space of transform"""

        # Create chain
        for key, ctl in self.controls.items():

            # Try get child control
            index = name.get_index(key)
            child_ctl = self.controls.get(name.set_index(key, index + 1), None)
            if child_ctl:

                # Add attrs
                cmds.addAttr(ctl.ctl, ln="length", at="double", min=0, dv=1)
                cmds.setAttr("%s.length" % ctl.ctl, cb=True)
                cmds.setAttr("%s.length" % ctl.ctl, k=True)

                # Connect to ctl jnt
                div_mlt = cmds.createNode("multiplyDivide", name=name.set_suffix(ctl.name, "divMlt"))
                cmds.connectAttr("%s.length" % ctl.ctl, "%s.input1X" % div_mlt)
                cmds.setAttr("%s.input2X" % div_mlt, 1)
                cmds.setAttr("%s.operation" % div_mlt, 2)
                cmds.connectAttr("%s.outputX" % div_mlt, "%s.scaleX" % ctl.fk_joint)

                # Detect positive or negative X value
                end_x = cmds.getAttr("%s.translateX" % self.joints[-1])
                mult = 1
                if end_x < 0:
                    mult = -1

                # Connect to child ctl grp
                distance = common.get_distance(ctl.ctl, child_ctl.ctl)
                grp_mlt = cmds.createNode("multiplyDivide", name=name.set_suffix(ctl.name, "grpMlt"))
                cmds.connectAttr("%s.length" % ctl.ctl, "%s.input1X" % grp_mlt)
                cmds.setAttr("%s.input2X" % grp_mlt, distance * mult)
                cmds.connectAttr("%s.outputX" % grp_mlt, "%s.translateX" % child_ctl.grp)

                # Directly connect FK joint to source joint
                cmds.connectAttr("%s.scaleX" % ctl.fk_joint, "%s.scaleX" % ctl.joint)

    def test_create(self):
        cmds.file(new=True, force=True)
        jnts = joint.create_chain(4, 'X', -3)

        self.set_joints(jnts)
        self.create()
        self.rotate_shapes([0, 0, 90])
        self.add_stretch()


