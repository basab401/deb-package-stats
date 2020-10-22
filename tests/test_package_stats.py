###############################################################################
# To be run like this:
#   python3 -m pytest -s tests -v
###############################################################################

# Disable linting warnings:
# flake8: noqa E401
# flake8: noqa F811

import os
import io
import sys
import pytest
from pytest_mock import mocker


module_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, module_path + '/../../')


from package_stats_lib import utils, index_parser


###############################################################################
# Test functions for ParseDebPackageContentIndex class methods
###############################################################################
def test_download(tmpdir, mocker):
    ''' Test file download operation '''
    f = 'test_file1'
    url = 'http://dummy-testurl.com'
    local_path = tmpdir.mkdir('test_folder1')
    local_path.join(f).write('dummy'*256)
    mock_request = mocker.patch('requests.get', autospec=True)
    mock_response = mock_request.return_value.__enter__()
    mock_response.raw = mocker.MagicMock()
    mock_open = mocker.patch('builtins.open')
    mock_shutil = mocker.patch('shutil.copyfileobj')
    obj = index_parser.ParseDebPackageContentIndex(
        url, f, str(local_path), keep_files=True)
    obj.download()
    mock_request.assert_called_with('{}/{}'.format(url, f), stream=True)
    mock_open.assert_called_with('{}/{}'.format(str(local_path), f), 'wb')
    mock_shutil.assert_called_with(
        mock_response.raw, mock_open().__enter__())


def test_parse(tmpdir, mocker):
    ''' Test file parsing operation '''
    f = 'test_file2'
    local_path = tmpdir.mkdir('test_folder2')
    local_path.join(f).write('dummy'*256)
    mock_file = list(io.StringIO(
            'file1   p1,p2\nfile2  p1,p3\nfile3  p3\nfile4 p1'))
    mock_reader = mocker.patch('package_stats_lib.utils.read_line_by_Line')
    mock_reader.return_value = mock_file
    exp_stats = {'p1': 3, 'p3': 2, 'p2': 1}
    obj = index_parser.ParseDebPackageContentIndex(
        'http://dummy-testurl.com', f, str(local_path), keep_files=True)
    obj.parse()
    assert obj.package_stats == exp_stats


###############################################################################
# Test functions for utils module
###############################################################################
def test_gunzip_file(mocker):
    ''' Test gunzip of a local file by mocking necessary libraries '''
    mock_open = mocker.patch('builtins.open')
    mock_gzip_open = mocker.patch('gzip.open')
    mock_shutil = mocker.patch('shutil.copyfileobj')
    f_uncompressed = 'test_file'
    f_compressed = '{}.gz'.format(f_uncompressed)
    utils.gunzip_file(f_compressed, f_uncompressed)
    mock_gzip_open.assert_called_with(f_compressed, 'rb')
    mock_open.assert_called_with(f_uncompressed, 'wb')
    mock_shutil.assert_called_with(
        mock_gzip_open().__enter__(), mock_open().__enter__())


@pytest.mark.parametrize(
    'tmp_dict, reverse',
    [
        ({'a': 10, 'b': 20, 'c': 30}, True),
        ({'a': 30, 'b': 20, 'c': 10}, False)
    ]
)
def test_sort_dict_by_value(tmp_dict, reverse):
    ''' Test sorting of dictionary '''
    ret_dict = utils.sort_dict_by_value(tmp_dict, reverse)
    for index, (k, v) in enumerate(ret_dict.items()):
        if index == 0:
            assert k == 'c'
