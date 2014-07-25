
from link.util import name
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
        self.top_node = cmds.createNode("transform", name=self.name)

    def _create(self):
        pass

    def _post_create(self):
        pass

    def create(self):
        log.info("%s" % self.__class__.__name__)
        self._pre_create()
        self._create()
        self._post_create()
