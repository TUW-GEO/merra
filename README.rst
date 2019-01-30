=====
merra
=====

.. image:: https://travis-ci.org/TUW-GEO/merra.svg?branch=master
    :target: https://travis-ci.org/TUW-GEO/merra

.. image:: https://readthedocs.org/projects/merra2/badge/?version=latest
   :target: https://merra2.readthedocs.io/en/latest/?badge=latest

The package provides readers and converters for the MERRA2 data in a similar
manner as the gldas package.

Description
===========

Functionalities for downloading, reading and writing MERRA-2 reanalysis data.
Specifically, the modules provide an interface to the M2T1NXLND data set,
which provides Land Surface Diagnostics at 0.5 ° x 0.625 ° spatial - and
1-hourly temporal resolution.

The structure of the package is as follows:

* grid.py : implements the asymmetrical GMAO 0.5 x 0.625 grid
* interface.py : classes for reading a single image, image stacks and time series
* reshuffle.py : provides a command line utility for reshuffling a stack of 1-hourly sampled native images to time series format with an arbitraty temporal sampling between 1-hour and daily
* download.py : command line utility for downloading MERRA-2 data from the NASA GES DISC datapool
* reshuffling_process.py : python interface to the reshuffling command line script