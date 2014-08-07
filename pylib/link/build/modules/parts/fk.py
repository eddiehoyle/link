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
            for attr in ["translate", "rotate"]:
                count = 0
                pma = cmds.createNode("plusMinusAverage")
                for axis in ["X", "Y", "Z"]:
                    val = cmds.getAttr("%s.%s%s" % (fk_jnt, attr, axis))

                    # # Determine if positive or negative
                    # child_translateX = cmds.xform(src_jnt, q=True, ws=True, t=True)[0]
                    # mult = 1
                    # if child_translateX < 0:
                    #     mult = -1

                    cmds.connectAttr("%s.%s%s" % (ctl.ctl, attr, axis), "%s.input3D[%s].input3D%s" % (pma, count, axis.lower()))
                    cmds.setAttr("%s.input3D[%s].input3D%s" % (pma, count + 1, axis.lower()), val)
                    cmds.connectAttr("%s.output3D.output3D%s" % (pma, axis.lower()), "%s.%s%s" % (fk_jnt, attr, axis))

                # Add pma to control class
                setattr(ctl, "pma_%s" % attr, pma)

                count += 1
            
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
            cmds.parent(ctl.grp, self.top_node)

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

                cmds.addAttr(ctl.ctl, ln="length", at="double", min=0, dv=1)
                cmds.setAttr("%s.length" % ctl.ctl, cb=True)
                cmds.setAttr("%s.length" % ctl.ctl, k=True)

                distance = common.get_distance(ctl.ctl, child_ctl.ctl)

                # Get save connection index for translate
                safe_translate_index = 0
                while cmds.listConnections("%s.input3D[%s].input3Dx" % (child_ctl.pma_translate, safe_translate_index), s=1, d=0, p=1):
                    safe_translate_index += 1
                    cmds.listConnections("%s.input3D[%s].input3Dx" % (child_ctl.pma_translate, safe_translate_index), s=1, d=0, p=1)

                # Determine if positive or negative
                child_translateX = cmds.xform(child_ctl.joint, q=True, ws=True, t=True)[0]
                mult = 1
                if child_translateX < 0:
                    mult = -1

                # Normailise the length attribute
                dst_mlt = cmds.createNode("multiplyDivide", name=name.set_suffix(ctl.name, "dstMlt"))
                cmds.connectAttr("%s.length" % ctl.ctl, "%s.input1X" % dst_mlt)
                cmds.setAttr("%s.input2X" % dst_mlt, distance * mult)

                # Connect to joint and ctl grp
                cmds.connectAttr("%s.outputX" % dst_mlt, "%s.input3D[%s].input3Dx" % (child_ctl.pma_translate, safe_translate_index))
                cmds.connectAttr("%s.outputX" % dst_mlt, "%s.translateX" % child_ctl.grp)

    def test_create(self):
        cmds.file(new=True, force=True)
        jnts = joint.create_chain(4, 'X', -3)

        self.set_joints(jnts)
        self.create()
        self.rotate_shapes([0, 0, 90])
        self.add_stretch()


