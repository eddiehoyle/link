
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

        # Store under top node
        cmds.parent(ctl.grp, self.top_node)

    def match_controls(self):

        # Match IK Handle to end joint
        for key in self.controls.keys():
            xform.match(self.controls[key].grp, self.joints[-1])

    def connect_controls(self):

        ctl = self.controls[self.controls.keys()[0]]
        joint = self.joints[-1]

        # Get ikHandle position
        ik_world_pos = cmds.xform(self.ik, q=True, ws=True, t=True)

        index = 0
        pma = cmds.createNode("plusMinusAverage")
        for axis in ["X", "Y", "Z"]:

            cmds.connectAttr("%s.translate%s" % (ctl.ctl, axis), "%s.input3D[%s].input3D%s" % (pma, index, axis.lower()))
            cmds.connectAttr("%s.output3D.output3D%s" % (pma, axis.lower()), "%s.translate%s" % (self.ik, axis))

        # Match original ikHandle values
        for ik_axis_pos, axis in zip(ik_world_pos, ["X", "Y", "Z"]):
            cmds.setAttr("%s.input3D[%s].input3D%s" % (pma, (index + 1), axis.lower()), ik_axis_pos)

    def add_stretch(self):

        '''
        TRY:
            Drive translateX of ik joint by distance node?
        '''

        # ctl = self.controls[self.controls.keys()[0]]
        # pma = cmds.createNode("plusMinusAverage")
        # index = 0
        # for axis in ["X", "Y", "Z"]:

        #     cmds.connectAttr("%s.translate%s" % (self.joints[-1], axis), "%s.input3D[%s].input3D%s" % (pma, index, axis.lower()))
        #     cmds.connectAttr("%s.translate%s" % (ctl.ctl, axis), "%s.input3D[%s].input3D%s" % (pma, (index + 1), axis.lower()))
        #     cmds.connectAttr("%s.output3D.output3D%s" % (pma, axis.lower()), "%s.translate%s" % (self.effector, axis), force=True)


        # joint_local_pos = cmds.xform(self.joints[-1], q=True, os=True, t=True)
        # for joint_axis_pos, axis in zip(joint_local_pos, ["X", "Y", "Z"]):
        #     cmds.setAttr("%s.input3D[%s].input3D%s" % (pma, (index + 1), axis.lower()), joint_axis_pos)




