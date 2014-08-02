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
    """Generate a name that doesn't exist in scene yet"""

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



#--------------------------------------------#
# Dunno if I wanna use this class or not yet

class Name(object):
    """
    """

    def __init__(self, position, description, type):

        self.__position = position
        self.__description = description
        self.__index = 0
        self.__suffix = type

        self.__name = "%s_%s_%s_%s" % (self.__position,
                                       self.__description,
                                       self.__index,
                                       self.__suffix)

    def __repr__(self):
        return self.get_name()

    def __str__(self):
        return self.get_name()

    def name(self):
        return self.__name

    def position(self):
        return self.__position

    def description(self):
        return self.__description

    def index(self):
        return self.__index

    def suffix(self):
        return self.__suffix

    #-----------#
    # Private

    def __get_position(self):
        return self.__position
    
    def __get_description(self):
        return self.__description
    
    def __get_index(self):
        return self.__index
    
    def __get_suffix(self):
        return self.__suffix
    
    def __set_position(self, position):
        self.__position = position
    
    def __set_description(self, description):
        self.__description = description

    def __set_description(self, description):
        self.__index = index
    
    def __set_suffix(self, suffix):
        self.__suffix = suffix

    def __rebuild(self, func):
        pass


    # property(name, fget=name, fset=None, fdel=None)

    # property(position, fget=__get_position, fset=__set_position, fdel=None)
    # property(index, fget=__get_index, fset=__set_index, fdel=None)
    # property(description, fget=__get_description, fset=__set_description, fdel=None)
    # property(suffix, fget=__get_suffix, fset=__set_suffix, fdel=None)

