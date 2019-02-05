import unittest
from merra.grid import create_merra_cell_grid


class Test(unittest.TestCase):
    """
    Testing base class
    """

    def test_MERRACellgrid(self):
        """
        Test if the grid remains homogenous.
        :return:
        """
        grid = create_merra_cell_grid()
        assert grid.activegpis.size == 207936
        assert grid.activegpis[159290] == 159290
        assert grid.activearrcell[159290] == 1431
        assert grid.activearrlat[159290] == 48.0
        assert grid.activearrlon[159290] == 16.25


if __name__ == "__main__":
    unittest.main()