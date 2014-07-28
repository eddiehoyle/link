
from link.config import Config
from maya import cmds
from link.build.modules.components.skeleton import Skeleton
from link.build.modules.components.proxy import Proxy
from link.build.modules.parts.fk import FkChain, Fk
from link.build.modules.parts.ik import Ik
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

        # Components
        self.create_skeleton()
        # self.create_proxy()

        # Parts
        for pos in ["L", "R"]:
            self.create_collar(pos)
            # self.create_arm(pos)
            # self.create_leg(pos)

    def _post_build(self):
        self._parent_parts()
        self._parent_components()

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

        cmds.parent([self.part_node, self.comp_node], self.top_node)

    def _parent_parts(self):
        log.info("Parenting %s part(s)" % len(self.parts.keys()))
        for key, part in self.parts.items():
            cmds.parent(part.top_node, self.part_node)

    def _parent_components(self):
        log.info("Parenting %s component(s)" % len(self.components.keys()))
        for key, part in self.components.items():
            cmds.parent(part.top_node, self.comp_node)

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

    def create_collar(self, position):
        part = IkFk(position, 'collar')
        joints = ["%s_collar_0_jnt" % position, "%s_arm_0_jnt" % position]
        part.set_joints(joints)
        part.create()
        self.append_part(part)

        part.scale_shapes(1)
        part.add_stretch()

    def create_arm(self, position):
        part = FkChain(position, 'arm')
        joints = ["%s_arm_%s_jnt" % (position, index) for index in range(3)]
        part.set_joints(joints)
        part.create()
        self.append_part(part)

        part.scale_shapes(4)
        part.rotate_shapes([0, 0, 90])
        part.add_stretch()

    def create_leg(self, position):
        part = FkChain(position, 'leg')
        joints = ["%s_leg_%s_jnt" % (position, index) for index in range(3)]
        part.set_joints(joints)
        part.create()
        self.append_part(part)

        part.scale_shapes(4)
        part.rotate_shapes([90, 0, 0])
        part.add_stretch()

    def append_part(self, part):
        self.parts[part.name] = part

    def append_component(self, part):
        self.components[part.name] = part
