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
    def __init__(self):

        self.config = Config()
        self.path = os.path.join(self.config.root)

    def get_data(self):
        return {}

    def write(self, data=None):
        """Write data as json to disk"""

        data = data or self.get_data()
        log.debug("Writing data key(s): %s" % len(data.keys()))

        with open(self.path, 'w') as f:
            json.dump(data, f)

        log.debug("Data written to disk: %s" % self.path)
        return self.path

    def read(self):
        """Read from json file on disk"""

        with open(self.path, 'r') as f:
            data = json.loads(f.read())

        return data
