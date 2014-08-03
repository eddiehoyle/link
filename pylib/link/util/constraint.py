#!/usr/bin/env python

from maya import cmds

def extend_constraint(new_parent, constraint):
    con = constraint
    aliases = cmds.parentConstraint(con, wal=True)

    cmds.connectAttr('%s.parentMatrix[0]' % new_parent, '%s.target[%s].targetParentMatrix' % (con, len(aliases)))
    cmds.connectAttr('%s.scale' % new_parent, '%s.target[%s].targetScale' % (con, len(aliases)))
    cmds.connectAttr('%s.rotateOrder' % new_parent, '%s.target[%s].targetRotateOrder' % (con, len(aliases)))
    cmds.connectAttr('%s.rotate' % new_parent, '%s.target[%s].targetRotate' % (con, len(aliases)))
    cmds.connectAttr('%s.rotatePivotTranslate' % new_parent, '%s.target[%s].targetRotateTranslate' % (con, len(aliases)))
    cmds.connectAttr('%s.rotatePivot' % new_parent, '%s.target[%s].targetRotatePivot' % (con, len(aliases)))
    cmds.connectAttr('%s.translate' % new_parent, '%s.target[%s].targetTranslate' % (con, len(aliases)))

    new_alias = "%sW%s" % (new_parent, len(aliases))
    cmds.addAttr(con, ln=new_alias, at="double", min=0, dv=1)
    cmds.setAttr("%s.%s" % (con, new_alias), cb=True)
    cmds.setAttr("%s.%s" % (con, new_alias), k=True)
    cmds.connectAttr("%s.%s" % (con, new_alias), "%s.target[%s].targetWeight" % (con, len(aliases)))

    return con
