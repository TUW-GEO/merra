#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Created on 03-02-2017 

@author: fzaussin
@email: felix.zaussinger@geo.tuwien.ac.at

Process handler for reshuffle routine
Writing all available parameters for 1980-2016 to ts
"""

import os

from datetime import datetime

from interface import MERRA_Img
from reshuffle import reshuffle

# change as necessary
usr_path = '/home/fzaussin/shares/'

# data path definitions
in_path = os.path.join(usr_path, 'exchange/students/fzaussin/BACKUP/D/MERRA/MERRA2_MONTHLY/M2TMNXLND.5.12.4')
out_path = os.path.join(usr_path, 'exchange/students/fzaussin/BACKUP/D/MERRA/MERRA2_MONTHLY/Timeseries_SM_TEST2_04072017')

# define date range as datetime (!) objects
start_date = datetime(2014,1,31)
end_date = datetime(2014,12,31)

# specific soil moisture params
param_list = ['GWETPROF', 'GWETROOT', 'GWETTOP']


if __name__ == '__main__':

    # start process
    reshuffle(in_path=in_path,
              out_path=out_path,
              start_date=start_date,
              end_date=end_date,
              parameters=param_list,
              img_buffer=50)
