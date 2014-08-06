
from link.config import Config
from maya import cmds
from link import util
from link.build.modules.components.skeleton import Skeleton
from link.build.modules.components.proxy import Proxy
from link.build.modules.parts.fk import FkChain
from link.build.modules.parts.ik import IkRp
from link.build.modules.parts.simple import Simple
from link.build.modules.parts.base import Base
from link.build.modules.parts.ikfk import IkFk

import logging
log = logging.getLogger(__name__)

class Link(object):
    def __init__(self):

        self.asset = "link"

        self.config = Config()
        self.parts = {}
        self.components = {}

    def _pre_build(self):
        cmds.file(new=True, force=True)
        self._create_nodes()

    def _build(self):
        """Create rig"""

        # Global control
        self.create_global()

        # Components
        self.create_skeleton()
        # self.create_proxy()

        # Parts
        self.create_root()
        self.create_hip()

        for pos in ["L", "R"]:
            self.create_collar(pos)
            self.create_arm(pos)
            self.create_leg(pos)

    def _post_build(self):
        self._parent_parts()
        self._parent_components()
        self._parent_settings()

    def build(self):
        log.info('build')
        self._pre_build()
        self._build()
        self._post_build()

    def _create_nodes(self):
        # Nodes
        self.top_node = cmds.createNode("transform", name=self.asset)
        self.part_node = cmds.createNode("transform", name="parts")
        self.comp_node = cmds.createNode("transform", name="components")
        self.settings_node = cmds.createNode("transform", name="settings")

        cmds.parent([self.part_node, self.comp_node, self.settings_node], self.top_node)

    def _parent_parts(self):
        log.info("Parenting %s part(s)" % len(self.parts.keys()))
        for key, part in self.parts.items():
            cmds.parent(part.top_node, self.part_node)

    def _parent_components(self):
        log.info("Parenting %s component(s)" % len(self.components.keys()))
        for key, comp in self.components.items():
            cmds.parent(comp.top_node, self.comp_node)

    def _parent_settings(self):
        for key, comp in self.components.items():
            cmds.parent(cmds.listRelatives(comp.settings_node, parent=True)[0], self.settings_node)

        for key, part in self.parts.items():
            cmds.parent(cmds.listRelatives(part.settings_node, parent=True)[0], self.settings_node)

            for ctl_key, ctl in part.controls.items():
                cmds.parent(part.settings_node, ctl.ctl, shape=True, add=True)

    def create_skeleton(self):
        component = Skeleton('C', 'skeleton')
        _file = "Users/eddiehoyle/Python/link/resources/skeleton.ma"
        component.set_file(_file)
        component.create()

        self.append_component(component)

    def create_proxy(self):
        component = Proxy('C', 'proxy')
        _file = "Users/eddiehoyle/Python/link/resources/proxy.ma"
        component.set_file(_file)
        component.create()

        self.append_component(component)

    def create_global(self):
        part = Base("C", "global")
        part.create()
        self.append_part(part)

        part.scale_shapes(12)

    def create_collar(self, position):
        part = FkChain(position, 'collar')
        joints = ["%s_collar_0_jnt" % position]
        part.set_joints(joints)
        part.create()
        part.omit_last_control()
        self.append_part(part)

        part.scale_shapes(4)
        part.rotate_shapes([0, 0, 90])

    def create_arm(self, position):
        part = IkFk(position, 'arm')
        joints = ["%s_arm_%s_jnt" % (position, index) for index in range(3)]
        part.set_joints(joints)
        part.create()
        self.append_part(part)

        part.scale_shapes(8)

    def create_leg(self, position):
        part = IkFk(position, 'leg')
        joints = ["%s_leg_%s_jnt" % (position, index) for index in range(3)]
        part.set_joints(joints)
        part.create()
        self.append_part(part)

        part.scale_shapes(10)

    def create_hip(self):
        part = Simple('C', 'hip')
        part.set_joints(["C_spine_0_jnt"])
        part.set_orient([0, 0, 0], world=True)
        part.create()        
        self.append_part(part)

        part.scale_shapes(6)

    def create_root(self):
        part = Simple('C', 'root')
        part.set_joints(["C_root_0_jnt"])
        part.set_orient([0, 0, 0], world=True)
        part.create()
        self.append_part(part)
        
        part.scale_shapes(10)

    def append_part(self, part):
        self.parts[part.name] = part

    def append_component(self, part):
        self.components[part.name] = part
