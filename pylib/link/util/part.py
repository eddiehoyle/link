#!/usr/bin/env python

from maya import cmds

def connect_ikfk(part):
    """Connect Ik and Fk part"""

    orient = part.ik.ik_orient
    aliases = cmds.parentConstraint(orient, q=True, wal=True)

    rev = cmds.createNode("reverse")
    cmds.connectAttr("%s.fkik" % part.settings_node, "%s.inputX" % rev)

    # Drive swap
    cmds.connectAttr("%s.outputX" % rev, "%s.%s" % (orient, aliases[1]))
    cmds.connectAttr("%s.fkik" % part.settings_node, "%s.%s" % (orient, aliases[0]))

    # Fk control vis
    for fk_key, fk_ctl in part.fk.controls.items():
        cmds.connectAttr("%s.outputX" % rev, "%s.visibility" % fk_ctl.grp)

    # Ik control vis
    cmds.connectAttr("%s.fkik" % part.settings_node, "%s.visibility" % part.ik.ik_ctl.grp)
    cmds.connectAttr("%s.fkik" % part.settings_node, "%s.visibility" % part.ik.polevector_ctl.grp)
