Within this directory, the user should unpack the ZIP archive that contains the
GeoLife GPS Trajectory dataset. As a default execution parameter, the
``dataset.py`` script expects the dataset to reside in the ``data/`` directory.

If the dataset is not unpacked in this directory, but its ZIP archive is
present, then the ZIP archive will automatically be unpacked.

If the dataset is not unpacked in this directory and its ZIP archive is not
present, then the script will automatically download the ZIP archive from the
following URL:

https://www.microsoft.com/en-us/download/details.aspx?id=52367

Downloading will take some time as the GeoLife ZIP archive is about 300 MB.
If an error occurs, you'll likely have to download it manually and place the
downloaded ZIP archive in the ``data/`` directory.
