
from link.util import name, xform
from link.util import node, common
from link.util.control.control import Control
from maya import cmds
from link.build.modules.parts.part import Part

class Fk(Part):
    '''Basic FK control with no hierarchy'''

    def __init__(self, position, description):
        super(Fk, self).__init__(position, description)

        self.joints = []
        self.controls = {}

    def create_controls(self):
        """Create controls"""

        for index, joint in enumerate(self.joints):
            ctl = Control(self.position, self.description, index)
            ctl.create()
            ctl.set_style("circle")

            # Append control
            self.controls[ctl.name] = ctl

            # Store under top node
            cmds.parent(ctl.grp, self.top_node)

    def match_controls(self):
        """Match controls to joints"""
        for joint, key in zip(sorted(self.joints), sorted(self.controls.keys())):
            xform.match(self.controls[key].grp, joint)

    def connect_controls(self):
        """Connect controls"""
        index = 0
        for key, joint in zip(sorted(self.controls.keys()), sorted(self.joints)):

            pma = cmds.createNode("plusMinusAverage")
            for axis in ["X", "Y", "Z"]:

                cmds.connectAttr("%s.rotate%s" % (self.controls[key].ctl, axis), "%s.input3D[%s].input3D%s" % (pma, index, axis.lower()))
                cmds.connectAttr("%s.output3D.output3D%s" % (pma, axis.lower()), "%s.rotate%s" % (joint, axis))

            index += 1

    def add_stretch(self):
        """Stretch is driven by translateX in object space of transform"""

        # Create chain
        for key, ctl in self.controls.items():

            # Try get child control
            index = name.get_index(key)
            child_ctl = self.controls.get(name.set_index(key, index + 1), None)
            if child_ctl:

                adl = cmds.createNode("addDoubleLinear")
                distance = common.get_distance(ctl.ctl, child_ctl.ctl)

                # Determine if positive or negative
                child_translateX = cmds.xform(child_ctl.ctl, q=True, ws=True, t=True)[0]
                mult = 1
                if child_translateX < 0:
                    mult = -1

                # Apply values
                cmds.connectAttr("%s.translateX" % ctl.ctl, "%s.input1" % adl)
                cmds.setAttr("%s.input2" % adl, distance * mult)
                cmds.connectAttr("%s.output" % adl, "%s.translateX" % child_ctl.grp)




class FkChain(Fk):
    """Hierarchical FK chain"""

    def __init__(self, position, description):
        super(FkChain, self).__init__(position, description)

    def _post_create(self):
        super(FkChain, self)._post_create()

        # Create chain
        for key, ctl in self.controls.items():
            index = name.get_index(key)
            child_ctl = self.controls.get(name.set_index(key, index + 1), None)
            if child_ctl:
                cmds.parent(child_ctl.grp, ctl.ctl)
