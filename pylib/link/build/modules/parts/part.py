from link.util import name
from maya import cmds
from link.build.modules.module import Module
from link.util import attr

class Part(Module):
    '''Joint dependent animation base class'''

    def __init__(self, position, description):
        super(Part, self).__init__(position, description)

        self.suffix = "prt"
        self.name = name.set_suffix(self.name, self.suffix)

    def _create_settings(self):
        loc = cmds.spaceLocator(name=name.set_suffix(self.name, "settings"))[0]
        shape = cmds.listRelatives(loc, shapes=True)[0]

        # Add attr
        attr.lock_all(loc)
        attr_path = "%s.parent" % shape
        cmds.addAttr(shape, ln="parent", at="long", min=0, max=4)
        cmds.setAttr(attr_path, cb=True)
        cmds.setAttr(attr_path, k=True)

        # Hide these
        for local in ["localPosition", "localScale"]:
            for axis in ["X", "Y", "Z"]:
                attr_path = "%s.%s%s" % (shape, local, axis)
                cmds.setAttr(attr_path, cb=False)

        self.settings_node = shape


    def _create(self):
        self._create_settings()
        self.create_controls()
        self.match_controls()
        self.connect_controls()
        self._add_settings()


    def _add_settings(self):
        # Temp method
        for key in self.controls.keys():
            cmds.parent(self.settings_node, self.controls[key].ctl, shape=True, add=True)


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
            return sorted(self.controls.keys())[index]
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

