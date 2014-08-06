#!/usr/bin/env python

from maya import cmds
from link import util

def create_chain(num, axis, value, description='temp'):
    joints = []
    for count, i in enumerate(range(num)):
        j = cmds.joint(name="C_%s_%s_jnt" % (description, i))
        joints.append(j)

        cmds.setAttr("%s.displayLocalAxis" % j, True)

        if count > 0:
            cmds.setAttr("%s.translate%s" % (j, axis.upper()), value)

    cmds.select(joints, r=True)
    cmds.joint(joints, e=True, oj="xyz", secondaryAxisOrient="yup", ch=True, zso=True)

    for j in joints:
        cmds.setAttr("%s.rotateY" % j, -10)
        cmds.joint(j, e=True, spa=True, ch=True)
        cmds.setAttr("%s.rotateY" % j, 0)

    # Add shapes
    for joint in joints:
        util.shape.add_shape(joint)
        
    return joints

def duplicate_joints(joints, description_suffix):
    """Duplicate joints and rename"""

    temp_joints = cmds.duplicate(joints, rc=True, parentOnly=True)
    new_jnts = []
    for jnt in temp_joints:
        new_jnt = util.name.set_description_suffix(jnt[:-1], description_suffix)
        cmds.rename(jnt, new_jnt)
        new_jnts.append(new_jnt)

    for jnt in new_jnts:
        util.shape.add_shape(jnt)

    cmds.parent(new_jnts[0], world=True)

    return new_jnts
