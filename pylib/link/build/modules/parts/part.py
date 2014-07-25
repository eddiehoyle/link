from link.util import name
from maya import cmds
from link.build.modules.module import Module

class Part(Module):
    '''Imports and stuff'''

    def __init__(self, position, description):
        super(Part, self).__init__(position, description)

        self.suffix = "prt"
        self.name = name.set_suffix(self.name, self.suffix)

    def create_controls(self):
        pass

    def match_controls(self):
        pass

    def connect_controls(self):
        pass
