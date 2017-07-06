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
import datetime

from interface import MERRA_Img
from reshuffle import reshuffle

# data path definitions
in_path = '/home/fzaussin/shares/radar/Datapool_raw/Earth2Observe/MERRA2/datasets/goldsmr4.gesdisc.eosdis.nasa.gov/data/MERRA2/M2T1NXLND.5.12.4'
out_path = '/home/fzaussin/Desktop/merra-1h-reshuffling-test-class'

# define date range as datetime (!) objects
start_date = datetime.datetime(1980,1,1)
end_date = datetime.datetime(1980,1,31)

# specific soil moisture params
param_list = ['GWETPROF', 'GWETROOT', 'GWETTOP']

if __name__ == '__main__':
    import time
    tic = time.clock()
    # start process
    reshuffle(in_path=in_path,
              out_path=out_path,
              start_date=start_date,
              end_date=end_date,
              parameters=param_list,
              temp_res='hourly',
              img_buffer=50)

    toc = time.clock()
    print "Elapsed time: ", str(datetime.timedelta(seconds=toc - tic))
