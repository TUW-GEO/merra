#!/usr/bin/env
# -*- coding: utf-8 -*-

"""
Created on 02-02-2017 

@author: fzaussin
@email: felix.zaussinger@geo.tuwien.ac.at

USAGE in terminal:

reshuffle.py [-h] [--imgbuffer IMGBUFFER]
                    dataset_root timeseries_root start end parameters
                    [parameters ...]
"""

import os
import sys
import argparse

from datetime import datetime

from repurpose.img2ts import Img2Ts
from interface import MERRA2_Ds_1h

from pygeogrids import BasicGrid

# define date/month string
def mkdate(datestring):
    if len(datestring) == 10:
        return datetime.strptime(datestring, '%Y-%m-%d')
    if len(datestring) == 16:
        return datetime.strptime(datestring, '%Y-%m-%dT%H:%M')


def reshuffle(in_path,
              out_path,
              start_date,
              end_date,
              parameters,
              img_buffer=50):
    """
    Reshuffle routine for MERRA2 data

    Parameters
    ----------
    :param in_path:
    :param out_path:
    :param start_date:
    :param end_date:
    :param parameters:
    :param img_buffer:

    Returns
    -------
    :return:
    """

    # define input dataset
    # TODO: MERRA2_Ds or MERRA_img ? -> needs to be ds !
    input_dataset = MERRA2_Ds_1h(in_path,
                              parameters,
                              array_1D=True) # TODO: understand why true

    # create out_path directory if it does not exist yet
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    # set global attribute
    global_attributes = {'product' : 'MERRA2'}

    # get ts attributes from fist day of data
    data = input_dataset.read(start_date)
    ts_attributes = data.metadata

    # define grid
    # TODO: why basicgrid call??
    #grid = MERRACellgrid()
    grid = BasicGrid(data.lon, data.lat)

    # define reshuffler
    reshuffler = Img2Ts(input_dataset=input_dataset,
                        outputpath=out_path,
                        startdate=start_date,
                        enddate=end_date,
                        input_grid=grid,
                        imgbuffer=img_buffer,
                        cellsize_lat=5.0,
                        cellsize_lon=6.25,
                        global_attr=global_attributes,
                        ts_attributes=ts_attributes)
    reshuffler.calc()


def parse_args(args):
    """
    Parse command line parameters for conversion from image to timeseries

    :param args: command line parameters as list of strings
    :return: command line parameters as :obj:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(
        description="Convert MERRA2 images to time series format.")
    parser.add_argument("dataset_root",
                        help='Root of local filesystem where the data is stored.')
    parser.add_argument("timeseries_root",
                        help='Root of local filesystem where the timeseries will be stored.')
    parser.add_argument("start", type=mkdate,
                        help=("Startdate. Either in format YYYY-MM-DD or YYYY-MM-DDTHH:MM."))
    parser.add_argument("end", type=mkdate,
                        help=("Enddate. Either in format YYYY-MM-DD or YYYY-MM-DDTHH:MM."))
    parser.add_argument("parameters", metavar="parameters",
                        nargs="+",
                        help=("Parameters to download in numerical format."))

    parser.add_argument("--imgbuffer", type=int, default=50,
                        help=("How many images to read at once. Bigger numbers make the "
                              "conversion faster but consume more memory."))

    args = parser.parse_args(args)
    # set defaults that can not be handled by argparse

    print("Converting data from {} to {} into folder {}.".format(args.start.isoformat(),
                                                                 args.end.isoformat(),
                                                                 args.timeseries_root))
    return args


def main(args):
    args = parse_args(args)

    reshuffle(args.dataset_root,
              args.timeseries_root,
              args.start,
              args.end,
              args.parameters,
              img_buffer=args.imgbuffer)


def run():
    main(sys.argv[1:])

if __name__ == '__main__':
    run()
