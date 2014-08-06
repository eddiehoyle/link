#!/usr/bin/env python

from link.util.control.shape import Shape
from link.util.control.transform import Transform
from link import util
from maya import cmds
import logging
log = logging.getLogger(__name__)

class Control(object):
    def __init__(self, position, description, index=0, style="square"):

        self.position = position
        self.description = description
        self.index = index
        self.suffix = "ctl"

        self.name = util.name.create_name(self.position, self.description, self.index, self.suffix)

        self._group = None
        self._transform = Transform(self.name)
        self._shape = Shape(self.name)
        self._style = style

        self.joint = None

    def __setattr__(self, attr, value):
        super(Control, self).__setattr__(attr, value)

    @property
    def ctl(self):
        return self._transform.node

    @property
    def shapes(self):
        return self._shape.nodes

    @property
    def style(self):
        return self._style

    @property
    def grp(self):
        return self._group

    def create(self):

        self._group = cmds.createNode("transform", name=util.name.set_suffix(self.name, "grp"))
        self._transform.create()
        self._shape.create(self.ctl, style=self._style)

        cmds.parent(self.ctl, self.grp)

    def set_style(self, style):
        self._shape.set_style(style)

    def scale_shapes(self, value):
        self._shape.scale_shapes(value)

    def rotate_shapes(self, value, world=False):
        self._shape.rotate_shapes(value, world=world)

    def lock_translates(self):
        util.attr.lock_translates(self.ctl)

    def lock_rotates(self):
        util.attr.lock_rotates(self.ctl)

    def lock_scales(self):
        util.attr.lock_scales(self.ctl)

    def lock_all(self):
        util.attr.lock_all(self.ctl)

    def lock_vis(self):
        util.attr.lock_vis(self.ctl)

    def set_translates(self, array, world=False):
        util.xform.set_translates(self.grp, array, world=world)

    def set_rotates(self, array, world=False):
        util.xform.set_rotates(self.grp, array, world=world)

    def set_point_offset(self, vector, world=False):
        util.xform.set_translates(self.grp, vector, world=world)

    def set_orient_offset(self, vector, world=False):
        util.xform.set_rotates(self.grp, vector, world=world)
