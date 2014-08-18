#!/usr/bin/env python

from maya import cmds

def add_shape(transform):
    l = cmds.createNode("locator", name="temp_locator_shape".encode('base64'))
    p = cmds.listRelatives(l, p=True)[0]
    cmds.parent(l, transform, shape=True, r=1)
    shape = cmds.rename(l, transform+"Shape")
    cmds.delete(p)
    return shape
