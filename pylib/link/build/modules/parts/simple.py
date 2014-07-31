
from link.util import name, xform
from link.util import common
from link.util.control.control import Control
from maya import cmds
from link.build.modules.parts.part import Part

class Simple(Part):
    '''Basic Simple control with no hierarchy'''

    def __init__(self, position, description):
        super(Simple, self).__init__(position, description)

    def create_controls(self):
        """Create controls"""

        for index, joint in enumerate(self.joints):
            ctl = Control(self.position, self.description, index)
            ctl.create()
            ctl.set_style("square")

            # Lock attrs
            ctl.lock_vis()

            # Append control
            self.controls[ctl.name] = ctl

        return self.controls

    def connect_controls(self):
        for key, joint in zip(self.controls.keys(), self.joints):
            cmds.parentConstraint(self.controls[key].ctl, joint, mo=True)

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
