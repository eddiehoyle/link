#!/usr/bin/env python

"""
Settings node file handling
"""

import os
import json
import logging

from link.util.io.base import FileHandler
from link.config import Config

log = logging.getLogger(__name__)

class SettingsFileHandler(FileHandler):

    def __init__(self, key):
        super(SettingsFileHandler, self).__init__(key)

        self.dir = self.config.get_settings_dir()
        self.path = os.path.join(self.dir, "%s.json" % self.key)
