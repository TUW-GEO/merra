import unittest
from merra.grid import MERRACellgrid

class Test(unittest.TestCase):
    """
    Testing base class
    """
    def test_MERRACellgrid(self):
        """
        Test if the grid remains homogenous.
        :return:
        """
        grid = MERRACellgrid()
        assert grid.activegpis.size == 207936
        assert grid.activegpis[153426] == 153426
        assert grid.activearrcell[153426] == 962
        assert grid.activearrlat[153426] == 43.0
        assert grid.activearrlon[153426] == -48.75
        return None

if __name__ == "__main__":
    unittest.main()