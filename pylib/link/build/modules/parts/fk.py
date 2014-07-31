
from link.util import name, xform
from link.util import common
from link.util.control.control import Control
from maya import cmds
from link.build.modules.parts.simple import Simple

class Fk(Simple):
    '''Basic FK control with no hierarchy'''

    def __init__(self, position, description):
        super(Fk, self).__init__(position, description)

        self.description = "%sFk" % description

    def create_controls(self):
        """Create controls"""
        super(Fk, self).create_controls()

        for key, ctl in self.controls.items():

            # Fk circles
            ctl.set_style("circle")

            # Lock transforms
            ctl.lock_translates()
            ctl.lock_scales()

        return self.controls

    def connect_controls(self):
        """Connect controls"""
        for key, joint in zip(self.controls.keys(), self.joints):
            cmds.orientConstraint(self.controls[key].ctl, joint, mo=True)

    def omit_last_control(self):
        """Delete last control"""

        if self.controls:
            last = self.get_control(-1)
            cmds.delete(last.grp)
            del self.controls[last.name]


class FkChain(Fk):
    """Hierarchical FK chain"""

    def __init__(self, position, description):
        super(FkChain, self).__init__(position, description)

    def _post_create(self):
        super(FkChain, self)._post_create()
        """Create hierarchy"""

        # Create chain
        for key, ctl in self.controls.items():
            index = name.get_index(key)
            child_ctl = self.controls.get(name.set_index(key, index + 1), None)
            if child_ctl:
                cmds.parent(child_ctl.grp, ctl.ctl)
