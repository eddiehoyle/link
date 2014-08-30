#!/usr/bin/env python

"""
"""

from link.util import name, attr, anno
from link import util
from maya import cmds
from functools import partial
import logging
log = logging.getLogger(__name__)

class Module(object):
    '''Built stuff like rigs'''

    def __init__(self, position, description, index=0):
        self.position = position
        self.description = description
        self.index = index
        self.suffix = "mod"

        self.name = name.create_name(self.position, self.description, self.index, self.suffix)
        
        self.nodes = []
        self.controls = {}
        self.setups = []

    def _create_module_nodes(self):
        """Create top nodes and settings"""

        # Create nodes
        self.top_node = cmds.createNode("transform", name=self.name)
        self.control_node = cmds.createNode("transform", name=name.set_description_suffix(self.name, "control"))
        self.setup_node = cmds.createNode("transform", name=name.set_description_suffix(self.name, "setup"))
        cmds.parent([self.setup_node, self.control_node], self.top_node)

        # Lock attrs
        attr.lock_all(self.top_node)
        attr.lock_all(self.control_node)
        attr.lock_all(self.setup_node)

        # Create settings node
        loc = cmds.spaceLocator(name=name.set_suffix(self.name, "settings"))[0]
        shape = cmds.listRelatives(loc, shapes=True)[0]
        attr.lock_all(loc)

        # Hide these
        for local in ["localPosition", "localScale"]:
            for axis in ["X", "Y", "Z"]:
                attr_path = "%s.%s%s" % (shape, local, axis)
                cmds.setAttr(attr_path, cb=False)

        cmds.setAttr("%s.overrideEnabled" % shape, True)
        cmds.setAttr("%s.overrideColor" % shape, 17)

        self.settings_node = shape
        cmds.parent(loc, self.top_node)

        # Hide shape
        cmds.setAttr("%s.visibility" % shape, 0)

    def _pre_create(self):
        pass

    def _create(self):
        pass

    def _post_create(self):
        pass

    def create(self):
        log.info("%s" % self.__class__.__name__)

        # Necessary part nodes
        self._create_module_nodes()

        # Creation process
        self._pre_create()
        self._create()
        self._post_create()

        # Parent nodes
        self._tidy_up()

    def _tidy_up(self):
        """Move nodes around into their modular containers"""

        # Put controls under control group
        for key, ctl in self.controls.items():
            if ctl.grp in cmds.ls(assemblies=True):
                cmds.parent(ctl.grp, self.control_node)

        # Connect vis and parent under setup node
        for node in set(self.setups):            

            cons = cmds.listConnections("%s.visibility" % node, source=True, destination=False, plugs=True) or []
            if not cons:
                cmds.connectAttr("%s.helpers" % self.settings_node, "%s.visibility" % node, force=True)

            if node in cmds.ls(assemblies=True):
                cmds.parent(node, self.setup_node)









