=====
merra
=====

.. image:: https://travis-ci.org/TUW-GEO/merra.svg?branch=master
    :target: https://travis-ci.org/TUW-GEO/merra

.. image:: https://coveralls.io/repos/github/TUW-GEO/merra/badge.svg?branch=master
   :target: https://coveralls.io/github/TUW-GEO/merra?branch=master

.. image:: https://readthedocs.org/projects/merra2/badge/?version=latest
   :target: https://merra2.readthedocs.io/en/latest/?badge=latest

The package provides readers and converters for the MERRA2 data in a similiar
manner like the gldas package.

Description
===========

So far the 1-hourly and monthly data sets are supported. The structure of the
package is as follows:

* grid.py : implements the asymmetrical GMAO 0.5 x 0.625 grid
* interface.py : classes for reading a single image, image stacks and time series
* reshuffle.py : provides a command line utility for reshuffling an image stack to time series format
* download.py : command line utility for downloading merra2 data from the nasa datapool
* reshuffling_process.py : WILL BE REMOVED

Note
====

This project has been set up using PyScaffold 2.5.7. For details and usage
information on PyScaffold see http://pyscaffold.readthedocs.org/.
