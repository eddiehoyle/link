from link.util import name
from maya import cmds
from link.build.modules.module import Module
from link.util import attr
from collections import OrderedDict

class Part(Module):
    '''Joint dependent animation base class'''

    def __init__(self, position, description):
        super(Part, self).__init__(position, description)

        self.suffix = "prt"
        self.name = name.set_suffix(self.name, self.suffix)
        self.controls = OrderedDict()

    def _create(self):
        self.create_controls()
        self.match_controls()
        self.connect_controls()

    def _post_create(self):
        super(Part, self)._post_create()

        # Parent settings BEFORE adding shapes
        cmds.parent(cmds.listRelatives(self.settings_node, parent=True)[0], self.top_node)

        for key, ctl, in self.controls.items():
            cmds.parent(ctl.grp, self.top_node)
            cmds.parent(self.settings_node, ctl.ctl, add=True, shape=True)

    def set_joints(self, joints):
        self.joints = joints

    def create_controls(self):
        pass

    def match_controls(self):
        pass

    def connect_controls(self):
        pass

    def get_control(self, index):
        try:
            return self.controls[self.controls.keys()[index]]
        except IndexError as e:
            raise IndexError("Control index not found: %s" % index)

    def scale_shapes(self, value):
        """Scale all control shapes"""

        for key, ctl in self.controls.items():
            ctl.scale_shapes(value)

    def rotate_shapes(self, array):
        """Rotate all control shapes"""

        for key, ctl in self.controls.items():
            ctl.rotate_shapes(array)

