#!/usr/bin/env python

from link.util import name, shape
from maya import cmds

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
        _shape = shape.add_shape(joint)
        cmds.setAttr("%s.visibility" % _shape, 0)
        
    return joints

def duplicate_joints(joints, description_suffix):
    """Duplicate joints and rename"""

    temp_joints = cmds.duplicate(joints, rc=True, parentOnly=True)
    new_jnts = []
    for jnt in temp_joints:
        new_jnt = name.set_description_suffix(jnt[:-1], description_suffix)
        cmds.rename(jnt, new_jnt)
        new_jnts.append(new_jnt)

    for jnt in new_jnts:
        _shape = shape.add_shape(jnt)
        cmds.setAttr("%s.visibility" % _shape, 0)

    # Joints may already be at world level
    try:
        cmds.parent(new_jnts[0], world=True)
    except RuntimeError as e:
        pass


    return new_jnts

def create_from_poisitions(positions):
    joints = []
    for vector in positions:
        jnt = cmds.joint(name="jnt", position=vector)
        joints.append(jnt)

    # world_nodes = cmds.ls(assemblies=True)
    joints.reverse()
    for index, jnt in enumerate(joints):
        if index + 1 == len(joints):
            break

        cmds.parent(jnt, joints[index + 1])











