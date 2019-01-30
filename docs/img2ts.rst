Conversion to time series format
================================

For a lot of applications it is favorable to convert the image based format into
a format which is optimized for fast time series retrieval. This is what we
often need for e.g. validation studies. This can be done by stacking the images
into a netCDF file and choosing the correct chunk sizes or a lot of other
methods. We have chosen to do it in the following way:

- Store only the reduced gaußian grid points since that saves space.
- Further reduction the amount of stored data by saving only land points if selected.
- Store the time series in netCDF4 in the Climate and Forecast convention
  `Orthogonal multidimensional array representation
  <http://cfconventions.org/cf-conventions/v1.6.0/cf-conventions.html#_orthogonal_multidimensional_array_representation>`_
- Store the time series in 5x5 degree cells. This means there will be 2566 cell
  files (without reduction to land points) and a file called ``grid.nc``
  which contains the information about which grid point is stored in which file.
  This allows us to read a whole 5x5 degree area into memory and iterate over the time series quickly.


This conversion can be performed using the ``merra_repurpose`` command line
program. An example would be:

.. code-block:: shell

   merra_repurpose /merra2_data /timeseries/data 2000-01-01 2018-11-30 SFMC RZMC

Which would take MERRA-2 data stored in ``/merra2_data`` from January 1st 2000
to November 30th 2018 and store the parameters for surface (SFMC) and root
zone soil moisture (RZMC) as time series in the folder ``/timeseries/data``.

Conversion to time series is performed by the `repurpose package
<https://github.com/TUW-GEO/repurpose>`_ in the background. For custom settings
or other options see the `repurpose documentation
<http://repurpose.readthedocs.io/en/latest/>`_ and the code in
``merra.reshuffle``.

**Note**: If a ``RuntimeError: NetCDF: Bad chunk sizes.`` appears during reshuffling, consider downgrading the
netcdf4 library via:

.. code-block:: shell

  conda install -c conda-forge netcdf4=1.2.2

if you are on Python 2.* and

.. code-block:: shell

  conda install -c conda-forge netcdf4=1.2.8

if you are using Python 3.*.

Reading converted time series data
----------------------------------

For reading the data the ``merra_repurpose`` command produces the class
``MERRA2_Ts``:

.. code-block:: python

    from merra.interface import MERRA2_Ts

    # specify path to data folder
    path = '../timeseries/data'

    # specify location lon and lat
    lon, lat = (16.375, 48.125)

    # initialize the time series class
    merra_reader = MERRA2_Ts(ts_path=path,
                             ioclass_kws={'read_bulk':True},
                             parameters=['SFMC'])

    # read SFMC time series at the location
    ts = merra_reader.read(lon, lat)