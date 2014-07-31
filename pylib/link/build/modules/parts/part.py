from link.util import name
from maya import cmds
from link.build.modules.module import Module
from link import util
from collections import OrderedDict

class Part(Module):
    '''Joint dependent animation base class'''

    def __init__(self, position, description):
        super(Part, self).__init__(position, description)

        self.suffix = "prt"
        self.name = name.set_suffix(self.name, self.suffix)
        self.controls = OrderedDict()

        self.offset = {"point": {},
                       "orient": {}}

    def _create(self):
        self.create_controls()
        self.match_controls()
        self.connect_controls()

    def _post_create(self):
        super(Part, self)._post_create()

        # Parent settings node BEFORE adding shapes
        cmds.parent(cmds.listRelatives(self.settings_node, parent=True)[0], self.top_node)

        for key, ctl, in self.controls.items():
            cmds.parent(ctl.grp, self.top_node)
            cmds.parent(self.settings_node, ctl.ctl, add=True, shape=True)

    def set_joints(self, joints):
        self.joints = joints

    def create_controls(self):
        pass

    def match_controls(self):
        """Match controls to joints"""

        self.match_translates()
        self.match_rotates()

    def match_translates(self):
        """Match each controls groups translates to it's designated joint"""

        for joint, key in zip(self.joints, self.controls.keys()):
            util.xform.match_translates(self.controls[key].grp, joint)

        # Set custom point at creation time
        point_offset = self.offset.get("point", {})
        if point_offset:
            array = point_offset['array']
            world = point_offset['world']
            util.xform.set_translates(self.controls[key].grp, array, world)

    def match_rotates(self, target=None):
        """Match each controls groups rotates to it's designated joint"""

        for joint, key in zip(self.joints, self.controls.keys()):
            util.xform.match_rotates(self.controls[key].grp, joint)

        # Set custom orient at creation time
        orient_offset = self.offset.get("orient", {})
        if orient_offset:
            array = orient_offset['array']
            world = orient_offset['world']
            util.xform.set_rotates(self.controls[key].grp, array, world)

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

    def rotate_shapes(self, array, world=False):
        """Rotate all control shapes"""

        for key, ctl in self.controls.items():
            ctl.rotate_shapes(array, world=world)

    def set_orient(self, array, world):
        """Set an offset orient to be applied at creation time"""

        self.offset['orient'] = dict(array=array,
                                     world=world)

    def set_point(self, array):
        """Set an offset point to be applied at creation time"""

        self.offset['point'] = dict(array=array,
                                    world=world)

    def set_translates(self, array):
        for key, ctl in self.controls.items():
            util.xform.set_translates(ctl.grp, array, world=world)

    def set_rotates(self, array, world=False):
        for key, ctl in self.controls.items():
            util.xform.set_rotates(ctl.grp, array, world=world)

    def add_translates(self, array):
        pass

    def add_rotates(self, array):
        pass
