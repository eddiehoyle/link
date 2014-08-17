
from link.config import Config
from maya import cmds
from link import util
from link.build.modules.components.skeleton import Skeleton
from link.build.modules.components.proxy import Proxy
from link.build.modules.parts.fk import FkChain
from link.build.modules.parts.ik import IkRp
from link.build.modules.parts.simple import Simple
from link.build.modules.parts.base import Base
from link.build.modules.parts.ikfk import IkFk
from link.build.modules.parts.spline import IkSpline, IkFkSpline
from link.util.io.control import ControlFileHandler

import logging
log = logging.getLogger(__name__)

class Link(object):
    def __init__(self):

        self.asset = "link"

        self.config = Config()
        self.parts = {}
        self.components = {}

    def _pre_build(self):
        cmds.file(new=True, force=True)
        self._create_nodes()

    def _build(self):
        """Create rig"""

        # Global control
        # self.create_global()

        # Components
        self.create_skeleton()
        self.create_proxy()

        # Parts
        # self.create_hat()
        # self.create_neck()
        # self.create_spine()
        # self.create_root()
        # self.create_hip()

        for pos in ['L' , 'R']:
            self.create_arm(pos)
            self.create_leg(pos)

    def _post_build(self):
        self._parent_parts()
        self._parent_components()
        self._parent_settings()

        self._load_data()

    def _load_data(self):
        # ControlFileHandler().apply()
        pass

    def build(self):
        log.info('build')
        self._pre_build()
        self._build()
        self._post_build()

    def _create_nodes(self):

        # Nodes
        self.top_node = cmds.createNode("transform", name=self.asset)
        self.part_node = cmds.createNode("transform", name="parts")
        self.comp_node = cmds.createNode("transform", name="components")
        self.settings_node = cmds.createNode("transform", name="settings")

        cmds.parent([self.part_node, self.comp_node, self.settings_node], self.top_node)

    def _parent_parts(self):
        log.info("Parenting %s part(s)" % len(self.parts.keys()))
        for key, part in self.parts.items():
            cmds.parent(part.top_node, self.part_node)

    def _parent_components(self):
        log.info("Parenting %s component(s)" % len(self.components.keys()))
        for key, comp in self.components.items():
            cmds.parent(comp.top_node, self.comp_node)

    def _parent_settings(self):
        pass
        # for key, comp in self.components.items():
        #     cmds.parent(cmds.listRelatives(comp.settings_node, parent=True)[0], self.settings_node)

        # for key, part in self.parts.items():
            # cmds.parent(cmds.listRelatives(part.settings_node, parent=True)[0], self.settings_node)

            # for ctl_key, ctl in part.controls.items():
            #     cmds.parent(part.settings_node, ctl.ctl, shape=True, add=True)

    def create_skeleton(self):
        component = Skeleton('C', 'skeleton')
        _file = "Users/eddiehoyle/Python/link/resources/skeleton.ma"
        component.set_file(_file)
        component.create()

        self.append_component(component)

    def create_proxy(self):
        component = Proxy('C', 'proxy')
        _file = "Users/eddiehoyle/Python/link/resources/proxy.ma"
        component.set_file(_file)
        component.create()

        self.append_component(component)

    def create_global(self):
        part = Base("C", "global")
        part.create()
        self.append_part(part)

        part.scale_shapes(12)
    
    def create_hat(self):
        hat_part = IkFkSpline("C", "hat")
        joints = ['C_hat_%s_jnt' % i for i in range(6)]
        hat_part.set_joints(joints)
        hat_part.create()
        hat_part.add_stretch()

        self.append_part(hat_part)

    def create_neck(self):
        head_part = FkChain("C", "head")
        joints = ['C_neck_1_jnt', 'C_neck_2_jnt', 'C_head_0_jnt']
        head_part.set_joints(joints)
        head_part.create()
        head_part.add_stretch()

        head_part.rotate_shapes([0, 0, 90])
        head_part.scale_shapes(8)
        self.append_part(head_part)

    def create_arm(self, position):

        # Arm
        arm_part = IkFk(position, 'arm')
        joints = ["%s_arm_%s_jnt" % (position, index) for index in range(3)]
        arm_part.set_joints(joints)
        arm_part.create()
        arm_part.add_stretch()
        arm_part.scale_shapes(6)

        # Custom arm shapes
        arm_part.ik.pv_ctl.scale_shapes(0.4)
        arm_part.ik.pv_ctl.rotate_shapes([90, 0, 0])

        # Pv position
        mult = 1
        if position == 'R':
            mult = -1
        arm_part.ik.pv_ctl.set_translates([46.753 * mult, 137.316, -40])

        # Collar
        collar_part = FkChain(position, 'collar')
        joints = ["%s_collar_0_jnt" % position]
        collar_part.set_joints(joints)
        collar_part.create()
        collar_part.scale_shapes(4)
        collar_part.rotate_shapes([0, 0, 90])

        # Append
        self.append_part(collar_part)
        self.append_part(arm_part)

        # Connect parts
        cmds.parentConstraint(collar_part.get_control(0).ctl, arm_part.fk.get_control(0).grp, sr=['x', 'y', 'z'], mo=True)
        cmds.parentConstraint(collar_part.get_control(0).ctl, arm_part.ik.base_null, sr=['x', 'y', 'z'], mo=True)

    def create_leg(self, position):
        leg_part = IkFk(position, 'leg')
        joints = ["%s_leg_%s_jnt" % (position, index) for index in range(3)]
        leg_part.set_joints(joints)
        leg_part.create()
        leg_part.add_stretch()
        self.append_part(leg_part)

        leg_part.scale_shapes(6)

        # Pv position
        mult = 1
        if position == 'R':
            mult = -1
        leg_part.ik.pv_ctl.set_translates([9.13346 * mult, 48.869499999999995, 50])
        leg_part.ik.pv_ctl.scale_shapes(0.2)
        leg_part.ik.pv_ctl.rotate_shapes([-90, 0, 0])


    def create_hip(self):
        part = Simple('C', 'hip')
        part.set_joints(["C_spine_0_jnt"])
        part.set_orient([0, 0, 0], world=True)
        part.create()  
        self.append_part(part)

        part.scale_shapes(6)

    def create_root(self):
        part = Simple('C', 'root')
        part.set_joints(["C_root_0_jnt"])
        part.set_orient([0, 0, 0], world=True)
        part.create()
        self.append_part(part)
        
        part.scale_shapes(10)

    def create_spine(self):
        part = IkFkSpline('C', 'spine')
        part.set_joints(["C_spine_%s_jnt" % index for index in range(5)])
        part.create()
        part.add_stretch()

        self.append_part(part)
        part.scale_shapes(10)        

    def append_part(self, part):
        self.parts[part.name] = part

    def append_component(self, part):
        self.components[part.name] = part
