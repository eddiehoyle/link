
from link.util import name, xform
from link.util import node, common
from link.util.control.control import Control
from maya import cmds
from link.build.modules.parts.part import Part
from link.build.modules.parts.ik import Ik
from link.build.modules.parts.fk import Fk
import logging
logger = logging.getLogger(__name__)

class IkFk(Part):
    '''Basic Ik and Fk swap'''

    def __init__(self, position, description):
        super(IkFk, self).__init__(position, description)

        self.joints = []
        self.controls = {}

        self.ik = Ik(position, description)
        self.fk = Fk(position, description)

    def set_joints(self, joints):
        print 'joints', joints
        self.ik.set_joints(joints)
        self.fk.set_joints(joints)

    def create_controls(self):
        ik_controls = self.ik.create_controls()
        fk_controls = self.fk.create_controls()

        self.fk.rotate_shapes([0, 0, 90])
        self.fk.scale_shapes(4)

        last_fk_ctl = self.fk.get_control(-1)
        cmds.delete(last_fk_ctl)
        del fk_controls[last_fk_ctl]

        self.controls.update(ik_controls)
        self.controls.update(fk_controls)

    def connect_controls(self):
        self.ik.connect_controls()
        self.fk.connect_controls()

    def match_controls(self):
        self.ik.match_controls()
        self.fk.match_controls()

    def add_stretch(self):
        self.ik.add_stretch()
