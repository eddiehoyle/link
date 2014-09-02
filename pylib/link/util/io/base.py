#!/usr/bin/env python

"""
Data file handling
"""

import os
import json
import logging

from link.config import Config

log = logging.getLogger(__name__)

class FileHandler2(object):
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

class FileHandler(FileHandler):

    def __init__(self, relative_path):
        self.dir = os.path.join(self.config.root, 'resources')
        self.path = os.path.join(self.dir, rel_path)
        self.data = {}

    def init_data(self):
        """Override method"""
        pass

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def write(self):
        """Write data as json to disk"""

        log.debug("Writing data to disk: %s" % self.path)

        if not self.path:
            raise IOError("No path set.")

        if not os.path.exists(self.dir):
            os.mkdir(self.dir)

        with open(self.path, 'w') as f:
            json.dump(self.data, f)

        return self.path

    def read(self):
        """Read from json file on disk"""

        log.debug("Reading data from disk: %s" % self.path)

        if not os.path.exists(self.path):
            raise IOError("Data file does not exist: %s" % self.path)

        data = {}
        with open(self.path, 'r') as f:
            try:
                self.data = json.loads(f.read())
            except Exception as e:
                log.error("Failed to parse json data file: %s" % self.path)
                log.error(e)

        self.set_data(data)

        return self.data

    def eval(self):
        """Override method"""
        pass

    
