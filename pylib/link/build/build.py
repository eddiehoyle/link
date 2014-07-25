
from link.config import Config
from maya import cmds
from link.build.modules.components.skeleton import Skeleton
from link.build.modules.components.proxy import Proxy
from link.build.modules.parts.fk import FkChain, Fk

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
        self._create_skeleton()
        self._create_proxy()
        for pos in ["L", "R"]:
            self._create_arm(pos)

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

    def _create_skeleton(self):
        component = Skeleton('C', 'skeleton')
        _file = "Users/eddiehoyle/Python/link/resources/skeleton.ma"
        component.set_file(_file)
        component.create()

        self._append_component(component)

    def _create_proxy(self):
        component = Proxy('C', 'proxy')
        _file = "Users/eddiehoyle/Python/link/resources/proxy.ma"
        component.set_file(_file)
        component.create()

        self._append_component(component)

    def _create_arm(self, position):
        part = FkChain(position, 'arm')
        joints = ["%s_arm_%s_jnt" % (position, index) for index in range(3)]
        print joints
        part.set_joints(joints)
        part.create()


        self._append_part(part)

    def _append_part(self, part):
        self.parts[part.name] = part

    def _append_component(self, part):
        self.components[part.name] = part
