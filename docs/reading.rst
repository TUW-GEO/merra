Reading MERRA-2 images
----------------------

Reading of the MERRA-2 netcdf files can be done in two ways:

1) Reading by file name
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import os
    from datetime import datetime
    from merra.interface import MerraImage

    # parameters to read
    param_list = ['SFMC', 'RZMC', 'PRECTOTLAND', 'TSOIL1']

    # timestamp (needed because there are 24 hourly simulations within
    # each file (3D-stack), so you need to choose one to return a 2D image)
    timestamp = datetime(2018, 10, 1, 0, 30)

    # the class is initialized with the exact filename.
    img = MerraImage(os.path.join(os.path.dirname(__file__),
                                 'merra-test-data',
                                 'M2T1NXLND.5.12.4',
                                 '2018',
                                 '10',
                                 'MERRA2_400.tavg1_2d_lnd_Nx.20181001.nc4'),
                              parameter=param_list)

    # reading returns an image object which contains a data dictionary
    # with one array per parameter. The returned data is a global image/array
    # with shape (361, 576)
    image = img.read(timestamp=timestamp)
    data = image.data

2) Reading by date
~~~~~~~~~~~~~~~~~~

All the MERRA-2 data in a directory structure can be accessed by date.
The filename is automatically built from the given date.

.. code-block:: python

    from merra.interface import MerraImageStack

    # parameters to read
    param_list = ['SFMC', 'RZMC', 'PRECTOTLAND', 'TSOIL1']

    # initializes an image stack class given the path to the data directory
    # the class knows about the default folder structure down the line
    img_stack = MerraImageStack(data_path=os.path.join(os.path.dirname(__file__),
                                                 'merra-test-data',
                                                 'M2T1NXLND.5.12.4'),
                              parameter=param_list)

    # timestamp
    timestamp = datetime(2018, 10, 1, 0, 30)

    # read one image out of the stack at specific timestamp
    image = img_stack.read(timestamp=timestamp)

For reading all image between two dates the
:py:meth:`merra.interface.MerraImageStack.iter_images` iterator can be
used.