#!/usr/bin/env python

from link.util.control.shape import Shape
from link.util.control.transform import Transform
from link.util import name
from maya import cmds
import logging
log = logging.getLogger(__name__)

class Control(object):
    def __init__(self, position, description, index=0, style="square"):

        self.position = position
        self.description = description
        self.index = index
        self.suffix = "ctl"

        self.name = name.create_name(self.position, self.description, self.index, self.suffix)

        self._group = None
        self._transform = Transform(self.name)
        self._shape = Shape(self.name)
        self._style = style

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

        self._group = cmds.createNode("transform", name=name.set_suffix(self.name, "grp"))
        self._transform.create()
        self._shape.create(self.ctl, style=self._style)

        cmds.parent(self.ctl, self.grp)

    def set_style(self, style):
        self._shape.set_style(style)

    def set_scale(self, value):
        self._shape.set_scale(value)

    def set_rotate(self, value):
        self._shape.set_rotate(value)
