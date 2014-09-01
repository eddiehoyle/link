#!/usr/bin/env python

"""
"""

from link.config import Config
from maya import cmds
from link.util import name
from link.modules.components.skeleton import Skeleton
from link.modules.components.proxy import Proxy
from link.modules.parts.fk import FkChain
from link.modules.parts.ik import IkRp
from link.modules.parts.simple import Simple
from link.modules.parts.base import Base
from link.modules.parts.ikfk import IkFk
from link.modules.parts.limb import Foot
from link.modules.parts.spline import IkSpline, IkFkSpline
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
        self.create_global()

        # Components
        self.create_skeleton()
        self.create_proxy()

        # Parts
        self.create_hat()
        self.create_neck()
        self.create_spine()
        self.create_root()

        for pos in ['L' , 'R']:
            self.create_arm(pos)
            self.create_leg(pos)

    def _post_build(self):
        self._parent_parts()
        self._parent_components()

        self._load_data()

        for key, part in self.parts.items():
            part.display_helpers(False)

    def _load_data(self):
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
        part.scale_shapes(32)
    
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

        # Shapes and positions
        mult = 1
        if position == 'R':
            mult = -1
        leg_part.ik.pv_ctl.set_translates([9.13346 * mult, 48.869499999999995, 50])
        leg_part.ik.pv_ctl.scale_shapes(0.2)
        leg_part.ik.pv_ctl.rotate_shapes([-90, 0, 0])
        leg_part.ik.ik_ctl.set_style("square")

        # Foot
        foot_part = Foot(position, 'foot')
        joints = ["%s_leg_2_jnt" % (position)]
        joints.extend(["%s_foot_%s_jnt" % (position, index) for index in range(2)])
        foot_part.set_joints(joints)
        foot_part.set_part_file('/Users/eddiehoyle/Python/link/resources/data/parts/%s_foot_0.json' % position)
        foot_part.set_settings_file('/Users/eddiehoyle/Python/link/resources/data/settings/%s_foot_0.json' % position)
        foot_part.create()
        foot_part.scale_shapes(3)

        self.append_part(foot_part)

        # Connect foot to leg
        ik_handle_grp = cmds.listRelatives(leg_part.ik.ik, p=True)[0]
        cmds.parentConstraint(foot_part.pivot_detail['ball'], ik_handle_grp, mo=True)
        foot_con = cmds.parentConstraint([leg_part.ik.ik_ctl.ctl, 
                                          leg_part.fk.get_control(-1).ctl],
                                          cmds.listRelatives(foot_part.pivot_detail['heel'], p=True)[0],
                                          mo=True)[0]

        foot_rev = cmds.createNode("reverse", name=name.create_name(position, "footIkFk", 0, "rev"))
        aliases = cmds.parentConstraint(foot_con, wal=True, q=True)

        cmds.connectAttr("%s.fkik" % leg_part.settings_node, "%s.%s" % (foot_con, aliases[0]))
        cmds.connectAttr("%s.fkik" % leg_part.settings_node, "%s.inputX" % foot_rev)
        cmds.connectAttr("%s.outputX" % foot_rev, "%s.%s" % (foot_con, aliases[1]))

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
