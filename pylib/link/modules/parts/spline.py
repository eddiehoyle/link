#!/usr/bin/env python

"""
"""

from link.util import name, joint, curve, xform
from link.util.control.control import Control
from maya import cmds
from link.modules.parts.part import Part
from link.modules.parts.fk import FkChain
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

        # Add meeee
        self.detail = 3

    def _duplicate_joints(self):

        # Create new joints
        self.ik_joints = joint.duplicate_joints(self.joints, "ik")

        # Connect ik jnts to source joints
        for ik_jnt, src_jnt in zip(self.ik_joints, self.joints):
            cmds.parentConstraint(ik_jnt, src_jnt, mo=True)

        # Add to setups
        self.setups.extend(self.ik_joints)

    def create_ik(self):
        """Ik spline"""

        # Create curve
        tmp_curve = curve.create_from_nodes(self.joints, name=name.set_suffix(self.name, 'ikCrv'), degree=3)
        self.curve = curve.rebuild_curve(tmp_curve, 3)[0]

        start_joint, end_joint = self.ik_joints[0], self.ik_joints[-1]
        logger.info("Creating Ik using nodes: %s" % self.joints)
        self.ik, self.effector = cmds.ikHandle(name=name.set_suffix(self.name, 'ikh'), sj=start_joint, ee=end_joint, curve=self.curve, createCurve=False, sol="ikSplineSolver", ns=3)

        # Add to setups
        self.setups.extend([self.ik, self.curve])

        # Set attrs
        cmds.setAttr("%s.dTwistControlEnable" % self.ik, 1)
        cmds.setAttr("%s.dWorldUpAxis" % self.ik, 1)
        cmds.setAttr("%s.dWorldUpType" % self.ik, 4)
        cmds.setAttr("%s.dWorldUpVector" % self.ik, 1.0, 0.0, 0.0, type="float3")
        cmds.setAttr("%s.dWorldUpVectorEnd" % self.ik, 1.0, 0.0, 0.0, type="float3")

        # Turn on cvs
        cmds.select(self.curve, r=True)
        cmds.toggle(cv=True)

        # Create clusters
        clusters = OrderedDict()
        clusters['bot'] = cmds.cluster(["%s.cv[0]" % self.curve, "%s.cv[1]" % self.curve])[1]
        clusters['mid'] = cmds.cluster(["%s.cv[2]" % self.curve, "%s.cv[3]" % self.curve])[1]
        clusters['top'] = cmds.cluster(["%s.cv[4]" % self.curve, "%s.cv[5]" % self.curve])[1]
        
        xform.match_pivot(start_joint, clusters['bot'])
        xform.match_pivot(end_joint, clusters['top'])

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

        # Lock mid controls rotates
        self.ik_controls['mid'].lock_scales()

        return self.controls

    def match_controls(self):

        bot_ctl = self.ik_controls['bot']
        mid_ctl = self.ik_controls['mid']
        top_ctl = self.ik_controls['top']

        xform.match_translates(bot_ctl.grp, self.joints[0])
        xform.match_translates(top_ctl.grp, self.joints[-1])

        # Get mid position
        xform.match_average_position(mid_ctl.grp, [top_ctl.grp, bot_ctl.grp])

    def connect_controls(self):

        bot_ctl = self.ik_controls['bot']
        mid_ctl = self.ik_controls['mid']
        top_ctl = self.ik_controls['top']

        for key, ctl in self.controls.items():
            cmds.parent(ctl.cluster, ctl.ctl)

        cmds.orientConstraint(self.ik_controls['top'].ctl, self.ik_joints[-1], mo=True)

        # Connect to IkHandle
        cmds.connectAttr("%s.worldMatrix" % bot_ctl.ctl, "%s.dWorldUpMatrix" % self.ik)
        cmds.connectAttr("%s.worldMatrix" % top_ctl.ctl, "%s.dWorldUpMatrixEnd" % self.ik)


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

    def connect_settings(self):

        for jnt in self.ik_joints:
            cmds.connectAttr("%s.helpers" % self.settings_node, "%s.visibility" % jnt)
            cmds.connectAttr("%s.helpers" % self.settings_node, "%s.displayLocalAxis" % jnt)

        for node in [self.ik, self.curve]:
            cmds.connectAttr("%s.helpers" % self.settings_node, "%s.visibility" % node)

        for key, cls in self.clusters.items():
            cmds.connectAttr("%s.helpers" % self.settings_node, "%s.visibility" % cls)

    def test_create(self):
        cmds.file(new=True, force=True)

        joints = joint.create_chain(5, "Y", 2)
        self.set_joints(joints)

        self.create()
        self.add_stretch()


