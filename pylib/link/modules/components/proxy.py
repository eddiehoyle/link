#!/usr/bin/env python

"""
"""

from link.util import xform, name
from maya import cmds
from link.modules.components.component import Component

class Proxy(Component):
    '''Imports and stuff'''

    def __init__(self, position, description):
        super(Proxy, self).__init__(position, description)

    def _collect_imported_nodes(self):
        """Only collect geometry"""

        # meshes = cmds.ls("temp:*", type="mesh")
        # nodes = []
        # for mesh in meshes:
        #     transform = cmds.listRelatives(mesh, p=True)[0]
        #     nodes.append(transform)

        return cmds.ls("temp:*")

    def _post_create(self):
        super(Proxy, self)._post_create()

        self._parent_geo_to_jnt()


    def _parent_geo_to_jnt(self):
        """Parent all geometry under corresponding joints"""

        for geo in self.nodes:
            jnt = geo.replace("_geo", "_jnt")

            if cmds.objExists(jnt):
                if cmds.nodeType(geo) == "transform" and cmds.nodeType(jnt) == "joint":

                    xform.match_pivot(jnt, geo)

                    jnt_shape = cmds.listRelatives(jnt, shapes=True)
                    if jnt_shape:
                        decom_node = cmds.createNode("decomposeMatrix", name=name.set_suffix(geo, "decompose"))
                        cmds.connectAttr("%s.worldMatrix" % jnt, "%s.inputMatrix" % decom_node)

                        cmds.setAttr("%s.scale" % geo, 1, 1, 1, type="float3")
                        cmds.parent(geo, jnt)
                        cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=0)
                        cmds.parent(geo, world=True)

                        for attr in ['translate', 'rotate', 'scale']:
                            cmds.connectAttr("%s.output%s" % (decom_node, attr.capitalize()), "%s.%s" % (geo, attr))

    def connect_settings(self):
        """Connect component nodes to settings node"""
        
        # Add settings
        cmds.addAttr(self.settings_node, ln="displayType", at="double", min=0, max=2)
        cmds.setAttr("%s.displayType" % self.settings_node, cb=True)
        cmds.setAttr("%s.displayType" % self.settings_node, k=False)

        for geo in self.nodes:
            meshes = cmds.listRelatives(geo, shapes=True) or []

            for mesh in meshes:
                cmds.setAttr("%s.overrideEnabled" % mesh, True)
                cmds.connectAttr("%s.displayType" % self.settings_node, "%s.overrideDisplayType" % mesh)
