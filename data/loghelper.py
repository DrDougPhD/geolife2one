#!/usr/bin/env python
"""
AUTHOR

    Doug McGeehan <doug.mcgeehan@mst.edu>

LICENSE

    This script is placed under the MIT License. Please refer to LICENSE file
    in the parent directory for more details.
    The GeoLife GPS Trajectory dataset is placed under the Microsoft Research
    License Agreement that is described in its user guide that is included in
    its ZIP archive.

"""

import os
import logging

def setup(args):
    loggerName = os.path.splitext(os.path.basename(args.logfile))[0]
    logger = logging.getLogger(loggerName)
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(args.logfile)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()

    if args.verbose:
        ch.setLevel(logging.DEBUG)

    else:
        ch.setLevel(logging.INFO)

    # create formatter and add it to the handlers
    fh.setFormatter(logging.Formatter(
      '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    ch.setFormatter(logging.Formatter(
      '%(levelname)s - %(message)s'
    ))
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

