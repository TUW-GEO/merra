import os
import glob
import tempfile
import numpy as np
import numpy.testing as npt
import unittest

from merra.reshuffle import main
from merra.interface import MerraTs


class Test(unittest.TestCase):
    """
    Testing base class
    """

    def test_reshuffle(self):
        """
        Create time series with 6-hourly sampling from one day of data.
        :return:
        """
        # specify resampling parameters
        inpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'merra-test-data', 'M2T1NXLND.5.12.4')
        startdate = '2018-10-01'
        enddate = '2018-10-01'
        parameters = ['SFMC']

        # create tempfile and run reshuffling
        ts_path = tempfile.mkdtemp()
        args = [inpath, ts_path, startdate, enddate] + parameters
        main(args)

        # read the resulting time series
        reader = MerraTs(ts_path,
                         ioclass_kws={'read_bulk': True},
                         parameters=['SFMC'])
        ts = reader.read(16.375, 48.125)

        # test assertion on soil moisture parameter
        ts_values_should = np.array([0.218083, 0.219587,
                                     0.214836, 0.220690],
                                    dtype=np.float32)
        npt.assert_allclose(ts['SFMC'].values, ts_values_should, rtol=1e-5)


if __name__ == "__main__":
    unittest.main()
