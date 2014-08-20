#!/usr/bin/env python

"""
"""

from link.util import name
from maya import cmds
from link.modules.module import Module
import logging
log = logging.getLogger(__name__)

class Component(Module):
    '''Imports and stuff'''

    def __init__(self, position, description):
        super(Component, self).__init__(position, description)

        self.suffix = "cmp"
        self.name = name.set_suffix(self.name, self.suffix)

    def set_file(self, path):
        self.file = path

    def _collect_imported_nodes(self):
        """Override method"""
        return []

    def import_file(self):
        """Import component file"""

        log.info("Importing file: %s" % self.file)

        temp_namespace = "temp"
        cmds.file(self.file, i=True, namespace=temp_namespace)

        # Collect component nodes
        nodes = self._collect_imported_nodes()
        for node in nodes:

            # Check for duplicates
            if node.count("|"):
                e = "Duplicate node detected %s in component %s" % (node, self.__class__.__name__)
                log.error(e)
                raise RuntimeError(e)

            # Rename
            clean_node = ":".join(node.split(":")[1:])
            try:
                cmds.rename(node, clean_node)
                self.nodes.append(clean_node)
            except:
                pass

        cmds.namespace(removeNamespace=temp_namespace, mergeNamespaceWithRoot=True, force=True)

        # Add to controls

    def _create(self):
        self.import_file()


    def _tidy_up(self):
        super(Component, self)._tidy_up()

        # Parent nodes under control node
        for n in self.nodes:
            if n in cmds.ls(assemblies=True):
                cmds.parent(n, self.control_node)


