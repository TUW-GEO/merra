import os
import unittest

from datetime import datetime
from merra.download import get_last_formatted_dir_in_dir
from merra.download import get_first_formatted_dir_in_dir
from merra.download import get_last_folder
from merra.download import get_first_folder
from merra.download import folder_get_version_first_last


class Test(unittest.TestCase):
    """
    Tests for download module.
    """

    def test_get_last_dir_in_dir(self):
        path = os.path.join(os.path.dirname(__file__),
                            'folder_test', 'success')
        last_dir = get_last_formatted_dir_in_dir(path, "{time:%Y}")
        assert last_dir == '2018'

    def test_get_last_dir_in_dir_failure(self):
        path = os.path.join(os.path.dirname(__file__),
                            'folder_test', 'failure')
        last_dir = get_last_formatted_dir_in_dir(path, "{time:%Y}")
        assert last_dir == None

    def test_get_first_dir_in_dir(self):
        path = os.path.join(os.path.dirname(__file__),
                            'folder_test', 'success')
        first_dir = get_first_formatted_dir_in_dir(path, "{time:%Y}")
        assert first_dir == '2017'

    def test_get_first_dir_in_dir_failure(self):
        path = os.path.join(os.path.dirname(__file__),
                            'folder_test', 'failure')
        first_dir = get_first_formatted_dir_in_dir(path, "{time:%Y}")
        assert first_dir == None

    def test_get_last_folder(self):
        path = os.path.join(os.path.dirname(__file__),
                            'folder_test', 'success')
        last = get_last_folder(path, ['{time:%Y}', '{time:%m}'])
        last_should = os.path.join(path, '2018', '12')
        assert last == last_should

    def test_get_last_folder_no_folder(self):
        path = os.path.join(os.path.dirname(__file__),
                            'folder_test', 'failure')
        last = get_last_folder(path, ['{time:%Y}', '{time:%m}'])
        last_should = None
        assert last == last_should

    def test_get_first_folder(self):
        path = os.path.join(os.path.dirname(__file__),
                            'folder_test', 'success')
        last = get_first_folder(path, ['{time:%Y}', '{time:%m}'])
        last_should = os.path.join(path, '2017', '01')
        assert last == last_should

    def test_get_first_folder_no_folder(self):
        path = os.path.join(os.path.dirname(__file__),
                            'folder_test', 'failure')
        last = get_first_folder(path, ['{time:%Y}', '{time:%m}'])
        last_should = None
        assert last == last_should

    def test_get_start_end(self):
        path = os.path.join(os.path.dirname(__file__),
                            'merra-test-data', 'M2T1NXLND.5.12.4')
        version, start, end = folder_get_version_first_last(path)
        version_should = 'M2T1NXLND.5.12.4'
        start_should = datetime(2018, 10, 1)
        end_should = datetime(2018, 10, 1)
        assert version == version_should
        assert end == end_should
        assert start == start_should
    

if __name__ == "__main__":
    unittest.main()