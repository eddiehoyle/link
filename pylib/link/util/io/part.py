#!/usr/bin/env python

"""
Data file handling
"""

import os
import json
import logging

from link.util.io.base import FileHandler
from link.config import Config

log = logging.getLogger(__name__)

class PartFileHandler(FileHandler):

    def __init__(self, key):
        super(PartFileHandler, self).__init__(key)

        self.dir = self.config.get_parts_dir()
        self.path = os.path.join(self.dir, "%s.json" % self.key)
