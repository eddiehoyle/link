
from link.util import name, xform
from link.util import common, joint
from link.util.control.control import Control
from maya import cmds
from link.build.modules.parts.part import Part
from link.build.modules.parts.ik import IkSc, IkRp
from link.build.modules.parts.fk import FkChain
from link.build.modules.parts.simple import Simple
import logging
logger = logging.getLogger(__name__)


class IkFk(Part):
    def __init__(self, position, description):
        super(IkFk, self).__init__(position, description)

        self.ik = IkRp(position, description)
        self.fk = FkChain(position, description)

    def add_settings(self):
        super(IkFk, self).add_settings()

        cmds.addAttr(self.settings_node, ln="fkik", at="double", min=0, max=1, dv=1)
        cmds.setAttr("%s.fkik" % self.settings_node, cb=True)
        cmds.setAttr("%s.fkik" % self.settings_node, k=True)
        cmds.connectAttr("%s.fkik" % self.settings_node, "%s.ikBlend" % self.ik.ik)

        self.ik.add_settings()
        self.fk.add_settings()

    def test_create(self, joints=None):
        cmds.file(new=True, force=True)

        joints = joint.create_chain(3, "X", 3)
        self.set_joints(joints)
        self.create()

        # self.ik.add_stretch()
        # self.fk.add_stretch()


        # ------------------ #
        # Get this working!
        # ------------------ #

        # Connect stretches
        ik_mlt = self.ik.stretch_nodes['out_mlt']
        for fk_key, fk_ctl in self.fk.controls.items():
            fk_pma = self.fk.stretch_nodes.get(fk_key, {}).get('jnt_pma', None)
            if fk_pma:
                target_joint = cmds.listConnections("%s.output1D" % fk_pma, d=True, s=False, p=True) or []
                bc = cmds.createNode("blendColors")
                cmds.connectAttr("%s.outputX" % ik_mlt, "%s.color1R" % bc)
                cmds.connectAttr("%s.output1D" % fk_pma, "%s.color2R" % bc)

                if target_joint:
                    cmds.disconnectAttr("%s.output1D" % fk_pma, target_joint[0])
                    cmds.connectAttr("%s.outputR" % bc, target_joint[0])





    def set_joints(self, joints):
        self.joints = joints
        self.ik.set_joints(joints)
        self.fk.set_joints(joints)

    def create_controls(self):
        ik_controls = self.ik.create_controls()
        fk_controls = self.fk.create_controls()

        pv = self.ik.add_polevector()

        self.fk.rotate_shapes([0, 0, 90])
        self.fk.scale_shapes(1)

        self.controls.update(ik_controls)
        self.controls.update(fk_controls)

    def connect_controls(self):
        self.ik.connect_controls()
        self.fk.connect_controls()

    def match_controls(self):
        self.ik.match_controls()
        self.fk.match_controls()

    def add_stretch(self):
        self.ik.add_stretch()

        # cmds.addAttr(self.settings_node, ln="fkik", at="double", min=0, max=1)
        # cmds.setAttr("%s.fkik" % self.settings_node, cb=True)
        # cmds.setAttr("%s.fkik" % self.settings_node, k=True)
    def _pre_create(self):
        super(IkFk, self)._pre_create()

        self.ik.top_node = self.top_node
        self.fk.top_node = self.top_node
        self.ik.settings_node = self.settings_node
        self.fk.settings_node = self.settings_node

    # def _post_create(self):
    #     super(IkFk, self)._post_create()

    #     self.ik.parent_controls()
    #     self.fk.parent_controls()





