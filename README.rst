=====
merra
=====

.. image:: https://travis-ci.org/TUW-GEO/merra.svg?branch=master
    :target: https://travis-ci.org/TUW-GEO/merra

.. image:: https://readthedocs.org/projects/merra2/badge/?version=latest
   :target: https://merra2.readthedocs.io/en/latest/?badge=latest

.. image:: https://coveralls.io/repos/github/TUW-GEO/merra/badge.svg?branch=master
    :target: https://coveralls.io/github/TUW-GEO/merra?branch=master

The package provides readers and converters for the Land Surface Diagnostics
within the Modern-Era Retrospective analysis for Research and Applications
version 2 (MERRA-2). MERRA-2 is a NASA atmospheric reanalysis integrating
satellite data assimilation and aims at historical climate analyses.
MERRA-2 covers Land Surface Diagnostics for the period 1980-present
at 0.5 ° x 0.625 ° spatial- and 1-hourly temporal-resolution.

The structure of the package is as follows:

* grid.py : implements the asymmetrical GMAO 0.5 x 0.625 grid
* interface.py : classes for reading a single image, image stacks and time series
* reshuffle.py : provides a command line utility for reshuffling a stack of 1-hourly sampled native images to time series format with an arbitraty temporal sampling between 1-hour and daily
* download.py : command line utility for downloading MERRA-2 data from the NASA GES DISC datapool

Installation
============

For developers, it is recommended to first clone the repository and then
use the provided environment.yml file to install all needed conda and pip
dependencies:

.. code-block:: shell

  git clone https://github.com/TUW-GEO/merra.git --recursive
  cd merra
  conda create -n merra python=3.7 # or any supported python version
  source activate merra
  conda update -f environment.yml
  python setup.py develop


Supported Products
==================

- `M2T1NXLND: MERRA-2 tavg1_2d_lnd_Nx <https://disc.gsfc.nasa.gov/datasets/M2T1NXLND_V5.12.4/summary?keywords=%22MERRA-2%22%20AND%20%22M2T1NXLND%22&start=1920-01-01&end=2017-01-05>`_: MERRA-2 2d, 1-Hourly, Time-Averaged, Single-Level, Assimilation, Land Surface Diagnostics V5.12.4


Contribute
==========

We are happy if you want to contribute. Please raise an issue explaining what
is missing or if you find a bug. We will also gladly accept pull requests
against our master branch for new features or bug fixes.


Guidelines
----------

If you want to contribute please follow these steps:

- Fork the merra repository to your account
- make a new feature branch from the merra master branch
- Add your feature
- please include tests for your contributions in one of the test directories
  We use py.test so a simple function called test_my_feature is enough
- submit a pull request to our master branch