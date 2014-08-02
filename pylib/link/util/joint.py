#!/usr/bin/env python

from maya import cmds

def create_chain(num, axis, value, display_local_axis=True):
    joints = []
    for count, i in enumerate(range(num)):
        j = cmds.joint(name="joint%s" % i)
        joints.append(j)

        cmds.setAttr("%s.displayLocalAxis" % j, display_local_axis)

        if count > 0:
            cmds.setAttr("%s.translate%s" % (j, axis.upper()), value)

    cmds.select(joints, r=True)
    cmds.joint(joints, e=True, oj="xyz", secondaryAxisOrient="yup", ch=True, zso=True)

    for j in joints:
        cmds.setAttr("%s.rotateY" % j, -10)
        cmds.joint(j, e=True, spa=True, ch=True)
        cmds.setAttr("%s.rotateY" % j, 0)
    
    return joints

