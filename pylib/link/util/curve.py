#!/usr/bin/env python

from maya import cmds
from link import util

def create_line_curve(transform0, transform1):
    """Create a curve between two transforms"""
    curve = util.name.set_description_suffix(transform0, "line")
    pos, desc, i, suf = util.name.decompile(transform0)


    curve = util.name.create_name(pos, desc + "Crv", i, "null")
    cmds.curve(name=curve, d=1, p=[[0, 0, 0], [0, 0, 0]], k=[0, 1])

    cls0 = cmds.cluster("%s.cv[0]" % curve, name=util.name.generate_name(pos, desc + "Cls", i, "cls"))[1]
    cls1 = cmds.cluster("%s.cv[1]" % curve, name=util.name.generate_name(pos, desc + "Cls", i, "cls"))[1]
    
    cmds.parent(cls0, transform0, r=True)
    cmds.parent(cls1, transform1, r=True)

    for cls in [cls0, cls1]:
        util.attr.lock_all(cls)    
        cmds.setAttr("%s.visibility" % cls, 0)

    crv_shape = cmds.listRelatives(curve, shapes=True)[0]
    cmds.setAttr("%s.overrideEnabled" % crv_shape, True)
    cmds.setAttr("%s.overrideDisplayType" % crv_shape, 2)

    return curve
