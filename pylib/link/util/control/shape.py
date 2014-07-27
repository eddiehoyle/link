#!/usr/bin/env python

from maya import cmds
from link.util.control.style import Style
import logging
log = logging.getLogger(__name__)

class Shape(object):
    """
    Shape manipulation object
    """
    def __init__(self, name):

        self.name = "%sShape" % name
        self.nodes = []
        self.parent = None
        self.scale = 1
        self.rotate = [0.0, 0.0, 0.0]

    def create(self, parent_transform, style):
        """Create shape"""

        self.parent = parent_transform

        # Add style
        curve_data = Style()[style]
        for curve in curve_data:
            temp = cmds.curve(name="temp_curve", d=1, p=curve['points'], k=curve['knot'])

            # Parent curve under transform
            shapes = cmds.listRelatives(temp, shapes=True)
            for shape_index, shape in enumerate(shapes):
                cmds.parent(shape, parent_transform, shape=True, r=True)

                # Rename shape to be tidy
                new_shape = cmds.rename(shape, "%s%s" % (self.name, shape_index))
                self.nodes.append(new_shape)

            # Remove temp transform
            cmds.delete(temp)

        # Match vlaues
        self.set_scale(self.scale)
        self.set_rotate(self.rotate)

        # Clear selection
        cmds.select(cl=True)

    def set_style(self, style):
        """Rebuild shape"""

        if Style().exists(style):
            parent_transform = self.parent
            cmds.delete(self.nodes)
            self.create(parent_transform, style)
        else:
            log.error("Shape style doesn't exist: '%s'" % style)

    def set_scale(self, value):
        """Scale shape"""

        cl_shape, cl_transform = cmds.cluster(self.nodes)
        cmds.setAttr("%s.scale" % cl_transform, value, value, value, type="float3")

        cmds.delete(self.nodes, ch=True)
        self.scale = value

    def set_rotate(self, array):
        """Rotate shape"""

        cl_shape, cl_transform = cmds.cluster(self.nodes)
        cmds.setAttr("%s.rotate" % cl_transform, *array, type="float3")

        cmds.delete(self.nodes, ch=True)
        self.rotate = array