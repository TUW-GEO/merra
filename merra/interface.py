#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Created on 02-02-2017 

@author: fzaussin
@email: felix.zaussinger@geo.tuwien.ac.at
"""

import os
from datetime import timedelta, date, datetime
import monthdelta

import numpy as np
import pandas as pd
from netCDF4 import Dataset

import pygeogrids
from pygeobase.io_base import ImageBase, MultiTemporalImageBase
from pygeobase.object_base import Image
from pygeogrids.netcdf import load_grid
from pynetcf.time_series import GriddedNcOrthoMultiTs

from grid import MERRACellgrid

class MERRA_Img(ImageBase):
    """
    Class for reading one MERRA 2 nc file in native resolution.

    Parameters
    ----------

    """
    def __init__(self, filename, mode='r', parameter='GWETPROF', array_1D=False):
        """

        :param filename:
        :param mode:
        :param parameter:
        :param array_1D:
        """

        super(MERRA_Img, self).__init__(filename, mode=mode)


        if type(parameter) != list:
            parameter = [parameter]
        self.parameters = parameter
        self.fill_values = np.repeat(1e15, 361 * 576)
        self.grid = MERRACellgrid()
        self.array_1D = array_1D
        self.filename = filename


    def open_file(self):

        """

        :return: netCDF4.Dataset object
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
        :return: list of available parameters
        """
        # read file
        # TODO: error handling, implement variable groups
        dataset = self.open_file()

        # check for number of vars and create df as placeholder
        param_count = len(dataset.variables.items())
        params = pd.DataFrame(index=range(param_count), columns=['var_name', 'long_name', 'units'])

        # iterate over var list and add info row-wise to df
        for v in range(param_count):
            var_name = dataset.variables.items()[v][0]
            long_name = dataset.variables.get(var_name).long_name
            units = dataset.variables.get(var_name).units
            # save to df
            params.iloc[v] = [var_name, long_name, units]

        if not var_list:
            # return extensive description as df
            print("\nAvailable Parameters:\n{1}\n{0}\n{1}").format(params, '_' * 80)
            return params
        else:
            # return list of params
            # skip lon,lat,time
            lnd_vars = params['var_name'][3:]
            return list(lnd_vars)


    def read(self, timestamp=None):
        """

        :param timestamp:
        :return:
        """
        print "{1}\nReading file: {0}".format(self.filename,
                                             '_' * 80)

        # return selected parameters and metadata for an image
        return_img = {}
        return_metadata = {}

        # horizontal soil layers
        layers = {'dzgt' : 1}

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
                        param_metadata.update({attr_name: getattr(variable, attr_name)})

                # initialize parameter data as masked array, set fill value to 1e+15
                param_data = dataset.variables[parameter][:]

                # GWETTOP is returned as nd-array in place of an masked array
                # type handling

                if not isinstance(param_data, np.ma.masked_array):
                    print("Parameter {} is of type {}. Should be {}.").format(parameter,
                                                                              type(param_data),
                                                                              np.ma.masked_array)
                    # flatten nd-array
                    param_data = param_data.flatten()
                else:
                    # TODO: check why there are only fill vals in data
                    # override fill value of masked array
                    # np.ma.set_fill_value(param_data, 1e+15)

                    # masked array to 1d nd-array
                    param_data = np.ma.getdata(param_data).flatten()

                # update data and metadata dicts depending on declared parameters
                return_img.update({parameter : param_data[self.grid.activegpis]})
                return_metadata.update({parameter : param_metadata})

                # Check for corrupt files
                try:
                    return_img[parameter]
                except KeyError:
                    path, file_name = os.path.split(self.filename)
                    print '%s in %s is corrupt - filling image with NaN values' % (parameter, file_name)
                    return_img[parameter] = np.empty(self.grid.n_gpi).fill(np.nan)
                    return_metadata['corrupt_parameters'].append()

        # 1D case
        # TODO: what is 1d case?
        if self.array_1D:
            return Image(self.grid.activearrlon,
                         self.grid.activearrlat,
                         return_img,
                         return_metadata,
                         timestamp)
        else:
            # iterate trough return_img dict and reshape nd-array to 361 x 576 matrix
            for key in return_img:
                return_img[key] = np.flipud(return_img[key].reshape((361, 576)))

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


class MERRA2_Ds(MultiTemporalImageBase):
    """
    Monthly data
    read/write a sequence of multi temporal images under a given path
    """
    def __init__(self, data_path, parameter='GWETPROF', array_1D=False):
        """

        :param data_path:
        :param parameters:
        """

        # TODO: whaaaaat is this?
        ioclass_kws = {'parameter' : parameter,
                       'array_1D' : array_1D}

        # define sub paths of root folder
        sub_path = ['%Y']

        # define fn template
        fn_template = "MERRA2_*.tavgM_2d_lnd_Nx.{datetime}.nc4"

        super(MERRA2_Ds, self).__init__(path=data_path,
                                        ioclass=MERRA_Img,
                                        fname_templ=fn_template,
                                        # monthly data
                                        datetime_format="%Y%m",
                                        subpath_templ=sub_path,
                                        exact_templ=False,
                                        ioclass_kws=ioclass_kws)

    def tstamps_for_daterange(self, start_date, end_date):
        """
        return timestamps for given date range

        Parameters
        ----------
        start_date: datetime
            start of date range
        end_date: datetime
            end of date range

        Returns
        -------
        timestamps : list
            list of datetime objects of each available image between
            start_date and end_date
        """

        # initialize timestamp array, calculate nr of months between start and end date
        timestamps = []
        diff = monthdelta.monthmod(start_date, end_date)[0] + monthdelta.monthdelta(1)

        for m in range(diff.months):
            # populate array month by month
            monthly_date = start_date + monthdelta.monthdelta(m)
            timestamps.append(monthly_date)

        return timestamps

class MERRA2_Ds_1h(MultiTemporalImageBase):
    """
    1 hourly data
    read/write a sequence of multi temporal images under a given path
    """
    def __init__(self, data_path, parameter='GWETPROF', array_1D=False):
        """

        :param data_path:
        :param parameters:
        """

        # TODO: whaaaaat is this?
        ioclass_kws = {'parameter': parameter,
                       'array_1D': array_1D}

        # define sub paths of root folder
        sub_path = ['%Y','%m']

        # define fn template for 1h data
        fn_template = "MERRA2_*.tavg1_2d_lnd_Nx.{datetime}.nc4"

        super(MERRA2_Ds_1h, self).__init__(path=data_path,
                                        ioclass=MERRA_Img,
                                        fname_templ=fn_template,
                                        # monthly data
                                        datetime_format="%Y%m%d",
                                        subpath_templ=sub_path,
                                        exact_templ=False,
                                        ioclass_kws=ioclass_kws)

    def tstamps_for_daterange(self, start_date, end_date):
        """
        return timestamps for given date range

        Parameters
        ----------
        start_date: datetime
            start of date range
        end_date: datetime
            end of date range

        Returns
        -------
        timestamps : list
            list of datetime objects of each available image between
            start_date and end_date
        """
        img_offsets = np.array([timedelta(hours=i, minutes=30) for i in range(24)])

        timestamps = []
        diff = end_date - start_date
        for i in range(diff.days + 1):
            daily_dates = start_date + timedelta(days=i) + img_offsets
            timestamps.extend(daily_dates.tolist())

        return timestamps


class MERRA2_Ts(GriddedNcOrthoMultiTs):
    """
    Reads merra ts data
    """

    def __init__(self, ts_path, grid_path=None):
        """

        :param ts_path:
        :param grid_path:
        """

        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        grid = pygeogrids.netcdf.load_grid(grid_path)
        super(MERRA2_Ts, self).__init__(ts_path, grid)


if __name__ == '__main__':
    # test 1h data read
    import matplotlib.pyplot as plt
    import datetime


    # plot hourly ts data
    ts_path = '/home/fzaussin/Desktop/merra-1h-reshuffling-test'

    # read ts at gp
    gpi = 100000
    ts = MERRA2_Ts(ts_path).read(gpi)
    print ts, type(ts)
    ts_daily = ts.resample('D').sum()

    # lon and lat of gp
    lon, lat = MERRACellgrid().gpi2lonlat(gpi)
    print lon, lat

    ts.plot(title='1h')
    ts_daily.plot(title='1d')
    plt.show()

    """
    # TEST
    import matplotlib.pyplot as plt

    # path to ts data
    usr_path = '/home/fzaussin/'
    ts_path = os.path.join(usr_path, 'shares/exchange/students/fzaussin/BACKUP/D/MERRA/MERRA2_MONTHLY/Timeseries_SM')

    # read ts at gp
    gpi = 100000
    ts = MERRA2_Ts(ts_path).read(gpi)
    print ts, type(ts)

    # lon and lat of gp
    lon, lat = MERRACellgrid().gpi2lonlat(gpi)
    print lon, lat

    # create plot
    fig, ax = plt.subplots()
    ts.plot(ax=ax)
    plt.show()
    """

