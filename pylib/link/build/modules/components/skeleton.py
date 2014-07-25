from maya import cmds
from link.build.modules.components.component import Component

class Skeleton(Component):
    '''Imports and stuff'''

    def __init__(self, position, description):
        super(Skeleton, self).__init__(position, description)

    def _collect_imported_nodes(self):
        """Only collect joints"""

        return cmds.ls("temp:*", type="joint")





