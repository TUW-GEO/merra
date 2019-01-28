"""
Tests for the download module of GLDAS.
"""
import os
from datetime import datetime
from merra.download import get_last_formatted_dir_in_dir
from merra.download import get_first_formatted_dir_in_dir
from merra.download import get_last_folder
from merra.download import get_first_folder
from merra.download import folder_get_version_first_last

def test_get_last_dir_in_dir():
    path = os.path.join(os.path.dirname(__file__),
                        'folder_test', 'success')
    last_dir = get_last_formatted_dir_in_dir(path, "{time:%Y}")
    assert last_dir == '2018'


if __name__ == '__main__':
    test_get_last_dir_in_dir()