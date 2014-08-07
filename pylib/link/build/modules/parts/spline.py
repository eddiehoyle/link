#!/usr/bin/env python

from link.util import name, xform, joint
from link.util import common, vector, joint
from link.util.control.control import Control
from link import util
from maya import cmds
from link.build.modules.parts.part import Part
from collections import OrderedDict
import logging
logger = logging.getLogger(__name__)

class IkSpline(Part):
    '''Ik single chain solver with no pole vector'''

    def __init__(self, position, description):
        super(IkSpline, self).__init__(position, description)

        self.name = name.set_description(self.name, self.description)

        # Important nodes
        self.ik = None
        self.effector = None
        self.curve = None

        # Ik specific control dict
        self.ik_controls = OrderedDict()

    def _duplicate_joints(self):
        # Create new joints
        self.ik_joints = util.joint.duplicate_joints(self.joints, "ik")

        # Connect fk jnts to source joints
        for ik_jnt, src_jnt in zip(self.ik_joints, self.joints):
            cmds.parentConstraint(ik_jnt, src_jnt, mo=True)

    def create_ik(self):
        """Ik spline"""

        start_joint, end_joint = self.ik_joints[0], self.ik_joints[-1]
        logger.info("Creating Ik using nodes: %s" % self.joints)
        self.ik, self.effector, self.curve = cmds.ikHandle(sj=start_joint, ee=end_joint, sol="ikSplineSolver", ns=3)

        # Turn on cvs
        cmds.select(self.curve, r=True)
        cmds.toggle(cv=True)

        # Create clusters
        clusters = OrderedDict()
        clusters['bot'] = cmds.cluster(["%s.cv[0]" % self.curve, "%s.cv[1]" % self.curve])[1]
        clusters['mid'] = cmds.cluster(["%s.cv[2]" % self.curve, "%s.cv[3]" % self.curve])[1]
        clusters['top'] = cmds.cluster(["%s.cv[4]" % self.curve, "%s.cv[5]" % self.curve])[1]
        
        util.xform.match_pivot(start_joint, clusters['bot'])
        util.xform.match_pivot(end_joint, clusters['top'])


        self.clusters = clusters

    def create_controls(self):
        
        # Make duplicate joint chain
        self._duplicate_joints()

        # Create ikHandle
        self.create_ik()

        # Create controls
        index = 0
        for cls_key, cls_node in self.clusters.items():
            ctl = Control(self.position, self.description, index)
            ctl.create()
            self.controls[ctl.name] = ctl

            # Store Ik controls for easy reference
            self.ik_controls[cls_key] = ctl

            # Store cluster
            ctl.cluster = cls_node

            index += 1

    def match_controls(self):

        bot_ctl = self.ik_controls['bot']
        mid_ctl = self.ik_controls['mid']
        top_ctl = self.ik_controls['top']

        util.xform.match_translates(bot_ctl.grp, self.joints[0])
        util.xform.match_translates(top_ctl.grp, self.joints[-1])

        # Get mid position
        util.xform.match_average_position(mid_ctl.grp, [top_ctl.grp, bot_ctl.grp])

    def connect_controls(self):        
        for key, ctl in self.controls.items():
            cmds.parent(ctl.cluster, ctl.ctl)

        cmds.orientConstraint(self.ik_controls['top'].ctl, self.ik_joints[-1], mo=True)

    def parent_controls(self):
        pass

    def add_stretch(self):
        arc = cmds.createNode("curveInfo")
        crv_shape = cmds.listRelatives(self.curve, shapes=True)[0]
        cmds.connectAttr("%s.worldSpace[0]" % crv_shape, "%s.inputCurve" % arc)

        length = cmds.getAttr("%s.arcLength" % arc)

        mlt = cmds.createNode("multiplyDivide")
        cmds.setAttr("%s.operation" % mlt, 2)
        cmds.connectAttr("%s.arcLength" % arc, "%s.input1X" % mlt)
        cmds.setAttr("%s.input2X" % mlt, length)

        for jnt in self.ik_joints[1:]:
            jnt_mlt = cmds.createNode("multiplyDivide")
            val = cmds.getAttr("%s.translateX" % jnt)

            cmds.connectAttr("%s.outputX" % mlt, "%s.input2X" % jnt_mlt)
            cmds.setAttr("%s.input1X" % jnt_mlt, val)

            cmds.connectAttr("%s.outputX" % jnt_mlt, "%s.translateX" % jnt)

    def test_create(self):
        cmds.file(new=True, force=True)

        joints = joint.create_chain(5, "Y", 4)
        self.set_joints(joints)

        self.create()
        self.add_stretch()
