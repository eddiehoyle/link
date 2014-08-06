#!/usr/bin/env python

from maya import cmds
from link.util import name

def aim(source, target, string):
    """Create annotation and aim it at target"""

    anno = add(source, string)
    target = cmds.listRelatives(target, shapes=True)[0]
    cmds.setAttr("%s.displayArrow" % anno, True)
    cmds.connectAttr("%s.worldMatrix[0]" % target, "%s.dagObjectMatrix[0]" % anno, force=True)

    return anno

def create(string):
    """Create base annotation"""

    anno = cmds.createNode('annotationShape')
    cmds.setAttr("%s.overrideEnabled" % anno, True)
    cmds.setAttr("%s.overrideColor" % anno, 18)
    cmds.setAttr("%s.displayArrow" % anno, False)
    cmds.setAttr("%s.text" % anno, string, type="string")
    transform = cmds.listRelatives(anno, parent=True)[0]

    return transform, anno

def add(source, string):
    """Add to node"""

    transform, anno = create(string)
    cmds.parent(anno, source, shape=True, relative=True)
    cmds.delete(transform)
    target = cmds.listRelatives(source, shapes=True)[0]
    cmds.connectAttr("%s.worldMatrix[0]" % target, "%s.dagObjectMatrix[0]" % anno, force=True)

    return anno
