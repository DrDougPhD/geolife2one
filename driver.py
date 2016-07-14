#!/usr/bin/env python
"""
SYNOPSIS

    python driver.py [-h,--help] [-v,--verbose] [-d,--directory DIRECTORY]

DESCRIPTION

    Blah blah.

ARGUMENTS

  -h, --help            show this help message and exit
  -v, --verbose         verbose output
  -d DIRECTORY, --directory DIRECTORY
                        directory where GeoLife dataset is stored
                        (default: ./data)
  -l LOGFILE, --log-file LOGFILE
                        log file to record all debug messages 
                        (default: ./geolife2one.log)
AUTHOR

    Doug McGeehan <doug.mcgeehan@mst.edu>

LICENSE

    This script is placed under the MIT License. Please refer to LICENSE file
    for more details.
    The GeoLife GPS Trajectory dataset is placed under the Microsoft Research
    License Agreement that is described in its user guide that is included in
    its ZIP archive.

"""

import argparse
from data import dataset
import logging
logger = logging.getLogger("geolife2one")
import os
import sys
from datetime import datetime


def parse_args():
    """
    Parse the arguments provided by the command-line interface.
    """
    parser = argparse.ArgumentParser(
        description="Verify, unpack, or download the GeoLife GPS trajectory"
                    " dataset for further processing."
    )
    parser.add_argument('-v', '--verbose', action='store_true',
                        default=False, help='verbose output')
    parser.add_argument('-d', '--directory', dest='directory',
                        default="./data",
                        help="directory where GeoLife dataset is stored")
    parser.add_argument('-l', '--log-file', dest='logfile',
                        default="./geolife2one.log",
                        help="log file to record all debug messages")

    return parser.parse_args()


def logging_setup(args):
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


if __name__ == '__main__':
    start_time = datetime.now()
    args = parse_args()
    logging_setup(args)

    try:
        logger.debug(start_time)

        dataset_root = dataset.verify(args.directory)

        finish_time = datetime.now()
        logger.debug(finish_time)
        logger.debug('Execution time: {time}'.format(
            time=(finish_time - start_time)
        ))

        sys.exit(0)

    except KeyboardInterrupt, e: # Ctrl-C
        raise e

    except SystemExit, e: # sys.exit()
        raise e

    except Exception, e:
        logger.exception("Something happened and I don't know what to do D:")
        sys.exit(1)

