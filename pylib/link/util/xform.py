#!/usr/bin/env python

from maya import cmds

def match(target, source):
    """Match target to source xform"""
    match_position(target, source)
    match_rotate(target, source)

def match_rotate(target, source):
    """Match worldspace rotate"""
    source_rot = cmds.xform(source, q=True, ws=True, ro=True)
    cmds.xform(target, ro=source_rot, ws=True)

def match_position(target, source):
    """Match worldspace position"""
    source_pos = cmds.xform(source, q=True, ws=True, t=True)
    cmds.xform(target, t=source_pos, ws=True)
