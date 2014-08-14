#!/usr/bin/env python

from link.util import name, xform, joint
from link.util import common, vector, joint
from link.util.control.control import Control
from link import util
from maya import cmds
from link.build.modules.parts.part import Part
import logging
logger = logging.getLogger(__name__)

class IkSc(Part):
    '''Ik single chain solver with no pole vector'''

    def __init__(self, position, description):
        super(IkSc, self).__init__(position, description)

        self.description = "%sIk" % description
        self.name = name.set_description(self.name, self.description)

        # Important nodes
        self.ik = None
        self.effector = None

        # Important ctls
        self.polevector_ctl = None
        self.ik_ctl = None

        # Ik joints
        self.ik_joints = []

    def _duplicate_joints(self):
        """Create a duplicate FK joint chain to drive rig"""

        # Create new joints
        self.ik_joints = util.joint.duplicate_joints(self.joints, "ik")

        # Connect fk jnts to source joints
        for ik_jnt, src_jnt in zip(self.ik_joints, self.joints):
            cmds.parentConstraint(ik_jnt, src_jnt, mo=True)

    def create_ik(self):
        """Ik handle"""

        start_joint, end_joint = self.ik_joints[0], self.ik_joints[-1]
        logger.info("Creating Ik using nodes: %s" % self.joints)
        self.ik, self.effector = cmds.ikHandle(sj=start_joint, ee=end_joint, sol="ikSCsolver")

    def create_controls(self):
        """Create controls"""

        # Make duplicate joint chain
        self._duplicate_joints()

        # Create ikHandle
        self.create_ik()
        
        # Create control
        ik_ctl = Control(self.position, self.description, 0)
        ik_ctl.create()

        # Style and lock attrs
        ik_ctl.set_style("cube")
        ik_ctl.lock_scales()

        # Create control
        base_ctl = Control(self.position, self.description, 1)
        base_ctl.create()

        # Append control
        self.controls[ik_ctl.name] = ik_ctl
        self.controls[base_ctl.name] = base_ctl
        self.ik_ctl = ik_ctl
        self.base_ctl = base_ctl

        return self.controls

    def match_controls(self):
        """Ik only has a single control"""

        # Match IK Handle to end joint
        xform.match_translates(self.ik_ctl.grp, self.ik_joints[-1])
        xform.match_translates(self.base_ctl.grp, self.ik_joints[0])

        # Apply orient offset if found to ik control
        orient_offset = self.offset.get("orient", {})
        if orient_offset:
            self.ik_ctl.set_orient_offset(orient_offset['vector'], orient_offset['world'])

        # Apply point offset if found to ik control
        point_offset = self.offset.get("point", {})
        if point_offset:
            self.ik_ctl.set_point_offset(point_offset['vector'], point_offset['world'])

    def connect_controls(self):

        # Parent IK handle under ctl
        cmds.parent(self.ik, self.ik_ctl.ctl)

        # Ik ctl
        self.ik_ctl.joint = self.ik_joints[-1]
        con = cmds.orientConstraint(self.ik_ctl.ctl, self.ik_ctl.joint, mo=True)[0]
        cmds.setAttr("%s.interpType" % con, 2)

        # Base ctl
        self.base_ctl.joint = self.ik_joints[0]
        con = cmds.pointConstraint(self.base_ctl.ctl, self.base_ctl.joint, mo=True)[0]

    def add_stretch(self):
        """Drive ik_joints by translateX and distance between start and end"""

        # Create distance
        loc_start, loc_end, dst_node = common.create_distance(self.ik_joints[0], self.ik_joints[-1])
        distance = cmds.getAttr("%s.distance" % dst_node)

        # Create stretch multiplier
        div_mlt = cmds.createNode("multiplyDivide", name=name.set_suffix(self.name, "divMlt"))
        cmds.connectAttr("%s.distance" % dst_node, "%s.input1X" % div_mlt)
        cmds.setAttr("%s.operation" % div_mlt, 2)

        # Create condition logic
        cond = cmds.createNode("condition")
        cmds.setAttr("%s.operation" % cond, 4)
        cmds.setAttr("%s.colorIfTrueR" % cond, 1)
        cmds.setAttr("%s.colorIfFalseR" % cond, 0)
        cmds.setAttr("%s.colorIfFalseR" % cond, distance)
        cmds.setAttr("%s.secondTerm" % cond, distance)

        cmds.connectAttr("%s.distance" % dst_node, "%s.firstTerm" % cond)
        cmds.connectAttr("%s.distance" % dst_node, "%s.colorIfTrueR" % cond)
        cmds.connectAttr("%s.outColorR" % cond, "%s.input2X" % div_mlt)

        # Detect positive or negative X value
        end_x = cmds.getAttr("%s.translateX" % self.joints[-1])
        mult = 1
        if end_x < 0:
            mult = -1

        # Parent dst locs
        cmds.parent(loc_end, self.ik_ctl.ctl)
        cmds.parent(loc_start, self.base_ctl.ctl)

        for ik_jnt, src_jnt in zip(self.ik_joints[:-1], self.joints):

            # Scale ik joints
            cmds.connectAttr("%s.outputX" % div_mlt, "%s.scaleX" % ik_jnt)

            # Connect ik to source joints
            cmds.connectAttr("%s.scaleX" % ik_jnt, "%s.scaleX" % src_jnt)

    def add_settings(self):
        super(IkSc, self).add_settings()
        cmds.connectAttr("%s.helpers" % self.settings_node, "%s.visibility" % self.ik)

    def test_create(self):
        cmds.file(new=True, force=True)

        joints = joint.create_chain(3, 'X', -4)

        self.set_joints(joints)
        self.create()


