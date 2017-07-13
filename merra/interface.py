#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Copyright (c) 2014,Vienna University of Technology, Department of Geodesy and Geoinformation
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the Vienna University of Technology, Department of
#      Geodesy and Geoinformation nor the names of its contributors may be
#      used to endorse or promote products derived from this software without
#      specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL VIENNA UNIVERSITY OF TECHNOLOGY,
# DEPARTMENT OF GEODESY AND GEOINFORMATION BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Created on 02-02-2017

@author: fzaussin
@email: felix.zaussinger@geo.tuwien.ac.at
"""

import os
import monthdelta
from datetime import timedelta

import numpy as np
import pandas as pd
from netCDF4 import Dataset

import pygeogrids
from pygeobase.io_base import ImageBase, MultiTemporalImageBase
from pygeobase.object_base import Image
from pygeogrids.netcdf import load_grid
from pynetcf.time_series import GriddedNcOrthoMultiTs

from grid import MERRACellgrid
from rsroot import root_path

class MERRA_Img(ImageBase):
    """
    Class for reading one MERRA2 nc file in native resolution.

    Parameters
    ----------
    filename: string
        filename of the MERRA2 nc file
    mode: string, optional
        mode of opening the file, only 'r' is implemented at the moment
    parameter : string or list, optional
        one or list of parameters to read, see MERRA2 documentation for more information
        Default : 'GWETTOP'
    array_1D: boolean, optional
        if set then the data is read into 1D arrays. Needed for some legacy code.
    """

    def __init__(self, filename, mode='r', parameter='GWETTOP', array_1D=False):
        super(MERRA_Img, self).__init__(filename, mode=mode)

        if not isinstance(parameter, list):
            parameter = [parameter]
        self.parameters = parameter
        self.fill_values = np.repeat(1e15, 361 * 576)
        self.grid = MERRACellgrid()
        self.array_1D = array_1D
        self.filename = filename

    def open_file(self):
        """
        Try to open dataset.

        Returns
        -------
        dataset : netCDF4.Dataset object
        """
        try:
            dataset = Dataset(self.filename)

            if dataset.data_model == 'NETCDF4':
                print "Successfully opened file '{}'.\n".format(dataset.Filename)
                return dataset
        except IOError as e:
            print(e)
            print(" ".join([self.filename, "can not be opened."]))
            raise e

    def show_params(self, var_list=False):
        """
        Lists all parameter names and their units

        Returns
        -------
        params: pd.DataFrame
            list of available parameters
        """
        # read file
        # TODO: error handling, implement variable groups
        dataset = self.open_file()

        # check for number of vars and create df as placeholder
        param_count = len(dataset.variables.items())
        params = pd.DataFrame(
            index=range(param_count), columns=[
                'var_name', 'long_name', 'units'])

        # iterate over var list and add info row-wise to df
        for v in range(param_count):
            var_name = dataset.variables.items()[v][0]
            long_name = dataset.variables.get(var_name).long_name
            units = dataset.variables.get(var_name).units
            # save to df
            params.iloc[v] = [var_name, long_name, units]

        if not var_list:
            # return extensive description as df
            print("\nAvailable Parameters:\n{1}\n{0}\n{1}").format(
                params, '_' * 80)
            return params
        else:
            # return list of params
            # skip lon,lat,time
            lnd_vars = params['var_name'][3:]
            return list(lnd_vars)

    def read(self, timestamp=None):
        """
        Reads single image for given timestamp.

        Parameters
        ----------
        timestamp : datetime.datetime
            exact timestamp of the image

        Returns
        -------
        Image : object
            pygeobase.object_base.Image object
        """
        print "{1}\nReading file: {0}".format(self.filename,
                                              '_' * 80)

        # return selected parameters and metadata for an image
        return_img = {}
        return_metadata = {}

        # horizontal soil layers
        layers = {'dzgt': 1}

        # open dataset
        dataset = self.open_file()

        # build parameter list
        param_names = []
        for param in self.parameters:
            param_names.append(param)

        # Iterate over all parameters in nc file
        for parameter, variable in dataset.variables.items():

            # Only process selected parameters
            if parameter in param_names:
                param_metadata = {}

                # Iterate over all attributes of the selected parameters
                for attr_name in variable.ncattrs():
                    # Only extract metadata of the attributes in the list
                    if attr_name in ['long_name', 'units']:
                        param_metadata.update(
                            {attr_name: getattr(variable, attr_name)})

                # initialize parameter data as masked array, set fill value to
                # 1e+15
                param_data = dataset.variables[parameter][:]

                # GWETTOP is returned as nd-array in place of an masked array
                # type handling

                if not isinstance(param_data, np.ma.masked_array):
                    print("Parameter {} is of type {}. Should be {}.").format(
                        parameter, type(param_data), np.ma.masked_array)
                    # flatten nd-array
                    param_data = param_data.flatten()
                else:
                    # TODO: check why there are only fill vals in data
                    # override fill value of masked array
                    # np.ma.set_fill_value(param_data, 1e+15)

                    # masked array to 1d nd-array
                    param_data = np.ma.getdata(param_data).flatten()

                # update data and metadata dicts depending on declared
                # parameters
                return_img.update(
                    {parameter: param_data[self.grid.activegpis]})
                return_metadata.update({parameter: param_metadata})

                # Check for corrupt files
                try:
                    return_img[parameter]
                except KeyError:
                    path, file_name = os.path.split(self.filename)
                    print '%s in %s is corrupt - filling image with NaN values' % (parameter, file_name)
                    return_img[parameter] = np.empty(
                        self.grid.n_gpi).fill(np.nan)
                    return_metadata['corrupt_parameters'].append()

        if self.array_1D:
            return Image(self.grid.activearrlon,
                         self.grid.activearrlat,
                         return_img,
                         return_metadata,
                         timestamp)
        else:
            # iterate trough return_img dict and reshape nd-array to 361 x 576
            # matrix
            for key in return_img:
                return_img[key] = np.flipud(
                    return_img[key].reshape((361, 576)))

            # return Image object for called parameters
            return Image(np.flipud(self.grid.activearrlon.reshape((361, 576))),
                         np.flipud(self.grid.activearrlat.reshape((361, 576))),
                         return_img,
                         return_metadata,
                         timestamp)

    def write(self, image, **kwargs):
        """
        Write data to an image file.

        Parameters
        ----------
        image : object
            pygeobase.object_base.Image object
        """
        raise NotImplementedError()
        pass

    def flush(self):
        """
        Flush data.
        """
        pass

    def close(self):
        """
        Close file.
        """
        pass


class MERRA2_Ds_monthly(MultiTemporalImageBase):
    """
    Class for reading the monthly merra2 data. Read image stack between
    start date and end date under a given path.
    """

    def __init__(self, data_path, parameter='GWETTOP', array_1D=False):
        """
        Initialize MERRA2_Ds object with a given path.

        Parameters
        ----------
        data_path : string
            path to the nc files
        parameter : string or list, optional
            one or list of parameters to read, see MERRA2 documentation for more information
            Default : 'GWETTOP'
        array_1D: boolean, optional
            if set then the data is read into 1D arrays. Needed for some legacy code.
        """

        ioclass_kws = {'parameter': parameter,
                       'array_1D': array_1D}

        # define sub paths of root folder
        sub_path = ['%Y']

        # define fn template
        fn_template = "MERRA2_*.tavgM_2d_lnd_Nx.{datetime}.nc4"

        super(MERRA2_Ds_monthly, self).__init__(path=data_path,
                                                ioclass=MERRA_Img,
                                                fname_templ=fn_template,
                                                # monthly data
                                        datetime_format="%Y%m",
                                                subpath_templ=sub_path,
                                                exact_templ=False,
                                                ioclass_kws=ioclass_kws)

    def tstamps_for_daterange(self, start_date, end_date):
        """
        Return timestamps for a given date range.

        Parameters
        ----------
        start_date: datetime.datetime
            start of date range
        end_date: datetime.datetime
            end of date range

        Returns
        -------
        timestamps : list
            list of datetime objects of each available image between
            start_date and end_date
        """

        # initialize timestamp array, calculate nr of months between start and
        # end date
        timestamps = []
        diff = monthdelta.monthmod(start_date, end_date)[
            0] + monthdelta.monthdelta(1)

        for m in range(diff.months):
            # populate array month by month
            monthly_date = start_date + monthdelta.monthdelta(m)
            timestamps.append(monthly_date)

        return timestamps


class MERRA2_Ds_hourly(MultiTemporalImageBase):
    """
    Class for reading the hourly merra2 data. Read image stack between
    start date and end date under a given path.
    """

    def __init__(self, data_path, parameter='GWETTOP', array_1D=False):
        """
        Initialize MERRA2_Ds_1h object with a given path.

        Parameters
        ----------
        data_path : string
            path to the nc files
        parameter : string or list, optional
            one or list of parameters to read, see MERRA2 documentation for more information
            Default : 'GWETTOP'
        array_1D: boolean, optional
            if set then the data is read into 1D arrays. Needed for some legacy code.
        """

        ioclass_kws = {'parameter': parameter,
                       'array_1D': array_1D}

        # define sub paths of root folder
        sub_path = ['%Y', '%m']

        # define fn template for 1h data
        fn_template = "MERRA2_*.tavg1_2d_lnd_Nx.{datetime}.nc4"

        super(MERRA2_Ds_hourly, self).__init__(path=data_path,
                                               ioclass=MERRA_Img,
                                               fname_templ=fn_template,
                                               # monthly data
                                           datetime_format="%Y%m%d",
                                               subpath_templ=sub_path,
                                               exact_templ=False,
                                               ioclass_kws=ioclass_kws)

    def tstamps_for_daterange(self, start_date, end_date):
        """
        Return timestamps for a given date range.

        Parameters
        ----------
        start_date: datetime.datetime
            start of date range
        end_date: datetime.datetime
            end of date range

        Returns
        -------
        timestamps : list
            list of datetime objects of each available image between
            start_date and end_date
        """
        # 00:30, 01:30, 02:30,..., 23:30
        img_offsets = np.array([timedelta(hours=i, minutes=30)
                                for i in range(24)])

        timestamps = []
        diff = end_date - start_date
        for i in range(diff.days + 1):
            daily_dates = start_date + timedelta(days=i) + img_offsets
            timestamps.extend(daily_dates.tolist())

        return timestamps


class MERRA2_Ts(GriddedNcOrthoMultiTs):
    """
    Read reshuffled hourly or monthly merra2 ts data under a given path.
    """

    def __init__(self, ts_path=None, grid_path=None):
        """
        Initialize MERRA2_Ts object with path to data repository. Use to read
        time series data at a given location.

        Parameters
        ----------
        ts_path : string
            path to the nc files
        grid_path : string
            path to grid.nc file
        """
        if ts_path is None:
            # TODO: root_path.r does not point to correct dirs for my ubuntu
            # TODO: temporary hardcoded user name in rspath
            ts_path = os.path.join(root_path.r,
                                   'Datapool_processed',
                                   'Earth2Observe',
                                   'MERRA2',
                                   'M2T1NXLND.5.12.4',
                                   'datasets',
                                   'ts_hourly_means')

        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        grid = pygeogrids.netcdf.load_grid(grid_path)
        super(MERRA2_Ts, self).__init__(ts_path, grid)

def temp_read_ts(lon, lat):
    """
    Temporary reader which concatenates the two time series pieces:
    piece 1: 1980-01-01 00:30:00 : 1998-10-31 23:30:00
    piece 2: 1998-11-01 00:30:00 : 2017-05-31 23:30:00

    :param lon: longitude
    :param lat: latitude
    :return: merra2 ts from 1980-01-01 to 2017-05-31
    """
    # first piece
    ts1_object = MERRA2_Ts()
    ts1 = ts1_object.read(lon, lat)

    # second piece
    ts_path2 = os.path.join(root_path.r,
                           'Datapool_processed',
                           'Earth2Observe',
                           'MERRA2',
                           'M2T1NXLND.5.12.4',
                           'datasets',
                           'ts_hourly_means_part2')

    # TODO: local pfad mit ts_path2 ersetzen sobald daten rübergeschoben
    ts2_object = MERRA2_Ts(ts_path='/home/fzaussin/merra-ts-from-1998-11-01')
    ts2 = ts2_object.read(lon, lat)

    # cut ts1 above overlap timestamp to drop duplicate rows
    overlap = '1998-10-31 23:30:00'
    ts1 = ts1[:overlap]
    # return concatenated ts
    ts_both = pd.concat([ts1,ts2])
    return ts_both


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    # examples

    # find gpi for given lon and lat
    lon, lat = (-104, 49)
    gpi = MERRACellgrid().find_nearest_gpi(lon=lon, lat=lat)[0]
    print gpi

    # read ts of whole length
    ts = temp_read_ts(lon, lat)
    ts.plot(title='merra2 1-hourly')

    # resample to daily resolution
    ts_daily = ts.resample('D').mean()
    ts_daily.plot(title='merra2 daily')

    # show plots
    plt.show()
