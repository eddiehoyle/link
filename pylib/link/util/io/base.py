#!/usr/bin/env python

"""
Data file handling
"""

import os
import json
import logging

from link.config import Config

log = logging.getLogger(__name__)

class FileHandler(object):
    def __init__(self, key):

        self.config = Config()

        self.key = key
        self.dir = os.path.join(self.config.root, 'resources')
        self.path = os.path.join(self.dir, "%s.json" % self.key)

    def _create_dir(self):
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)

    def write(self, data):
        """Write data as json to disk"""

        data = data or self.get_data()
        log.debug("Writing data key(s): %s" % len(data.keys()))

        self._create_dir()

        with open(self.path, 'w') as f:
            json.dump(data, f)

        log.debug("Writing data to disk: %s" % self.path)
        return self.path

    def read(self):
        """Read from json file on disk"""

        log.debug("Reading data from disk: %s" % self.path)

        with open(self.path, 'r') as f:
            data = json.loads(f.read())
            log.debug("Reading data key(s): %s" % len(data.keys()))

        return data
