#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Created on 03-02-2017 

@author: fzaussin
@email: felix.zaussinger@geo.tuwien.ac.at

Process handler for reshuffle routine
"""

from datetime import datetime
from merra.reshuffle import reshuffle

# data path definitions

in_path = '/home/fzaussin/shares/radar/Datapool_raw/Earth2Observe/MERRA2/datasets/M2T1NXLND.5.12.4'
out_path = '/home/fzaussin/shares/radar/Datapool_processed/Earth2Observe/MERRA2/datasets/M2T1NXLND.5.12.4_6h_temporal_sampling_test'

# define date range as datetime (!) objects
start_date = datetime(1980, 1, 1)
end_date = datetime(1980, 1, 31)

# specific soil moisture params
param_list = ['TSOIL1', 'TSOIL2', 'TSOIL3', 'TSOIL4', 'TSOIL5', 'TSOIL6', 'TSURF',
              'SFMC', 'RZMC',
              'GWETPROF', 'GWETROOT', 'GWETTOP',
              'SNOMAS', 'PRECSNOLAND', 'PRECTOTLAND']

#param_list = ['SFMC']

if __name__ == '__main__':
    import time, datetime
    tic = time.clock()
    # start process
    reshuffle(in_path=in_path,
              out_path=out_path,
              start_date=start_date,
              end_date=end_date,
              parameters=param_list,
              img_buffer=240,
              # specify time resolution
              temporal_sampling=6)

    toc = time.clock()
    print("Elapsed time: ", str(datetime.timedelta(seconds=toc - tic)))
