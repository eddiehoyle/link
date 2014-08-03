
from link.util import name, xform
from link.util import common
from link.util.control.control import Control
from maya import cmds
from link.build.modules.parts.simple import Simple

class Base(Simple):
    '''Basic FK control with no hierarchy'''

    def __init__(self, position, description):
        super(Base, self).__init__(position, description)

    def create_controls(self):
        """Create controls"""

        ctl = Control("C", "global")
        ctl.create()
        ctl.set_style("square")

        self.controls[ctl.name] = ctl

        return self.controls

    def connect_controls(self):
        pass

    def match_controls(self):
        pass