class IkRp(IkSc):
    '''Ik rotate plane control with polevector'''

    def __init__(self, position, description):
        super(IkRp, self).__init__(position, description)

    def _create(self):
        super(IkRp, self)._create()
        self.add_polevector(offset=[0, 0, 4])

    def create_ik(self):
        """Ik handle"""

        start_joint, end_joint = self.ik_joints[0], self.ik_joints[-1]
        logger.info("Creating Ik using nodes: %s" % self.joints)
        self.ik, self.effector = cmds.ikHandle(sj=start_joint, ee=end_joint, sol="ikRPsolver")

    def add_polevector(self, description=None, offset=[0, 0, 0]):
        """Add pole vector for ikHandle"""

        description = description or util.name.get_description(util.name.set_description_suffix(self.ik_ctl.ctl, "pv"))
        
        # Create control
        ctl = Control(self.position, description)
        ctl.create()
        ctl.set_style("pyramid")

        ctl.lock_rotates()
        ctl.lock_scales()

        # TODO
        # Create aim
        # for axis in ["X", "Y", "Z"]:
        #     cmds.setAttr("%s.rotate%s" % (ctl.ctl, axis), k=False, cb=False)

        # Find center of ik handle
        start_pos = cmds.xform(self.ik_joints[0], q=1, t=1, ws=1)
        end_pos = cmds.xform(self.ik_joints[-1], q=1, t=1, ws=1)
        middle_pos = vector.average_3f(start_pos, end_pos)
        middle_pos = vector.add_3f(middle_pos, offset)

         # Find center of ik handle
        start_rot = cmds.xform(self.ik_joints[0], q=1, ro=1, ws=1)
        end_rot = cmds.xform(self.ik_joints[-1], q=1, ro=1, ws=1)
        middle_rot = vector.average_3f(start_rot, end_rot)

        # Move into position
        cmds.xform(ctl.grp, t=middle_pos, ws=True)

        # Create poleVector
        cmds.poleVectorConstraint(ctl.ctl, self.ik, weight=True)

        # Add annotation
        mid_jnt = self.ik_joints[(len(self.ik_joints)-1)/2]
        util.anno.aim(ctl.ctl, mid_jnt, "pv")

        self.pv_ctl = ctl
        self.controls[ctl.name] = ctl

    def test_create(self):
        super(IkRp, self).test_create()

        self.pv_ctl.rotate_shapes([-90, 0, 0])
        self.pv_ctl.scale_shapes(0.5)
        self.base_ctl.rotate_shapes([0, 0, 90])
        self.add_stretch()
