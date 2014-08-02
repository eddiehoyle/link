
from link.util import name, xform
from link.util import common, vector, joint
from link.util.control.control import Control
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

        self.ik = None
        self.effector = None

    def create_ik(self):
        """Ik handle"""

        start_joint, end_joint = self.joints[0], self.joints[-1]
        logger.info("Creating Ik using nodes: %s" % self.joints)
        self.ik, self.effector = cmds.ikHandle(sj=start_joint, ee=end_joint, sol="ikSCsolver")

    def create_controls(self):
        """Create controls"""

        # Create ikHandle
        self.create_ik()

        # Create control
        ctl = Control(self.position, self.description)
        ctl.create()
        ctl.set_style("cube")

        # Append control
        self.controls[ctl.name] = ctl

        return self.controls

    def match_controls(self):

        # Match IK Handle to end joint
        for key in self.controls.keys():
            xform.match(self.controls[key].grp, self.joints[-1])

    def connect_controls(self):

        # Parent IK handle under ctl
        cmds.parent(self.ik, self.controls[self.controls.keys()[0]].ctl)

    def parent_controls(self):
        for key, ctl in self.controls.items():
            cmds.parent(ctl.grp, self.top_node)

    def add_stretch(self):
        """Drive joints by translateX and distance between start and end"""

        # Create distance
        loc_start, loc_end, dst_node = common.create_distance(self.joints[0], self.joints[-1])
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
        mult = 1
        start_x = cmds.getAttr("%s.translateX" % loc_start)
        end_x = cmds.getAttr("%s.translateX" % loc_end)
        if end_x - start_x < 0:
            mult = -1

        # Connect logic
        out_mlt = cmds.createNode("multiplyDivide", name=name.set_suffix(self.name, "outMlt"))
        cmds.connectAttr("%s.outputX" % div_mlt, "%s.input2X" % out_mlt)
        cmds.setAttr("%s.input1X" % out_mlt, (distance / len(self.joints[1:])) * mult)

        # Assign parents
        # cmds.parent(loc_start, self.joints[0])
        cmds.parent(loc_end, self.controls[self.controls.keys()[0]].ctl)

        # Add to joint
        for joint in self.joints[1:]:
            cmds.connectAttr("%s.outputX" % out_mlt, "%s.translateX" % joint)

        # Store important nodes
        self.stretch_nodes.update({'out_mlt': out_mlt,
                                   'div_mlt': div_mlt})

    def test_create(self):
        cmds.file(new=True, force=True)

        joints = joint.create_chain(4, 'X', 4)

        for j in joints:
            cmds.setAttr("%s.rotateY" % j, -10)
            cmds.joint(j, e=True, spa=True, ch=True)
            cmds.setAttr("%s.rotateY" % j, 0)

        self.set_joints(joints)
        self.create()


class IkRp(IkSc):
    '''Ik rotate plane control with polevector'''

    def __init__(self, position, description):
        super(IkRp, self).__init__(position, description)

    def create_ik(self):
        """Ik handle"""

        start_joint, end_joint = self.joints[0], self.joints[-1]
        logger.info("Creating Ik using nodes: %s" % self.joints)
        self.ik, self.effector = cmds.ikHandle(sj=start_joint, ee=end_joint, sol="ikRPsolver")

    def add_polevector(self, description, offset=[0, 0, 0]):
        """Add pole vector for ikHandle"""

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
        start_pos = cmds.xform(self.joints[0], q=1, t=1, ws=1)
        end_pos = cmds.xform(self.joints[-1], q=1, t=1, ws=1)
        middle_pos = vector.average_3f(start_pos, end_pos)
        middle_pos = vector.add_3f(middle_pos, offset)

         # Find center of ik handle
        start_rot = cmds.xform(self.joints[0], q=1, ro=1, ws=1)
        end_rot = cmds.xform(self.joints[-1], q=1, ro=1, ws=1)
        middle_rot = vector.average_3f(start_rot, end_rot)

        # Move into position
        cmds.xform(ctl.grp, t=middle_pos, ws=True)
        cmds.xform(ctl.grp, ro=middle_rot, ws=True)

        # Create poleVector
        cmds.poleVectorConstraint(ctl.ctl, self.ik, weight=True)

        self.controls[ctl.name] = ctl

    def test_create(self):
        super(IkRp, self).test_create()

        self.add_polevector("elbow", [0, 0, -4])
        self.controls["L_elbow_0_ctl"].rotate_shapes([90, 0, 0])
        self.controls["L_elbow_0_ctl"].scale_shapes(0.5)
