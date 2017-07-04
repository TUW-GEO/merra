#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Created on 02-02-2017 

@author: fzaussin
@email: felix.zaussinger@geo.tuwien.ac.at
"""

import numpy as np
from pygeogrids.grids import BasicGrid


def MERRACellgrid():
    """
    Class implementing the GMAO 0.5 x 0.625 grid
        - southernmost lat : -90°
        - northernmost lat : 90°
        - westernmost lat : -180°
        - easternmost lat : 179.375°

    :return: BasicGrid instance
    """
    # asymmetrical grid
    lon_res = 0.625
    lat_res = 0.5

    # create 361 x 576 meshgrid
    lon, lat = np.meshgrid(
        np.arange(-180, 180 , lon_res),
        np.arange(-90, 90 + lat_res / 2, lat_res)
    )

    return BasicGrid(lon.flatten(), lat.flatten()).to_cell_grid(cellsize=5.)


if __name__ == "__main__":

    # TEST
    gpis, lons, lats, cells = MERRACellgrid().get_grid_points()
    print gpis
    print lons, lats

    cells = MERRACellgrid().get_cells()
    print cells

