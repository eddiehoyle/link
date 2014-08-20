#!/usr/bin/env python

"""
"""

import os
from maya import cmds
from link.util.io.base import FileHandler

class ControlFileHandler(FileHandler):
    def __init__(self):
        super(ControlFileHandler, self).__init__()
    
        self.path = os.path.join(self.config.root, self.config.config.get('data', 'control_shapes'))

    def get_data(self):
        ctls = cmds.ls("*ctl", type="transform", long=True)

        data = dict()
        for ctl in ctls:
            
            shapes = cmds.listRelatives(ctl, type="nurbsCurve", children=True) or []
            for shape in cmds.ls(shapes, long=True):

                # Create shape array
                data[shape] = []

                # Get cvs
                cv_range = cmds.getAttr("%s.spans" % shape)
                for index in range(cv_range + 1):
                    cv = "%s.cv[%s]" % (shape, index)

                    pos = cmds.xform(cv, q=True, ws=True, os=False, t=True)
                    data[shape].append([index, pos])

        return self.data

    def apply(self):
        data = self.read()

        for key, array in data.items():
            
            for cluster in array:
                index, pos = cluster
                attr = "%s.cv[%s]" % (key, index)

                if cmds.objExists(attr):
                    cmds.xform(attr, t=pos, ws=True)


# from link.util import python as p;p.flush()
# from link.io import control
# t=control.ControlFileHandler()
# t.get_data()
