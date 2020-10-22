#!/usr/bin/env python3

import os
import gzip
import time
import shutil
import logging


# custom logger for this module
cre_print = logging.getLogger('package_stats')


def cre_logger(console_level=logging.INFO,
               file_level=logging.INFO,
               log_dir='./tmp'):
    ''' Set custom logger attributes '''
    log_file = '{}/cre_automation.log'.format(log_dir)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(file_level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[file_handler, console_handler])


def timeit(method):
    ''' Decorator to time individual function execution '''
    def timed(*args, **kwargs):
        start_time = time.time()
        result = method(*args, **kwargs)
        end_time = time.time()
        cre_print.debug('{} - {}s'.format(
            method.__name__, (end_time - start_time)))
        return result
    return timed


def gunzip_file(file_to_gunzip, gunzipped_file):
    ''' Uncompress the given gzipped file '''
    cre_print.debug('file_to_gunzip: {},  gunzipped_file: {}'.format(
        file_to_gunzip, gunzipped_file))
    with gzip.open(file_to_gunzip, 'rb') as f_input:
        with open(gunzipped_file, 'wb') as f_output:
            shutil.copyfileobj(f_input, f_output)


def read_line_by_Line(file_to_read):
    ''' Yield a line at a time from the given file '''
    cre_print.debug('file_to_read: {}'.format(file_to_read))
    with open(file_to_read, 'r', encoding='utf-8') as f:
        for line in f:
            yield line


def sort_dict_by_value(dict_to_sort, reverse=True):
    ''' Sort a given dictionary by its values '''
    return {k: v for k, v in sorted(
                dict_to_sort.items(),
                key=lambda x: x[1],
                reverse=reverse)}


def print_welcome_msg():
    ''' Print the welcome message for the tool '''
    print('{}'.format('*'*70))
    print('\tWelcome to the package_statistics command line tool!\n\n')
    print('Please wait while it does the following...')
    print('1. take in the architecture (amd64, arm64, mips etc.) '
          'as an argument')
    print('2. download the compressed Contents file associated '
          'with the')
    print('   architecture from a given debian mirror')
    print('3. parse the file')
    print('4. output the statistics of the top 10 packages having most files')
    print('{}\n\n'.format('*'*70))


def ensure_dir_exists(dir_path):
    ''' Create a direcotry path if it does not yet exist '''
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
