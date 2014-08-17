#!/usr/bin/env python

import logging
logger = logging.getLogger(__name__)

from maya import cmds

def tidy_shape_names():
    """Rename mesh to match parent transform"""

    meshes = cmds.ls(type="mesh")

    rename_count = 0
    for mesh in meshes:
        transform = cmds.listRelatives(mesh, parent=True)[0]

        # Rename
        index = 0 
        shape_name = "%sShape%s" % (transform, index) 
        while cmds.objExists(shape_name):
            index += 1
            shape_name = "%sShape%s" % (transform, index) 

        cmds.rename(mesh, shape_name)
        rename_count +=1

    logger.debug("Renamed %s node(s)" % rename_count)
