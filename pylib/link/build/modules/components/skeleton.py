from maya import cmds
from link.build.modules.components.component import Component

class Skeleton(Component):
    '''Imports and stuff'''

    def __init__(self, position, description):
        super(Skeleton, self).__init__(position, description)

    def _collect_imported_nodes(self):
        """Only collect joints"""

        return cmds.ls("temp:*", type="joint")

    def connect_settings(self):
        """Connect component nodes to settings node"""
        
        # Add settings
        cmds.addAttr(self.settings_node, ln="displayType", at="double", min=0, max=2)
        cmds.setAttr("%s.displayType" % self.settings_node, cb=True)
        cmds.setAttr("%s.displayType" % self.settings_node, k=False)

        for joint in self.nodes:
            cmds.setAttr("%s.overrideEnabled" % joint, True)
            cmds.connectAttr("%s.displayType" % self.settings_node, "%s.overrideDisplayType" % joint)





