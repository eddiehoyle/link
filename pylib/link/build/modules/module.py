
from link.util import name, attr, anno
from maya import cmds
import logging
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

    def _pre_create(self):
        """Create top nodes and settings"""

        # Create top node
        self.top_node = cmds.createNode("transform", name=self.name)

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

        # Hide shape
        cmds.setAttr("%s.visibility" % shape, 0)
        # anno.add(loc, loc)

        self.settings_node = shape

    def _create(self):
        pass

    def _post_create(self):
        pass

    def create(self):
        log.info("%s" % self.__class__.__name__)
        self._pre_create()
        self._create()
        self._post_create()

        self.connect_settings()

    def connect_settings(self):
        pass
