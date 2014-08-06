#!/usr/bin/env python

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
