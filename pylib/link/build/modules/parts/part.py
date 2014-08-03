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
        self.joints = OrderedDict()

        self.offset = {"point": {},
                       "orient": {}}

        self.stretch_nodes = {'adl': [],
                              'mlt': [],
                              'div': []}

    def _create(self):
        self.setup_controls()
        self.setup_settings()

    def setup_controls(self):
        self.create_controls()
        self.match_controls()
        self.connect_controls()
        self.parent_controls()

    def setup_settings(self):
        self.add_settings()

    def add_settings(self):
        if not cmds.objExists("%s.helpers" % self.settings_node):
            cmds.addAttr(self.settings_node, ln="helpers", at='double', dv=0)
            cmds.setAttr("%s.helpers" % self.settings_node, cb=True)
            cmds.setAttr("%s.helpers" % self.settings_node, k=False)

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
            vector = point_offset['vector']
            world = point_offset['world']
            util.xform.set_translates(self.controls[key].grp, vector, world)

    def match_rotates(self, target=None):
        """Match each controls groups rotates to it's designated joint"""

        for joint, key in zip(self.joints, self.controls.keys()):
            util.xform.match_rotates(self.controls[key].grp, joint)

        # Set custom orient at creation time
        orient_offset = self.offset.get("orient", {})
        if orient_offset:
            vector = orient_offset['vector']
            world = orient_offset['world']
            util.xform.set_rotates(self.controls[key].grp, vector, world)


    def connect_controls(self):
        pass

    def parent_controls(self):
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

    def set_orient(self, vector, world=True):
        """Set an offset orient to be applied at creation time"""

        self.offset['orient'] = dict(vector=vector,
                                     world=world)

    def set_point(self, vector):
        """Set an offset point to be applied at creation time"""

        self.offset['point'] = dict(vector=vector,
                                    world=world)

    def set_translates(self, array):
        for key, ctl in self.controls.items():
            util.xform.set_translates(ctl.grp, array, world=world)

    def set_rotates(self, array, world=False):
        for key, ctl in self.controls.items():
            util.xform.set_rotates(ctl.grp, array, world=world)

    def test_create(self):
        """Single test creation methods for part"""
        pass

