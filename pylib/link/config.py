#!/usr/bin/env python

import re
import os
from ConfigParser import ConfigParser

class Config(object):
    """docstring for Config"""

    def __init__(self):
        self.config = ConfigParser()
        self.root = os.path.dirname("{sep}".join(os.path.abspath(__file__).split(os.sep)[:-2]).format(sep=os.sep))
        self.path = os.path.join(self.root, "config", "link.cfg")
        self.config.read(self.path)