class IkFkSpline(Part):
    def __init__(self, position, description):
        super(IkFkSpline, self).__init__(position, description)

        self.ik = IkSpline(position, description)
        self.fk = FkChain(position, description)

        # Ik joint logic override
        self.ik._duplicate_joints = self._ik_duplicate_joints
        self.fk._duplicate_joints = self._fk_duplicate_joints

        self._offset_fk_joints = []

    def offset_fk_joints(self, joints):
        log.warning("Offset fk joints not supported yet.")
        self.fk.set_joints(joints)

    def _ik_duplicate_joints(self):
        self.ik.ik_joints = joint.duplicate_joints(self.ik.joints, "ik")
        self.setups.extend(self.ik.ik_joints)

    def _fk_duplicate_joints(self):
        self.fk.fk_joints = joint.duplicate_joints(self.fk.joints, "fk")
        self.setups.extend(self.fk.fk_joints)

    def _pre_create(self):
        super(IkFkSpline, self)._pre_create()

        self.ik.top_node = self.top_node
        self.fk.top_node = self.top_node
        self.ik.settings_node = self.settings_node
        self.fk.settings_node = self.settings_node

    def create_controls(self):
        ik_controls = self.ik.create_controls()
        fk_controls = self.fk.create_controls()

        self.fk.rotate_shapes([0, 0, 90])

        self.controls.update(ik_controls)
        self.controls.update(fk_controls)

    def set_joints(self, joints):
        self.joints = joints
        self.ik.set_joints(joints)
        self.fk.set_joints(joints)

    def connect_controls(self):
        self.ik.connect_controls()
        self.fk.connect_controls()

    def match_controls(self):
        self.ik.match_controls()
        self.fk.match_controls()

    def add_stretch(self):
        logger.warning("Stretch unavailable for: %s" % self.__class__.__name__)
        # self.ik.add_stretch()
        # self.fk.add_stretch()

    def parent_controls(self):
        self.ik.parent_controls()
        self.fk.parent_controls()

    def connect_settings(self):
        self.ik.connect_settings()
        self.fk.connect_settings()
        self.connect_ikfk()

    def connect_ikfk(self):

        for ik_jnt, fk_ctl_key in zip(self.ik.ik_joints, self.fk.controls.keys()):
            
            ctl = self.fk.controls[fk_ctl_key]
            cmds.orientConstraint(ik_jnt, ctl.grp, mo=True)

        ik_joints = self.ik.ik_joints
        fk_ctls = [self.fk.controls[k] for k in self.fk.controls.keys()]

        print len(self.ik.ik_joints) - len(self.fk.fk_joints), len(ik_joints)
        for index in range(len(self.ik.ik_joints) - len(self.fk.fk_joints), len(ik_joints)):
            fk_ctl = self.fk.get_control(index)

            for child_index in range(index + 1, len(ik_joints)):
                fk_child_ctl = self.fk.get_control(child_index)

                if fk_child_ctl:
                    cons = cmds.listConnections(fk_child_ctl.inb, type='plusMinusAverage', scn=True, s=True, d=False, p=False)
                    if not cons:
                        pma = cmds.createNode("plusMinusAverage", name=name.set_suffix(fk_child_ctl.name, "ctlOrient"))
                        cmds.connectAttr("%s.output3D" % pma, "%s.rotate" % fk_child_ctl.inb)
                    else:
                        pma = cons[0]
                    
                    v = cmds.getAttr("%s.input3D" % pma, size=True)
                    cmds.connectAttr("%s.rotate" % fk_ctl.ctl, "%s.input3D[%s]" % (pma, index))

    def _tidy_up(self):
        """Collect ik and fk nodes"""

        self.setups.extend(self.ik.setups)
        self.setups.extend(self.fk.setups)

        super(IkFkSpline, self)._tidy_up()

    def test_create(self):
        cmds.file(new=True, force=True)

        joints = joint.create_chain(5, "Y", 2)

        self.set_joints(joints)

        self.create()
        self.add_stretch()
