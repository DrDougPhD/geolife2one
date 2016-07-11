#!/usr/bin/env python
"""
SYNOPSIS

    TODO helloworld [-h,--help] [-v,--verbose] [--version]

DESCRIPTION

    TODO This describes how to use this script. This docstring
    will be printed by the script if there is an error or
    if the user requests help (-h or --help).

EXAMPLES

    TODO: Show some examples of how to use this script.

EXIT STATUS

    TODO: List exit codes

AUTHOR

    Doug McGeehan <doug.mcgeehan@mst.edu>

LICENSE

    This script is placed under the MIT License. Please refer to LICENSE file
    in the parent directory for more details.
    The GeoLife GPS Trajectory dataset is placed under the Microsoft Research
    License Agreement that is described in its user guide that is included in
    its ZIP archive.

VERSION

    $Id$
"""

import traceback
import argparse
import time
import os
import sys
import glob
import urllib
import zipfile


#GEOLIFE_ZIP_ARCHIVE_URL="https://download.microsoft.com/download/F/4/8/F4894AA5-FDBC-481E-9285-D5F8C4C4F039/Geolife%20Trajectories%201.3.zip"
GEOLIFE_ZIP_ARCHIVE_URL="http://web.mst.edu/~djmvfb/super_secret/sample.zip"


def verify(directory="."):
    """
    Verify the GeoLife dataset exists in this directory, and if not, make it
    so. Return the dataset's root directory.
    """

    # Check if uncompressed PLX files exist within the specified directory
    try:
        dataset_root = find_geolife_root(directory)

    except PLXNotFound, e:
        # If no PLX files exist in the directory, then check if a ZIP archive
        # exists. If no ZIP archive exists, download it.
        print("GeoLife PLX files not found in '{0}'. Checking for ZIP"
              " archive.".format(directory))

        zip_files = glob.glob(os.path.join(directory, "*.zip"))
        if not zip_files:
            print("No GeoLife ZIP archive. Proceeding with download.")
            geolife_zip = download(url=GEOLIFE_ZIP_ARCHIVE_URL)

        else:
            geolife_zip = zip_files[0]
            print("GeoLife ZIP archive found at '{0}'".format(geolife_zip))

        unpack(archive=geolife_zip, to=directory)
        dataset_root = find_geolife_root(directory)

    return dataset_root


def find_geolife_root(directory_to_search):
    """
    Walk down tree until a PLT file is encountered. If none is found, raise
    an exception.
    """
    directory_containing_plt = None
    for d, subd, files in os.walk(directory_to_search):
        for f in files:
            if f.lower().endswith(".plt"):
                directory_containing_plt = d
                break
    if directory_containing_plt is None:
        raise PLXNotFound

    geolife_root = os.path.abspath(
        os.path.dirname(os.path.dirname(directory_containing_plt))
    )
    print("GeoLife dataset found within '{0}'".format(geolife_root))
    return geolife_root


def download(url):
    """
    Download the GeoLife dataset from Microsoft Research.
    """
    print("Downloading from '{0}'. Please be patient.".format(url))
    print("After this run, downloading shouldn't have to be performed again")
    downloader = urllib.URLopener()
    download_to = os.path.join(".", "geolife.zip")
    downloader.retrieve(url, download_to)
    print("Download complete!")
    return download_to


def unpack(archive, to):
    """
    Unpack the zip archive.
    """
    print("Unpacking ZIP archive '{0}' to '{1}'. Please be patient.".format(
        archive, to
    ))
    print("After this run, unpacking shouldn't have to be performed again")
    unzipper = zipfile.ZipFile(archive, 'r')
    unzipper.extractall(to)
    unzipper.close()
    print("Unpacking complete!")


class PLXNotFound(IOError):
    def __init__(self,*args,**kwargs):
        IOError.__init__(self,*args,**kwargs)


if __name__ == '__main__':
  try:
    start_time = time.time()

    parser = argparse.ArgumentParser(
      description="Verify, unpack, or download the GeoLife GPS trajectory"
                  " dataset for further processing."
    )
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='verbose output')
    parser.add_argument('-d', '--directory', dest='directory', default=".",
                        help="directory where GeoLife dataset is stored")
    args = parser.parse_args()

    if args.verbose:
      print(time.asctime())

    verify(args.directory)

    if args.verbose: 
      print(time.asctime())
      print('Execution time (minutes): {time}'.format(
        time=(time.time() - start_time) / 60.0
      ))

    sys.exit(0)

  except KeyboardInterrupt, e: # Ctrl-C
    raise e

  except SystemExit, e: # sys.exit()
    raise e

  except Exception, e:
    print(e)
    traceback.print_exc()
    sys.exit("ERROR, UNEXPECTED EXCEPTION")

