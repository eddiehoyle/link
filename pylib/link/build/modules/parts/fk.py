
from link.util import name, xform
from link.util.control.control import Control
from maya import cmds
from link.build.modules.parts.part import Part

class Fk(Part):
    '''Imports and stuff'''

    def __init__(self, position, description):
        super(Fk, self).__init__(position, description)

        self.joints = []
        self.controls = {}

    def set_joints(self, joints):
        self.joints = joints

    def _create(self):
        self.create_controls()
        self.match_controls()
        self.connect_controls()

    def create_controls(self):
        """Create controls"""

        for index, joint in enumerate(self.joints):
            ctl = Control(self.position, self.description, index)
            ctl.create()

            # Append control
            self.controls[ctl.name] = ctl

            # Store under top node
            cmds.parent(ctl.grp, self.top_node)

    def match_controls(self):
        """Match controls to joints"""
        for joint, key in zip(sorted(self.joints), sorted(self.controls.keys())):
            xform.match(joint, self.controls[key].grp)


class FkChain(Fk):
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
