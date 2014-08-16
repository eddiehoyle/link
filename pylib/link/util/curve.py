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

def create_curve(positions, degree):
    knots = []
    knots.extend([0 for i in range(degree)])
    knots.extend(range(len(positions) - 1)[1:-2])
    knots.extend([len(positions) - degree for i in range(degree)])
    print 'knots', knots
    return cmds.curve(name="test", d=degree, p=positions, k=knots)

def rebuild_curve(curve, detail):
    return cmds.rebuildCurve(curve, ch=False, replaceOriginal=True, end=1, kr=0, kcp=0, kep=1, kt=0, s=detail)
    # rebuildCurve -ch 0 -rpo 1 -rt 0 -end 1 -kr 0 -kcp 0 -kep 1 -kt 0 -s 3 -d 3 -tol 1.15862e-08 "test";

def create_from_nodes(nodes, degree=3):
    """Create a curve from a bunch of transforms"""
    positions = [cmds.xform(n, q=True, ws=True, t=True) for n in nodes]
    print positions
    # print len(positions)
    crv = create_curve(positions, degree)
