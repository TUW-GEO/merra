import os
import unittest
import numpy.testing as npt
from datetime import datetime
from merra.interface import MerraImage, MerraImageStack


class Test(unittest.TestCase):
    """
    Testing base class
    """

    def test_img_reading_1D(self):
        """
        Test if netCDF image file is correctly read in 1D.
        """
        # specify parameters
        parameters = ['SFMC', 'RZMC', 'GWETPROF',
                      'GWETROOT', 'GWETTOP', 'TSURF']

        # create image object based on test file
        img = MerraImage(
            os.path.join(
                os.path.dirname(__file__),
                'merra-test-data',
                'M2T1NXLND.5.12.4',
                '2018',
                '10',
                'MERRA2_400.tavg1_2d_lnd_Nx.20181001.nc4'),
            parameter=parameters,
            array_1d=True)

        # read image for specified timestamp
        image = img.read(timestamp=datetime(2018, 10, 1, 0, 30))

        # test assertions
        assert sorted(image.data.keys()) == sorted(parameters)
        assert image.lon.shape == (207936,)
        assert image.lon.shape == image.lat.shape
        npt.assert_almost_equal(image.data['SFMC'][159290], 0.218083,
                                decimal=6)
        npt.assert_almost_equal(image.data['RZMC'][159290], 0.218432,
                                decimal=6)
        npt.assert_almost_equal(image.data['GWETPROF'][159290], 0.496459,
                                decimal=6)
        npt.assert_almost_equal(image.data['GWETROOT'][159290], 0.498425,
                                decimal=6)
        npt.assert_almost_equal(image.data['GWETTOP'][159290], 0.497566,
                                decimal=6)
        npt.assert_almost_equal(image.data['TSURF'][159290], 277.240417,
                                decimal=6)

    def test_img_reading_2D(self):
        """
        Test if netCDF image file is correctly read in 2D.
        """
        # specify parameters
        parameters = ['SFMC', 'RZMC', 'GWETPROF',
                      'GWETROOT', 'GWETTOP', 'TSURF']

        # create image object based on test file
        img = MerraImage(
            os.path.join(
                os.path.dirname(__file__),
                'merra-test-data',
                'M2T1NXLND.5.12.4',
                '2018',
                '10',
                'MERRA2_400.tavg1_2d_lnd_Nx.20181001.nc4'),
            parameter=parameters,
            array_1d=False)

        # read image for specified timestamp
        image = img.read(timestamp=datetime(2018, 10, 1, 0, 30))

        # test assertions
        assert sorted(image.data.keys()) == sorted(parameters)
        assert image.lon.shape == (361, 576)
        assert image.lon.shape == image.lat.shape
        assert image.lon[0, 0] == -180.0
        assert image.lon[0, 575] == 179.375
        assert image.lat[0, 0] == 90.0
        assert image.lat[360, 0] == -90.0
        # 361-277=84 (panoply seems to count latitude differently, although
        # longitude is the same) we go from -90-90 and panoply from 0-180?
        npt.assert_almost_equal(image.data['SFMC'][84][314], 0.218083,
                                decimal=6)
        npt.assert_almost_equal(image.data['RZMC'][84][314], 0.218432,
                                decimal=6)
        npt.assert_almost_equal(image.data['GWETPROF'][84][314], 0.496459,
                                decimal=6)
        npt.assert_almost_equal(image.data['GWETROOT'][84][314], 0.498425,
                                decimal=6)
        npt.assert_almost_equal(image.data['GWETTOP'][84][314], 0.497566,
                                decimal=6)
        npt.assert_almost_equal(image.data['TSURF'][84][314], 277.240417,
                                decimal=6)

    def test_image_stack_reading(self):
        """
        Test if the image stack is read correctly.
        """
        # specify parameters
        parameters = ['SFMC', 'RZMC', 'GWETPROF',
                      'GWETROOT', 'GWETTOP', 'TSURF']

        # create image stack object based on test file directory
        img = MerraImageStack(os.path.join(os.path.dirname(__file__),
                                           'merra-test-data',
                                           'M2T1NXLND.5.12.4'),
                              parameter=parameters,
                              array_1d=True,
                              temporal_sampling=6)

        image = img.read(timestamp=datetime(2018, 10, 1))

        # test assertions
        assert sorted(image.data.keys()) == sorted(parameters)
        assert sorted(list(image.metadata.keys())) == sorted(parameters)
        assert image.lon.shape == (207936,)
        assert image.lon.shape == image.lat.shape
        npt.assert_almost_equal(image.data['SFMC'][159290], 0.218083,
                                decimal=6)
        npt.assert_almost_equal(image.data['RZMC'][159290], 0.218432,
                                decimal=6)
        npt.assert_almost_equal(image.data['GWETPROF'][159290], 0.496459,
                                decimal=6)
        npt.assert_almost_equal(image.data['GWETROOT'][159290], 0.498425,
                                decimal=6)
        npt.assert_almost_equal(image.data['GWETTOP'][159290], 0.497566,
                                decimal=6)
        npt.assert_almost_equal(image.data['TSURF'][159290], 277.240417,
                                decimal=6)
        assert image.metadata['SFMC']['units'] == u'm-3 m-3'
        assert image.metadata['SFMC']['long_name'] == u'water_surface_layer'

    def test_timestamps_for_daterange(self):
        """
        Test of timestamps are created correctly.
        """
        # specify parameters
        parameters = ['SFMC', 'RZMC', 'GWETPROF',
                      'GWETROOT', 'GWETTOP', 'TSURF']

        # create image stack object based on test file directory
        img = MerraImageStack(os.path.join(os.path.dirname(__file__),
                                           'merra-test-data',
                                           'M2T1NXLND.5.12.4'),
                              parameter=parameters,
                              array_1d=True,
                              temporal_sampling=6)

        # create timestamps for the default 6-hourly sampling
        tstamps = img.tstamps_for_daterange(start_date=datetime(2018, 10, 1),
                                            end_date=datetime(2018, 10, 1))
        # test assertions
        assert len(tstamps) == 4
        assert tstamps == [datetime(2018, 10, 1, 0, 30),
                           datetime(2018, 10, 1, 6, 30),
                           datetime(2018, 10, 1, 12, 30),
                           datetime(2018, 10, 1, 18, 30)]


if __name__ == "__main__":
    unittest.main()