#!/usr/bin/env python

"""
"""

from link.util import attr, name, xform
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

        self.name = name.create_name(self.position, self.description, self.index, self.suffix)

        self._group = None
        self._inb = None
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
    def inb(self):
        return self._inb

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
        self._inb = cmds.createNode("transform", name=name.set_suffix(self.name, "inb"))
        self._shape.create(self.ctl, style=self._style)

        cmds.parent(self.ctl, self.inb)
        cmds.parent(self.inb, self.grp)

        # Lock vis auto
        self.lock_vis()

    def set_style(self, style):
        cons = []
        for node in self.shapes:
            in_cons_src = cmds.listConnections(node, plugs=True, source=True) or []
            in_cons_dst = []
            for in_con in in_cons_src:
                dst_con = cmds.listConnections(in_con, d=True, p=True)[0]
                in_cons_dst.append(dst_con)

            out_cons_src = cmds.listConnections(node, plugs=True, d=True) or []
            out_cons_dst = []
            for out_con in out_cons_src:
                dst_con = cmds.listConnections(out_con, s=True, p=True)[0]
                out_cons_dst.append(dst_con)

            cons.append([in_cons_src, in_cons_dst, out_cons_src, out_cons_dst])

        self._shape.set_style(style)

        for con in cons:
            in_cons_src, in_cons_dst, out_cons_src, out_cons_dst = con
            for in_src, in_dst in zip(in_cons_src, in_cons_dst):
                print 'in', in_src, in_dst
                # cmds.connectAttr(in_src, in_dst)

            for out_src, out_dst in zip(out_cons_src, out_cons_dst):
                print 'out', out_src, out_dst
                # cmds.connectAttr(out_src, out_dst)


    def scale_shapes(self, value):
        self._shape.scale_shapes(value)

    def rotate_shapes(self, value, world=False):
        self._shape.rotate_shapes(value, world=world)

    def lock_translates(self):
        attr.lock_translates(self.ctl)

    def lock_rotates(self):
        attr.lock_rotates(self.ctl)

    def lock_scales(self):
        attr.lock_scales(self.ctl)

    def lock_all(self):
        attr.lock_all(self.ctl)

    def lock_vis(self):
        attr.lock_vis(self.ctl)

    def set_translates(self, array, world=False):
        xform.set_translates(self.grp, array, world=world)

    def set_rotates(self, array, world=False):
        xform.set_rotates(self.grp, array, world=world)

    def set_point_offset(self, vector, world=False):
        xform.set_translates(self.grp, vector, world=world)

    def set_orient_offset(self, vector, world=False):
        xform.set_rotates(self.grp, vector, world=world)
