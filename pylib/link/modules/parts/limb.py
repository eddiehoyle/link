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

        self.data_file = None
        self.settings_file = None
        self.data_positions = []        

        # Specific joint position names
        self.joint_detail = {}
        self.pivot_detail = {}
        self.ik_detail = {}

    def set_data_file(self, path):
        self.data_file = path

    def set_settings_file(self, path):
        self.settings_file = path        

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
        ctl.joint = self.joint_detail['ankle']

        # Style and lock attrs
        ctl.set_style("sphere")
        ctl.lock_all()

        self.controls[ctl.name] = ctl

    def match_controls(self):
        xform.match_translates(self.get_control(0).grp, self.joint_detail['ankle'])


    def create_functionality(self):
        self._create_reverse_setup()
        self._create_pivots_setup()

    def connect_controls(self):
        self._create_attrs()
        self._connect_functionality()

        cmds.parentConstraint(self.joint_detail['ankle'], self.get_control(0).grp, mo=True)

    def _create_reverse_setup(self):
        
        # Create Ik handles
        ball_ik, ball_effector = cmds.ikHandle(sj=self.joint_detail['ankle'], ee=self.joint_detail['ball'], sol="ikSCsolver")
        tip_ik, tip_effector = cmds.ikHandle(sj=self.joint_detail['ball'], ee=self.joint_detail['tip'], sol="ikSCsolver")

        self.ik_detail['ball'] = ball_ik
        self.ik_detail['tip'] = tip_ik

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
            log.debug("Data file found! Loading...")
            key = os.path.splitext(os.path.basename(self.data_file))[0]
            data = PartFileHandler(key).read()
            for key, vector in data.items():
                cmds.setAttr("%s.translate" % key, *vector, type="float3")
        else:
            log.warning("No data file found, please create before continuing.")
            return

        # Parent detail
        cmds.parent(self.ik_detail['ball'], self.pivot_detail['ball'])
        cmds.parent(self.ik_detail['tip'], self.pivot_detail['tip'])

        cmds.parent(self.pivot_detail['ball'], self.pivot_detail['tip'])
        cmds.parent(self.pivot_detail['tip'], self.pivot_detail['bank_in'])
        cmds.parent(self.pivot_detail['bank_in'], self.pivot_detail['bank_out'])
        cmds.parent(self.pivot_detail['bank_out'], self.pivot_detail['heel'])

        # Connections
        cmds.parentConstraint(self.pivot_detail['ball'], self.joint_detail['ankle'], sr=['x', 'y', 'z'], mo=True)

        # Collect setups
        for key, item in self.pivot_detail.items():
            self.setups.append(item)

        for key, item in self.ik_detail.items():
            self.setups.append(item)

    def _create_attrs(self):
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
                settings_full_attr = "%s.%s%s" % (self.settings_node, attr, titled_attr)
                cmds.addAttr(self.settings_node, ln="%s%s" % (attr, titled_attr), at="double")
                cmds.setAttr(settings_full_attr, cb=True)
                cmds.setAttr(settings_full_attr, k=True)

                cmds.connectAttr(settings_full_attr, "%s.%s" % (sr, settings_attr))

        if self.settings_file:
            log.debug("Data file found! Loading...")
            key = os.path.splitext(os.path.basename(self.data_file))[0]
            data = SettingsFileHandler(key).read()
            for full_attr, value in data.items():
                cmds.setAttr(full_attr, value)
        else:
            log.warning("No data file found, please create before continuing.")
            return



    def _connect_functionality(self):
        pass










    def test_create(self):
        cmds.file(new=True, force=True)

        # Create basic foot joints
        joints = joint.create_chain(3, "Z", 4)
        cmds.setAttr("%s.translate" % joints[0], 0, 4, 0, type="float3")
        cmds.setAttr("%s.translate" % joints[1], 2, -4, 0, type="float3")
        cmds.joint(joints[0], e=True, oj="xyz", sao="yup", ch=True, zso=True)

        self.set_joints(joints)
        self.set_data_file("/Users/eddiehoyle/Python/link/resources/data/parts/L_foot_0.json")
        self.set_settings_file("/Users/eddiehoyle/Python/link/resources/data/settings/L_foot_0.json")
        self.create()

        self.display_helpers(True)
        





