# The MIT License (MIT)
#
# Copyright (c) 2019, TU Wien
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
The download module implements a command line script for downloading MERRA2
reanalysis data from the NASA GESDISC repository.
"""

import os
import sys
import glob
import argparse
from functools import partial

from trollsift import parser
from datetime import datetime
from datedown.interface import mkdate
from datedown.dates import daily
from datedown.urlcreator import create_dt_url
from datedown.fname_creator import create_dt_fpath
from datedown.interface import download_by_dt
from datedown.down import download


def folder_get_version_first_last(
        root,
        fmt="MERRA2_{stream}.tavg1_2d_lnd_Nx.{time:%Y%m%d}.nc4",
        subpaths=['{time:%Y}', '{time:%m}']):
    """
    Get product version and first and last product
    which exists under the root folder.

    Parameters
    ----------
    root: string
        Root folder on local filesystem
    fmt: string, optional
        formatting string
    subpaths: list, optional
        format of the subdirectories under root.
    Returns
    -------
    version: string
        Found product version
    start: datetime.datetime
        First found product datetime
    end: datetime.datetime
        Last found product datetime
    """
    start = None
    end = None
    version = None
    first_folder = get_first_folder(root, subpaths)
    print('First folder', first_folder)
    last_folder = get_last_folder(root, subpaths)
    print('Last folder', last_folder)

    if first_folder is not None:
        files = sorted(
            glob.glob(
                os.path.join(
                    first_folder,
                    parser.globify(fmt))))
        # parse files according to formatting string ({stream} is ignored)
        data = parser.parse(fmt, os.path.split(files[0])[1])
        start = data['time']
        version = 'M2T1NXLND.5.12.4'

    if last_folder is not None:
        files = sorted(
            glob.glob(
                os.path.join(
                    last_folder,
                    parser.globify(fmt))))
        data = parser.parse(fmt, os.path.split(files[-1])[1])
        end = data['time']

    return version, start, end


def get_last_folder(root, subpaths):
    """
    ...

    Parameters
    ----------
    root : string
        ...
    subpaths : list of strings
        ...

    Returns
    -------
    directory : list of strings
        ...

    """
    directory = root
    for level, subpath in enumerate(subpaths):
        last_dir = get_last_formatted_dir_in_dir(directory, subpath)
        if last_dir is None:
            directory = None
            break
        directory = os.path.join(directory, last_dir)
    return directory


def get_first_folder(root, subpaths):
    """
    ...

    Parameters
    ----------
    root : string
        ...
    subpaths : list of strings
        ...

    Returns
    -------
    directory : list of strings
        ...
    """
    directory = root
    for level, subpath in enumerate(subpaths):
        last_dir = get_first_formatted_dir_in_dir(directory, subpath)
        if last_dir is None:
            directory = None
            break
        directory = os.path.join(directory, last_dir)
    return directory


def get_last_formatted_dir_in_dir(folder, fmt):
    """
    Get the (alphabetically) last directory in a directory
    which can be formatted according to fmt.

    Parameters
    ----------
    folder : string
        path to folder
    fmt : ...
        formatting rule

    Returns
    -------
    last_elem: string
        path to last directory

    """
    last_elem = None
    root_elements = sorted(os.listdir(folder))
    for root_element in root_elements[::-1]:
        if os.path.isdir(os.path.join(folder, root_element)):
            if parser.validate(fmt, root_element):
                last_elem = root_element
                break
    return last_elem


def get_first_formatted_dir_in_dir(folder, fmt):
    """
    Get the (alphabetically) first directory in a directory
    which can be formatted according to fmt.

    Parameters
    ----------
    folder : string
        path to folder
    fmt : ...
        formatting rule

    Returns
    -------
    first_elem: string
        path to last directory
    """
    first_elem = None
    root_elements = sorted(os.listdir(folder))
    for root_element in root_elements:
        if os.path.isdir(os.path.join(folder, root_element)):
            if parser.validate(fmt, root_element):
                first_elem = root_element
                break
    return first_elem


def get_start_date(product):
    """
    Define start date of product version.

    Parameters
    ----------
    product : string
        product specification

    Returns
    -------
    datetime : datetime.datetime
        timestamp of start date

    """
    dt_dict = {'M2T1NXLND.5.12.4': datetime(1980, 1, 1)}
    return dt_dict[product]


def parse_args(args):
    """
    Parse command line parameters for recursive download

    Parameters
    ----------
    args : list of strings
        command line parameters

    Returns
    -------
    args: argparse.Namespace object
        command line parameters
    """
    parser = argparse.ArgumentParser(
        description="Download MERRA2 hourly data.",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "localroot",
        help='Root of local filesystem where the data is stored.')
    parser.add_argument(
        "-s",
        "--start",
        type=mkdate,
        help=(
            "Startdate. Either in format YYYY-MM-DD or YYYY-MM-DDTHH:MM."
            "If not given then the target folder is scanned for a start date."
            "If no data is found there then the first available "
            "date of the product is used."))
    parser.add_argument(
        "-e",
        "--end",
        type=mkdate,
        help=(
            "Enddate. Either in format YYYY-MM-DD or YYYY-MM-DDTHH:MM."
            "If not given then the current date is used."))
    help_string = '\n'.join(['MERRA2 product to download.',
                             'M2T1NXLND.5.12.4 available from {}'])
    help_string = help_string.format(get_start_date('M2T1NXLND.5.12.4'))

    parser.add_argument(
        "--product",
        choices=["M2T1NXLND.5.12.4"],
        default="M2T1NXLND.5.12.4",
        help=help_string)
    parser.add_argument("--username",
                        help='Username to use for download.')
    parser.add_argument("--password",
                        help='password to use for download.')
    parser.add_argument(
        "--n_proc",
        default=1,
        type=int,
        help='Number of parallel processes to use for downloading.')
    args = parser.parse_args(args)
    # set defaults that can not be handled by argparse

    # Compare versions to prevent mixing data sets
    version, first, last = folder_get_version_first_last(args.localroot)
    if args.product and version and (args.product != version):
        raise Exception(
            'Error: Found products of different '
            'version ({}) in {}. Abort download!'.format(
                version, args.localroot))
    if args.start is None or args.end is None:
        if not args.product:
            args.product = version
        if args.start is None:
            if last is None:
                if args.product:
                    args.start = get_start_date(args.product)
                else:
                    args.start = get_start_date('M2T1NXLND.5.12.4')
            else:
                args.start = last
        if args.end is None:
            args.end = datetime.now()

    prod_urls = {'M2T1NXLND.5.12.4':
                 {'root': 'https://goldsmr4.gesdisc.eosdis.nasa.gov',
                  'dirs': ['data', 'MERRA2', 'M2T1NXLND.5.12.4',
                           '%Y', '%m']}}

    args.urlroot = prod_urls[args.product]['root']
    args.urlsubdirs = prod_urls[args.product]['dirs']
    args.localsubdirs = ['%Y', '%m']

    print("Downloading data from {} to {} into folder {}.".format(
        args.start.isoformat(), args.end.isoformat(), args.localroot))
    return args


def main(args):
    args = parse_args(args)

    dts = list(daily(args.start, args.end))
    fname = ""
    url_create_fn = partial(create_dt_url, root=args.urlroot,
                            fname=fname, subdirs=args.urlsubdirs)
    fname_create_fn = partial(create_dt_fpath, root=args.localroot,
                              fname=fname, subdirs=args.localsubdirs)
    down_func = partial(download,
                        num_proc=args.n_proc,
                        username=args.username,
                        password="'" + args.password + "'",
                        recursive=True,
                        filetypes=['nc4'])
    download_by_dt(dts, url_create_fn,
                   fname_create_fn, down_func,
                   recursive=True)


def run():
    main(sys.argv[1:])