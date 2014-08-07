#!/usr/bin/env python

from link.util import name, xform, joint
from link.util import common, vector, joint
from link.util.control.control import Control
from link import util
from maya import cmds
from link.build.modules.parts.part import Part
import logging
logger = logging.getLogger(__name__)

class IkSpline(Part):
    '''Ik single chain solver with no pole vector'''

    def __init__(self, position, description):
        super(IkSpline, self).__init__(position, description)

        self.description = "%sSpline" % description
        self.name = name.set_description(self.name, self.description)

        # Important nodes
        self.ik = None
        self.effector = None
        self.curve = None

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
        clusters = {}
        clusters['bot'] = cmds.cluster(["%s.cv[0]" % self.curve, "%s.cv[1]" % self.curve])[1]
        clusters['mid'] = cmds.cluster(["%s.cv[2]" % self.curve, "%s.cv[3]" % self.curve])[1]
        clusters['top'] = cmds.cluster(["%s.cv[4]" % self.curve, "%s.cv[5]" % self.curve])[1]
        
        util.xform.match_pivot(start_joint, clusters['bot'])
        util.xform.match_pivot(end_joint, clusters['top'])



    def create_controls(self):
        
        # Make duplicate joint chain
        self._duplicate_joints()

        # Create ikHandle
        self.create_ik()

    def match_controls(self):
        pass
    def connect_controls(self):
        pass
    def parent_controls(self):
        pass

    def test_create(self):
        cmds.file(new=True, force=True)

        joints = joint.create_chain(5, "Y", 3)
        self.set_joints(joints)

        self.create()
