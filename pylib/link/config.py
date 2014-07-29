#!/usr/bin/env python

import os
from ConfigParser import ConfigParser

class Config(object):
    """docstring for Config"""

    def __init__(self):

        self.config = ConfigParser()
        config_dir = os.path.dirname("{sep}".join(os.path.abspath(__file__).split(os.sep)[:-2]).format(sep=os.sep))
        self.path = os.path.join(config_dir, "config", "link.cfg")
        print self.path
        self.config.read(self.path)
