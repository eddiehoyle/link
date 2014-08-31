#!/usr/bin/env python

"""
"""
import os
import re
from link.util.control.control import Control
from maya import cmds
from link.util import name, joint, xform, vector, anno, common
from link.util.io.part import PartFileHandler
from link.util.io.settings import SettingsFileHandler
from link.modules.parts.part import Part
import logging
log = logging.getLogger(__name__)

class Foot(Part):
    '''Simple foot setup with heel, ball and toe'''

    def __init__(self, position, description):
        super(Foot, self).__init__(position, description)

        self.part_file = None
        self.settings_file = None
        self.data_positions = [] 
        self.foot_joints = []       

        # Specific joint position names
        self.joint_detail = {}
        self.pivot_detail = {}
        self.ik_detail = {}
        self.pma_detail = {}
        

    def set_part_file(self, path):
        self.part_file = path

    def set_settings_file(self, path):
        self.settings_file = path     

    def _duplicate_joints(self):
        """Create a duplicate FK joint chain to drive rig"""

        self.foot_joints = joint.duplicate_joints(self.joints, "foot")
        self.setups.extend(self.foot_joints) 

        self.joint_detail['ankle'] = self.foot_joints[0]
        self.joint_detail['ball'] = self.foot_joints[1]
        self.joint_detail['tip'] = self.foot_joints[2]

    def set_joints(self, joints):

        if not len(joints) >= 3:
            raise ValueError("%s part needs 3 joints minimum." % self.__class__.__name__)

        self.joints = joints

        self.joint_detail['ankle'] = self.joints[0]
        self.joint_detail['ball'] = self.joints[1]
        self.joint_detail['tip'] = self.joints[2]

    def create_controls(self):

        # Create roll pivots
        self.create_functionality()

        # Create control
        ctl = Control(self.position, self.description, 0)
        ctl.create()
        ctl.joint = self.joint_detail['ankle']

        # Style and lock attrs
        ctl.set_style("sphere")
        ctl.lock_all()

        self.controls[ctl.name] = ctl

        toe_ctl = Control(self.position, "toe", 0)
        toe_ctl.create()

        toe_ctl.lock_translates()
        toe_ctl.lock_scales()
        toe_ctl.rotate_shapes([0, 0, 90])

        toe_ctl.set_style('circle')

        self.controls[toe_ctl.name] = toe_ctl

    def match_controls(self):
        xform.match_translates(self.get_control(0).grp, self.joint_detail['ankle'])
        xform.match_translates(self.get_control(1).grp, self.joint_detail['ball'])

    def parent_controls(self):
        switch_ctl = self.get_control(0)
        toe_ctl = self.get_control(1)
        cmds.parent(toe_ctl.grp, switch_ctl.ctl)

    def create_functionality(self):
        self._create_reverse_setup()
        self._create_pivots_setup()

    def connect_controls(self):
        self._create_functionality()
        self._connect_functionality()

        cmds.parentConstraint(self.joint_detail['ankle'], self.get_control(0).grp, mo=True)
        cmds.connectAttr("%s.rotate" % self.get_control(1).ctl, "%s.rotate" % self.pivot_detail['toe'])

    def _create_reverse_setup(self):
        
        # Create Ik handles
        ball_ik, ball_effector = cmds.ikHandle(sj=self.joint_detail['ankle'], ee=self.joint_detail['ball'], sol="ikSCsolver")
        tip_ik, tip_effector = cmds.ikHandle(sj=self.joint_detail['ball'], ee=self.joint_detail['tip'], sol="ikSCsolver")

        self.ik_detail['ball'] = ball_ik
        self.ik_detail['tip'] = tip_ik

    def _create_pivots_setup(self):
            
        # Transforms
        top_grp = cmds.createNode("transform", name=name.create_name(self.position, "%sPivots" % self.description, 0, "grp"))
        tip_grp = cmds.createNode("transform", name=name.create_name(self.position, "%sTipPivots" % self.description, 0, "grp"))
        toe_grp = cmds.createNode("transform", name=name.create_name(self.position, "%sToePivots" % self.description, 0, "grp"))
        ball_grp = cmds.createNode("transform", name=name.create_name(self.position, "%sBallPivots" % self.description, 0, "grp"))

        xform.match_translates(tip_grp, self.joint_detail['tip'])
        xform.match_translates(ball_grp, self.joint_detail['ball'])
        xform.match_translates(toe_grp, self.joint_detail['ball'])

        self.pivot_detail['heel'] = cmds.spaceLocator(name=name.create_name(self.position, self.description, 0, "heelNull"))[0]
        ball_loc = cmds.spaceLocator(name=name.create_name(self.position, self.description, 0, "ballNull"))[0]
        tip_loc = cmds.spaceLocator(name=name.create_name(self.position, self.description, 0, "tipNull"))[0]
        self.pivot_detail['toe'] = toe_grp
        self.pivot_detail['tip'] = tip_grp
        self.pivot_detail['ball'] = ball_grp
        self.pivot_detail['bank_in'] = cmds.spaceLocator(name=name.create_name(self.position, self.description, 0, "bankInNull"))[0]
        self.pivot_detail['bank_out'] = cmds.spaceLocator(name=name.create_name(self.position, self.description, 0, "bankOutNull"))[0]

        for key, loc in self.pivot_detail.items():
            cmds.setAttr("%s.overrideEnabled" % loc, True)
            cmds.setAttr("%s.overrideColor" % loc, 1)
            cmds.connectAttr("%s.helpers" % self.settings_node, "%s.displayHandle" % loc)
            cmds.connectAttr("%s.helpers" % self.settings_node, "%s.visibility" % loc)

        # Load in positions if exist
        if self.part_file:
            log.debug("Data file found! Loading...")
            key = os.path.splitext(os.path.basename(self.part_file))[0]
            data = PartFileHandler(key).read()
            for key, vector in data.items():
                cmds.setAttr("%s.translate" % key, *vector, type="float3")
        else:
            log.warning("No data file found, please create before continuing.")
            return

        # Parent detail
        cmds.parent(self.ik_detail['ball'], ball_loc)
        cmds.parent(self.ik_detail['tip'], tip_loc)

        cmds.parent(ball_loc, ball_grp)
        cmds.parent(tip_loc, toe_grp)
        cmds.parent([toe_grp, ball_grp], tip_grp)
        cmds.parent(tip_grp, self.pivot_detail['bank_in'])

        cmds.parent(self.pivot_detail['bank_in'], self.pivot_detail['bank_out'])
        cmds.parent(self.pivot_detail['bank_out'], self.pivot_detail['heel'])
        cmds.parent(self.pivot_detail['heel'], top_grp)

        # Collect setups
        for key, item in self.pivot_detail.items():
            self.setups.append(item)

        for key, item in self.ik_detail.items():
            self.setups.append(item)

        self.setups.append(top_grp)

    def _create_functionality(self):
        ctl = self.get_control(0)
        attrs = ['heel', 'ball', 'tip', 'bankIn', 'bankOut']
        for attr in attrs:
            cmds.addAttr(ctl.ctl, ln=attr, at="double", min=-10, max=10)
            cmds.setAttr("%s.%s" % (ctl.ctl, attr), cb=True)
            cmds.setAttr("%s.%s" % (ctl.ctl, attr), k=True)

        # Standard connections
        self.range_detail = {}
        for attr in attrs:
            sr = cmds.createNode("setRange", name=name.create_name(self.position, self.description, 0, "%sRange" % attr))
            self.range_detail[attr] = sr

            # Create settings node connections
            for settings_attr in ['minX', 'maxX', 'oldMinX', 'oldMaxX']:
                titled_attr = re.sub('([a-zA-Z])', lambda k: k.groups()[0].upper(), settings_attr, 1)
                settings_full_attr = "%s.%s%s" % (self.setup_node, attr, titled_attr)
                cmds.addAttr(self.setup_node, ln="%s%s" % (attr, titled_attr), at="double")
                cmds.setAttr(settings_full_attr, cb=True)
                cmds.setAttr(settings_full_attr, k=True)

                cmds.connectAttr(settings_full_attr, "%s.%s" % (sr, settings_attr))

        # Load settings for part
        if self.settings_file:
            log.debug("Settings file found! Loading...")
            key = os.path.splitext(os.path.basename(self.part_file))[0]
            data = SettingsFileHandler(key).read()
            for full_attr, value in data.items():
                if cmds.objExists(full_attr):
                    cmds.setAttr(full_attr, value)
        else:
            log.warning("No settnings file found, please create before continuing.")

    def _connect_functionality(self):
        """
        Connect attributes to foot functionality
        """

        ctl = self.get_control(0)
        attrs = ['heel', 'ball', 'tip', 'bankIn', 'bankOut']
        for attr in attrs:
            pma = cmds.createNode("plusMinusAverage", name=name.set_suffix(self.name, "%sPma" % attr))
            cmds.connectAttr("%s.%s" % (ctl.ctl, attr), "%s.input1D[0]" % pma)
            cmds.connectAttr("%s.output1D" % pma, "%s.valueX" % self.range_detail[attr])

            self.pma_detail[attr] = pma

        cmds.connectAttr("%s.outValueX" % self.range_detail['heel'], "%s.rotateX" % self.pivot_detail['heel'])
        cmds.connectAttr("%s.outValueX" % self.range_detail['ball'], "%s.rotateX" % self.pivot_detail['ball'])
        cmds.connectAttr("%s.outValueX" % self.range_detail['tip'], "%s.rotateX" % self.pivot_detail['tip'])
        cmds.connectAttr("%s.outValueX" % self.range_detail['bankIn'], "%s.rotateZ" % self.pivot_detail['bank_in'])
        cmds.connectAttr("%s.outValueX" % self.range_detail['bankOut'], "%s.rotateZ" % self.pivot_detail['bank_out'])

        # Add reverse inbetweens
        common.add_reverse_md("%s.outValueX" % self.range_detail['heel'], "%s.rotateX" % self.pivot_detail['heel'])
        common.add_reverse_md("%s.outValueX" % self.range_detail['bankOut'], "%s.rotateZ" % self.pivot_detail['bank_out'])











    def test_create(self):
        cmds.file(new=True, force=True)

        # Create basic foot joints
        joints = joint.create_chain(3, "Z", 4)
        cmds.setAttr("%s.translate" % joints[0], 0, 4, 0, type="float3")
        cmds.setAttr("%s.translate" % joints[1], 2, -4, 0, type="float3")
        cmds.joint(joints[0], e=True, oj="xyz", sao="yup", ch=True, zso=True)

        self.set_joints(joints)
        self.set_part_file("/Users/eddiehoyle/Python/link/resources/data/parts/foot_test.json")
        self.set_settings_file("/Users/eddiehoyle/Python/link/resources/data/settings/foot_test.json")
        self.create()

        self.display_helpers(True)
        





