#!/usr/bin/env python

"""
"""

from link.util.control.control import Control
from maya import cmds
from link.util import name, joint, xform, vector, anno, common
from link.util.io.base import FileHandler
from link.modules.parts.part import Part
import logging
logger = logging.getLogger(__name__)

class Foot(Part):
    '''Simple foot setup with heel, ball and toe'''

    def __init__(self, position, description):
        super(Foot, self).__init__(position, description)

        self.data_file = None
        self.data_positions = []        

        # Specific joint position names
        self.joint_detail = {}
        self.pivot_detail = {}

    def set_data_file(self, path):
        self.data_file = path

    def set_joints(self, joints):

        if not len(joints) >= 3:
            raise ValueError("%s part needs 3 joints minimum." % self.__class__.__name__)

        self.joints = joints

        self.joint_detail['ankle'] = joints[0]
        self.joint_detail['ball'] = joints[1]
        self.joint_detail['tip'] = joints[2]

    def create_controls(self):

        # Create roll pivots
        self.create_functionality()

        # Create control
        ctl = Control(self.position, self.description, 0)
        ctl.create()

        # Style and lock attrs
        ctl.set_style("sphere")
        ctl.lock_scales()

    def create_functionality(self):
        self._create_reverse_setup()
        self._create_pivots_setup()

    def _create_reverse_setup(self):
        
        # Create Ik handles
        ball_ik, ball_effector = cmds.ikHandle(sj=self.joint_detail['ankle'], ee=self.joint_detail['ball'], sol="ikSCsolver")
        tip_ik, tip_effector = cmds.ikHandle(sj=self.joint_detail['ball'], ee=self.joint_detail['tip'], sol="ikSCsolver")

    def _create_pivots_setup(self):
        
        self.pivot_detail['heel'] = cmds.spaceLocator(name=name.create_name(self.position, self.description, 0, "heelNull"))[0]
        self.pivot_detail['ball'] = cmds.spaceLocator(name=name.create_name(self.position, self.description, 0, "ballNull"))[0]
        self.pivot_detail['tip'] = cmds.spaceLocator(name=name.create_name(self.position, self.description, 0, "tipNull"))[0]
        self.pivot_detail['bank_in'] = cmds.spaceLocator(name=name.create_name(self.position, self.description, 0, "bankInNull"))[0]
        self.pivot_detail['bank_out'] = cmds.spaceLocator(name=name.create_name(self.position, self.description, 0, "bankOutNull"))[0]

        for key, loc in self.pivot_detail.items():
            cmds.setAttr("%s.overrideEnabled" % loc, True)
            cmds.setAttr("%s.overrideColor" % loc, 1)
            cmds.connectAttr("%s.helpers" % self.settings_node, "%s.displayHandle" % loc)

        # Load in positions if exist
        if self.data_file:
            f = FileHandler("foot")
            data = f.read()
            for key, vector in data.items():
                cmds.setAttr("%s.translate" % key, *vector, type="float3")

    def test_create(self):
        cmds.file(new=True, force=True)

        # Create basic foot joints
        joints = joint.create_chain(3, "Z", 4)
        cmds.setAttr("%s.translate" % joints[0], 0, 4, 0, type="float3")
        cmds.setAttr("%s.translate" % joints[1], 2, -4, 0, type="float3")
        cmds.joint(joints[0], e=True, oj="xyz", sao="yup", ch=True, zso=True)

        self.set_joints(joints)
        # self.set_data_file("/Users/eddiehoyle/Python/link/foot.json")
        self.create()
        




