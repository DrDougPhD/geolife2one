#!/usr/bin/env python
"""
SYNOPSIS

    python dataset.py [-h,--help] [-v,--verbose] [-d,--directory DIRECTORY]

DESCRIPTION

    Assert the existence of the GeoLife dataset within the specified DIRECTORY.
    If the dataset is not present, this script will first see if a ZIP archive
    is within that directory and will unpack it. If no ZIP archive exists, it
    will download the GeoLife dataset, unpack it, and confirm the unpacking
    resulted in PLX files now existing somewhere under the specified DIRECTORY.

    This script can be used as a stand-alone script or imported into another
    Python script as a module.

ARGUMENTS

  -h, --help            show this help message and exit
  -v, --verbose         verbose output
  -d DIRECTORY, --directory DIRECTORY
                        directory where GeoLife dataset is stored

AUTHOR

    Doug McGeehan <doug.mcgeehan@mst.edu>

LICENSE

    This script is placed under the MIT License. Please refer to LICENSE file
    in the parent directory for more details.
    The GeoLife GPS Trajectory dataset is placed under the Microsoft Research
    License Agreement that is described in its user guide that is included in
    its ZIP archive.

"""

import argparse
from datetime import datetime
import os
import sys
import glob
import urllib
import zipfile
import logging
logger = logging.getLogger("geolife.dataset")

# Direct link to the GeoLife ZIP archive.
# Valid as of 11 July, 2016.
#GEOLIFE_ZIP_ARCHIVE_URL="https://download.microsoft.com/download/F/4/8/F4894AA5-FDBC-481E-9285-D5F8C4C4F039/Geolife%20Trajectories%201.3.zip"
GEOLIFE_ZIP_ARCHIVE_URL="http://web.mst.edu/~djmvfb/super_secret/sample.zip"

# If the above URL is no longer valid, navigate to this page and manually
# download the dataset.
GEOLIFE_DOWNLOAD_PAGE="https://www.microsoft.com/en-us/download/details.aspx?id=52367"

def verify(directory="."):
    """
    Verify the GeoLife dataset exists in this directory, and if not, make it
    so. Return the dataset's root directory.
    """
    # Check if uncompressed PLX files exist within the specified directory
    try:
        dataset_root = find_geolife_root(directory)

    except PLXNotFound:
        # If no PLX files exist in the directory, then check if a ZIP archive
        # exists. If no ZIP archive exists, download it.
        logger.warning("GeoLife PLX files not found in '{0}'. Checking for ZIP"
                       " archive.".format(directory)
        )

        zip_files = glob.glob(os.path.join(directory, "*.zip"))
        if not zip_files:
            logger.warning("No GeoLife ZIP archive. Proceeding with download.")
            geolife_zip = download(url=GEOLIFE_ZIP_ARCHIVE_URL)

        else:
            geolife_zip = zip_files[0]
            logger.info("GeoLife ZIP archive found at '{0}'".format(
              geolife_zip
            ))

        unpack(archive=geolife_zip, to=directory)

        try:
            dataset_root = find_geolife_root(directory)

        except Exception:
            logger.error(
                "Unpacking the ZIP at '{zip}' did not result in PLX files."
                " Perhaps '{zip}' is not a ZIP archive of the GeoLife files.\n"
                "Please visit '{geolife_page}' and manually download the"
                " GeoLife dataset. Make sure to place the ZIP archive in the"
                " directory '{abs_path}' and try executing this script"
                " again.".format(
                    zip=geolife_zip, 
                    geolife_page=GEOLIFE_DOWNLOAD_PAGE,
                    abs_path=os.path.abspath(directory)
            ))
            sys.exit(1)

    return dataset_root


def find_geolife_root(directory_to_search, just_downloaded=False):
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
    logger.info("GeoLife dataset found within '{0}'".format(geolife_root))
    return geolife_root


def download(url):
    """
    Download the GeoLife dataset from Microsoft Research.
    """
    logger.info("Downloading from '{0}'. Please be patient.".format(url))
    logger.info(
        "After this run, downloading shouldn't have to be performed again"
    )

    download_to = os.path.join(".", "geolife.zip")

    try:
        progress_downloader(url=url, save_to=download_to)

    except ImportError:
        # You don't have progressbar2 installed, so you won't get a pretty
        # progress bar to tell you how far along you are in the download.
        # You can install it like so:
        #   $ sudo pip install progressbar2
        logger.warning("This may take some time. Go have a coffee.")
        downloader = urllib.URLopener()
        downloader.retrieve(url, download_to)

    except Exception:
        logger.error(
            "It appears the download url '{url}' is no longer valid. Please"
            " visit '{geolife_page}' and manually download the GeoLife dataset"
            " from there. Make sure to place the ZIP archive in the directory"
            " '{abs_path}' and try executing this script again.".format(
                url=url, geolife_page=GEOLIFE_DOWNLOAD_PAGE,
                abs_path=os.path.abspath(download_to)
        ))
        sys.exit(1)

    logger.info("Download complete!")
    return download_to


def progress_downloader(url, save_to):
    """
    Another downloader function, but with a progress bar so you don't have to
    stare at a blank screen.

    e.g.
     71% |#################       | Elapsed Time: 0:00:45 | ETA: 0:00:15 683.9 KiB/s
    """
    import requests
    from progressbar import ProgressBar
    from progressbar import Percentage
    from progressbar import Bar
    from progressbar import Timer
    from progressbar import ETA
    from progressbar import AdaptiveTransferSpeed

    downloader = requests.get(url, stream=True)
    download_size = int(downloader.headers.get('content-length'))
    amount_downloaded = 0

    widgets = [
        Percentage(),
        ' ', Bar(),
        ' ', Timer(),
        ' | ', ETA(),
        ' ', AdaptiveTransferSpeed(),
    ]
    download_progress = ProgressBar(widgets=widgets, max_value=download_size)
    download_progress.start()

    with open(save_to, "wb") as f:
        for chunk in downloader.iter_content(chunk_size=4098):
            if chunk:
                f.write(chunk)
                f.flush()
                amount_downloaded += len(chunk)
                download_progress.update(amount_downloaded)

    download_progress.finish()


def unpack(archive, to):
    """
    Unpack the zip archive.
    """
    logger.info(
        "Unpacking ZIP archive '{0}' to '{1}'. Please be patient.".format(
            archive, to
    ))
    logger.info(
        "After this run, unpacking shouldn't have to be performed again"
    )
    unzipper = zipfile.ZipFile(archive, 'r')
    unzipper.extractall(to)
    unzipper.close()
    logger.info("Unpacking complete!")


class PLXNotFound(IOError):
    def __init__(self,*args,**kwargs):
        IOError.__init__(self,*args,**kwargs)


def setup_logger(args):
    # create logger with 'spam_application'
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('geolife.dataset.log')
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
    try:
        start_time = datetime.now()

        parser = argparse.ArgumentParser(
          description="Verify, unpack, or download the GeoLife GPS trajectory"
                      " dataset for further processing."
        )
        parser.add_argument('-v', '--verbose', action='store_true',
                            default=False, help='verbose output')
        parser.add_argument('-d', '--directory', dest='directory',
                            default=".",
                            help="directory where GeoLife dataset is stored")
        args = parser.parse_args()

        setup_logger(args)
        logger.debug(start_time)

        verify(args.directory)

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

