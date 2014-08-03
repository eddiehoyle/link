
from link.util import name, xform
from link.util import common, joint
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

    def create_controls(self):
        """Create controls"""
        super(FkChain, self).create_controls()

        for key, ctl in self.controls.items():

            # Fk circles
            ctl.set_style("circle")

            # Lock transforms
            ctl.lock_translates()
            ctl.lock_scales()

        return self.controls

    def connect_controls(self):
        """Connect controls"""

        for key, joint in zip(self.controls.keys(), self.joints):

            self.controls[key].joint = joint
            ctl = self.controls[key]
            cmds.orientConstraint(ctl.ctl, joint, mo=True)

            # for axis in ["X", "Y", "Z"]:
            #     cmds.connectAttr("%s.rotate%s" % (self.controls[key].ctl, axis), "%s.rotate%s" % (joint, axis))
            #     # Add inbetween pma to any existing connections
            #     pma = cmds.createNode("plusMinusAverage")
            #     con = cmds.listConnections("%s.rotate%s" % (joint, axis), source=True, destination=False, plugs=True) or []
            #     if con:
            #         cmds.disconnectAttr(con[0], "%s.rotate%s" % (joint, axis))
            #         cmds.connectAttr(con[0], "%s.input3D[0].input3D%s" % (pma, axis.lower()))
            #         cmds.connectAttr("%s.output3D.output3D%s" % (pma, axis.lower()),  "%s.rotate%s" % (joint, axis))
            #     else:
            #         cmds.connectAttr("%s.rotate%s" % (ctl.ctl, axis), "%s.rotate%s" % (joint, axis))

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
                ctl_pma = cmds.createNode("plusMinusAverage", name=name.set_suffix(ctl.name, "ctlPma"))
                jnt_pma = cmds.createNode("plusMinusAverage", name=name.set_suffix(ctl.name, "jntPma"))
                out_mlt = cmds.createNode("multiplyDivide", name=name.set_suffix(ctl.name, "outMlt"))
                nrm_mlt = cmds.createNode("multiplyDivide", name=name.set_suffix(ctl.name, "nrmMlt"))

                # Determine if positive or negative
                child_translateX = cmds.xform(child_ctl.ctl, q=True, ws=True, t=True)[0]
                mult = 1
                if child_translateX < 0:
                    mult = -1

                # Normalise length value
                cmds.connectAttr("%s.length" % ctl.ctl, "%s.input1X" % nrm_mlt)

                # Apply ctl values
                cmds.connectAttr("%s.outputX" % nrm_mlt, "%s.input1D[0]" % ctl_pma)
                cmds.setAttr("%s.input2X" % nrm_mlt, distance)
                cmds.connectAttr("%s.output1D" % ctl_pma, "%s.input1X" % out_mlt)
                cmds.connectAttr("%s.outputX" % out_mlt, "%s.translateX" % child_ctl.grp)

                # Apply joint values
                cmds.connectAttr("%s.outputX" % nrm_mlt, "%s.input1D[0]" % jnt_pma)

                # Connect to joint
                cons = cmds.listConnections("%s.translateX" % child_ctl.joint, source=True, destination=False, plugs=True) or []
                if cons:
                    cmds.disconnectAttr(cons[0], "%s.translateX" % child_ctl.joint)
                    jnt_pma = cmds.createNode("plusMinusAverage")
                    cmds.connectAttr(cons[0], "%s.input1D[0]" % jnt_pma)
                    cmds.connectAttr("%s.output1D" % jnt_pma, "%s.translateX" % child_ctl.joint)
                else:
                    cmds.connectAttr("%s.output1D" % jnt_pma, "%s.translateX" % child_ctl.joint)


                self.stretch_nodes[child_ctl.name] = dict(out_mlt=out_mlt,
                                                          jnt_pma=jnt_pma,
                                                          ctl_pma=ctl_pma,
                                                          nrm_mlt=nrm_mlt)

    def test_create(self):
        cmds.file(new=True, force=True)
        jnts = joint.create_chain(3, 'X', 4)

        self.set_joints(jnts)
        self.create()
        self.rotate_shapes([0, 0, 90])
        self.add_stretch()


