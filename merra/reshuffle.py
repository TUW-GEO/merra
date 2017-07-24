# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2016, TU Wien
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Created on 02-02-2017

@author: fzaussin
@email: felix.zaussinger@geo.tuwien.ac.at

Module for a command line interface to convert the MERRA2 data into a
time series format using the repurpose package.

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
from interface import MERRA2_Ds_monthly, MERRA2_Ds_hourly
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
              temp_res='hourly',
              img_buffer=50):
    """
    Reshuffle method applied to MERRA2 data.

    Parameters
    ----------
    in_path: string
        input path where merra2 data was downloaded
    out_path : string
        Output path.
    start_date : datetime
        Start date.
    end_date : datetime
        End date.
    parameters: list
        parameters to read and convert
    temp_res : string
        if 'hourly', MERRA2_Ds_hourly will be used
        if 'monthly', MERRA2_Ds_monthly will be used
        notice: diurnal data not supported yet
    img_buffer: int, optional
        How many images to read at once before writing the time series.
    """

    # define input dataset
    if temp_res == 'hourly':
        input_dataset = MERRA2_Ds_hourly(in_path,
                                          parameters,
                                          array_1D=True)
        product = 'MERRA2_hourly'
    elif temp_res == 'monthly':
        input_dataset = MERRA2_Ds_monthly(in_path,
                                         parameters,
                                         array_1D=True)
        product = 'MERRA2_monthly'
    else:
        raise NotImplementedError()
        pass

    # create out_path directory if it does not exist yet
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    # set global attribute
    global_attributes = {'product': product}

    # get ts attributes from fist day of data
    data = input_dataset.read(start_date)
    ts_attributes = data.metadata
    # define grid
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
                        zlib=True,
                        unlim_chunksize=1000,
                        ts_attributes=ts_attributes)
    reshuffler.calc()


def parse_args(args):
    """
    Parse command line parameters for conversion from image to timeseries

    Parameters
    ----------
    args : list of strings
        command line parameters as list of strings

    Returns
    -------
    args : object
        command line parameters as :obj:`argparse.Namespace`
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
