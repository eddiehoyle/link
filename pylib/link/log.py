#!/usr/bin/env pythong

"""
Project log settings
"""

import logging

from link.config import Config

def main():
    config = Config()
    level = config.config.get("log", "level")

    logging.basicConfig()
    log = logging.getLogger('link')
    log.setLevel(getattr(logging, level))

if __name__ == 'link.log':
    main()
