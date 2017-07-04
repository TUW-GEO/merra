#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Created on 13-02-2017 

@author: fzaussin
@email: felix.zaussinger@geo.tuwien.ac.at
"""

import os
import sys
import glob
import argparse
from functools import partial

import trollsift.parser as parser
from datetime import datetime
from datedown.interface import mkdate
from datedown.dates import n_hourly
from datedown.urlcreator import create_dt_url
from datedown.fname_creator import create_dt_fpath
from datedown.interface import download_by_dt
from datedown.down import download

class FolderStructure(object):
    """

    """
    def __init__(self, product, start_date, folder_root=None, fmt_string=None, sub_paths=None):
        """

        :param product:
        :param start_date:
        :param folder_root:
        :param fmt_string:
        :param sub_paths:
        """
        self.product = product
        self.start_date = start_date
        self.folder_root = folder_root
        self.fmt_string = fmt_string
        self.sub_paths = sub_paths

    def get_first_last_folder_(self):
        """

        :return:
        """
        pass

    def get_last_folder(self):
        """

        :return:
        """

        pass

    def get_last_formatted_dir_in_dir(self, folder):
        """

        :param folder:
        :return:
        """
        pass

    def get_first_formatted_dir_in_dir(self, folder):
        """

        :param folder:
        :return:
        """
        pass


class Downloader(FolderStructure):
    """

    """


    def __init__(self, product, start_date, args):
        """

        :param args:
        """

        # TODO: resolve issues ???
        super(Downloader, self).__init__(product, start_date)
        self.args = args
        self.product = product
        self.start_date = start_date


    def parse_args(self):
        """

        :return:
        """
        parser = argparse.ArgumentParser(
            description="Download {} data.".format(self.product))
        parser.add_argument("localroot",
                            help='Root of local filesystem where the data is stored.')
        parser.add_argument("-s", "--start", type=mkdate,
                            help=("Start-date. Either in format YYYY-MM-DD or YYYY-MM-DDTHH:MM."
                                  "If not given then the target folder is scanned for a start date."
                                  "If no data is found there then the first available date of the product is used."))
        parser.add_argument("-e", "--end", type=mkdate,
                            help=("End-date. Either in format YYYY-MM-DD or YYYY-MM-DDTHH:MM."
                                  "If not given then the current date is used."))
        parser.add_argument("--product", choices=[self.product], default=self.product,
                            help='Product to download.')
        parser.add_argument("--username",
                            help='Username to use for download.')
        parser.add_argument("--password",
                            help='password to use for download.')
        parser.add_argument("--n_proc", default=1, type=int,
                            help='Number of parallel processes to use for downloading.')
        args = parser.parse_args(self.args)

        # set defaults that can not be handled by argparse
        if args.start is None or args.end is None:
            first, last = self.get_first_last_folder_(self.args.localroot)
            if args.start is None:
                if last is None:
                    args.start = self.start_date
                else:
                    args.start = last
            if args.end is None:
                args.end = datetime.now()

        # TODO: generalize
        prod_urls = {self.product:
                     {'root': 'hydro1.sci.gsfc.nasa.gov',
                      'dirs': ['data','s4pa',
                               'GLDAS_V1','GLDAS_NOAH025SUBP_3H',
                               '%Y', '%j']}}

        args.urlroot = prod_urls[args.product]['root']
        args.urlsubdirs = prod_urls[args.product]['dirs']
        args.localsubdirs = ['%Y', '%j']

        print("Downloading data from {} to {} into folder {}.".format(args.start.isoformat(),
                                                                      args.end.isoformat(),
                                                                      args.localroot))
        return args

    def main(self, args):
        args = self.parse_args(args)

        dts = list(n_hourly(args.start, args.end, 3))
        url_create_fn = partial(create_dt_url, root=args.urlroot,
                                fname='', subdirs=args.urlsubdirs)
        fname_create_fn = partial(create_dt_fpath, root=args.localroot,
                                  fname='', subdirs=args.localsubdirs)
        down_func = partial(download,
                            num_proc=args.n_proc,
                            username=args.username,
                            password=args.password,
                            recursive=True)
        download_by_dt(dts, url_create_fn,
                       fname_create_fn, down_func,
                       recursive=True)


    def run(self):
        self.main(sys.argv[1:])

if __name__ == "__main__":
    Downloader.main()