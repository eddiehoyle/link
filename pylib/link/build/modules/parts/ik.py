
from link.util import name, xform
from link.util import node, common
from link.util.control.control import Control
from maya import cmds
from link.build.modules.parts.part import Part
import logging
logger = logging.getLogger(__name__)

class Ik(Part):
    '''Basic FK control with no hierarchy'''

    def __init__(self, position, description):
        super(Ik, self).__init__(position, description)

        self.description = "%sIk" % description
        self.joints = []
        self.controls = {}

        self.ik = None
        self.effector = None

    def create_controls(self):
        """Create controls"""

        start_joint, end_joint = self.joints[0], self.joints[-1]
        logger.info("Creating Ik using nodes: %s" % self.joints)
        self.ik, self.effector = cmds.ikHandle(sj=start_joint, ee=end_joint, sol="ikRPsolver")

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

    def add_stretch(self):
        """Drive joints by translateX and distance between start and end"""

        # Create distance
        loc_start, loc_end, dst_node = common.create_distance(self.joints[0], self.joints[-1])
        distance = cmds.getAttr("%s.distance" % dst_node)

        # Create stretch multiplier
        md_mlt = cmds.createNode("multiplyDivide")
        cmds.connectAttr("%s.distance" % dst_node, "%s.input1X" % md_mlt)
        cmds.setAttr("%s.input2X" % md_mlt, distance)
        cmds.setAttr("%s.operation" % md_mlt, 2)

        # Detect positive or negative X value
        mult = 1
        start_x = cmds.getAttr("%s.translateX" % loc_start)
        end_x = cmds.getAttr("%s.translateX" % loc_end)
        if end_x - start_x < 0:
            mult = -1

        # Connect logic
        md_dst = cmds.createNode("multiplyDivide")
        cmds.connectAttr("%s.outputX" % md_mlt, "%s.input2X" % md_dst)
        cmds.setAttr("%s.input1X" % md_dst, distance * mult)

        # Assign parents
        # cmds.parent(loc_start, self.joints[0])
        cmds.parent(loc_end, self.controls[self.controls.keys()[0]].ctl)

        # Add to joint
        cmds.connectAttr("%s.outputX" % md_dst, "%s.translateX" % self.joints[-1])





