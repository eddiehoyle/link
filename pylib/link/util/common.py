#!/usr/bin/env python

"""
Common utility methods for Maya
"""

from maya import cmds

def get_color_index(position):
		"""Get color index for position"""

		colors = {"blue": 6,
							"red": 13,
							"yellow": 17,
							"light_blue": 18,
							"pink": 20,
							"purple": 30}

		positions = {"C": "yellow",
								 "R": "red",
								 "L": "blue"}

		index = colors.get(positions.get(position[0], None), None)
		if not index:
				raise KeyError("Position color index '%s' not recognised." % position)

		return index

def get_top_parent(node):
	"""Get top of hierarchy"""

	top_node = cmds.listRelatives(node, p=True)
	while top_node:
		node = top_node[0]
		top_node = cmds.listRelatives(node, p=True)
	return node

def create_distance(start, end):
		loc_start = cmds.spaceLocator()[0]
		loc_end = cmds.spaceLocator()[0]
		dst_node = cmds.createNode("distanceBetween")

		cmds.connectAttr("%s.worldPosition[0]" % cmds.listRelatives(loc_start, shapes=True)[0],
										 "%s.point1" % (dst_node))
		cmds.connectAttr("%s.worldPosition[0]" % cmds.listRelatives(loc_end, shapes=True)[0],
										 "%s.point2" % (dst_node))

		start_pos = cmds.xform(start, q=True, ws=True, t=True)
		end_pos = cmds.xform(end, q=True, ws=True, t=True)

		cmds.xform(loc_start, ws=True, t=start_pos)
		cmds.xform(loc_end, ws=True, t=end_pos)

		return (loc_start, loc_end, dst_node)


def get_distance(start, end):
		"""Get distance between two nodes"""

		loc_start, loc_end, dst_node = create_distance(start, end)
		distance = cmds.getAttr("%s.distance" % dst_node)

		cmds.delete([loc_start, loc_end, dst_node])

		return distance

def blend_attributes(input1, input2, driver):
		"""Create blend node with inputs and driver attr"""

		bc = cmds.createNode('blendColors')
		cmds.connectAttr(input1, "%s.color1R" % bc)
		cmds.connectAttr(input2, "%s.color2R" % bc)
		cmds.connectAttr(driver, "%s.blender" % bc)
		return bc

def add_reverse_md(attr1, attr2):
	md = cmds.createNode("multiplyDivide")
	cmds.connectAttr(attr1, "%s.input1X" % md)
	cmds.connectAttr("%s.outputX" % md, attr2, force=True)
	cmds.setAttr("%s.input2X" % md, -1)
	return md






