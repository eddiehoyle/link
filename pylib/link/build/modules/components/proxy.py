from maya import cmds
from link.build.modules.components.component import Component

class Proxy(Component):
    '''Imports and stuff'''

    def __init__(self, position, description):
        super(Proxy, self).__init__(position, description)

    def _collect_imported_nodes(self):
        """Only collect geometry"""

        meshes = cmds.ls("temp:*", type="mesh")
        nodes = []
        for mesh in meshes:
            transform = cmds.listRelatives(mesh, p=True)[0]
            nodes.append(transform)
        return nodes

    def _post_create(self):
        super(Proxy, self)._post_create()

        self._parent_geo_to_jnt()

    def _parent_geo_to_jnt(self):
        """Parent all geometry under corresponding joints"""

        for geo in self.nodes:
            jnt = geo.replace("_geo", "_jnt")

            if cmds.objExists(jnt):
                if cmds.nodeType(geo) == "transform" and cmds.nodeType(jnt) == "joint":
                    cmds.parent(geo, jnt)

