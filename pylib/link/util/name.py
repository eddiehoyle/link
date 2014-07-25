#!/usr/bin/env python

"""
Module related to all string related naming and creation.
"""

from maya import cmds
import re
import logging
logging.getLogger(__name__)

def create_name(position, description, index=0, suffix="grp"):
    """Compile a name"""

    return "%s_%s_%s_%s" % (position, description, index, suffix)

def generate_name(position, description, index=0, suffix="grp"):
    """Generate a name that doesn't exist yet in scene"""

    name = create_name(position, description, index, suffix)
    while cmds.objExists(name):
        index += 1
        name = create_name(position, description, index, suffix)
    return name

def decompile(string):
    data = None
    if string.count("_") == 3:
        data = string.split("_")
    return data

def get_position(string):
    return decompile(string)[0]

def get_description(string):
    return decompile(string)[1]

def get_index(string):
    return int(decompile(string)[2])

def get_suffix(string):
    return decompile(string)[3]

def get_description_suffix(string):
    description = get_description(string)
    pattern = re.compile(r"([A-Z]?[^A-Z]+)")
    description_suffix = re.findall(pattern, description)[-1]
    return description_suffix

def get_opposite_position(position):
    data = None
    if position.startswith("L"):
        data = "R"
    elif position.startswith("R"):
        data = "L"
    else:
        raise NameError("Position not recognised: '%s'" % position)
    return data
def set_position(name, position):
    data = decompile(name)
    data[0] = position
    return "_".join(data)

def set_description(name, description):
    data = decompile(name)
    data[1] = description
    return "_".join(data)

def set_index(name, index):
    data = decompile(name)
    data[2] = str(index)
    return "_".join(data)

def set_suffix(name, suffix):
    data = decompile(name)
    data[3] = suffix
    return "_".join(data)

def set_description_suffix(name, description_suffix):
    description = get_description(name)
    description += description_suffix.capitalize()
    return set_description(name, description)
















# class Name(object):
#     def __init__(self, position, description, type):
#         self.position = position
#         self.description = description
#         self.index = 0
#         self.type = type

#         self.__generate_name()

#     def __generate_name(self):
#         """Create unique name"""

#         name = "%s_%s_%s_%s" % (self.position, self.description, self.index, self.type)
#         while cmds.objExists(name):
#             self.index += 1
#             name = "%s_%s_%s_%s" % (self.position, self.description, self.index, self.type)
#         self.name = name

#     def set_position(self, position):
#         self.position = position
#         return "%s_%s_%s_%s" % (self.position, self.description, self.index, self.type)

#     def set_description(self, description):
#         self.description = description
#         return "%s_%s_%s_%s" % (self.position, self.description, self.index, self.type)

#     def set_type(self, type):
#         self.type = type
#         return "%s_%s_%s_%s" % (self.position, self.description, self.index, self.type)
