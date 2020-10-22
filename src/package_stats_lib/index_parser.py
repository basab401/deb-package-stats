#!/usr/bin/env python3


import os
import requests
import shutil
from pathlib import Path
from . import utils


class ParseDebPackageContentIndex():
    ''' This class provides methods to do the following:
        - download a package content-index file
        - parse the file to create package statistics
        - print the results in a pretty format
        - wrappr run method to execute the above steps
    '''
    def __init__(self,
                 deb_mirror_url,
                 file_to_download,
                 local_path,
                 keep_files=False,
                 number_of_rows_to_print=10):
        # Initialize a package_stats disctionary that will have this data:
        #  { package_name:  number of files in this package }
        self.package_stats = {}
        # Debian Mirror url to download the file from
        self.deb_mirror_url = deb_mirror_url
        # Debian package content index file, which is in compressed form
        self.file_to_download = file_to_download
        # Local file path for the downloaded file
        self.path_to_downloaded_file = '{}/{}'.format(
            local_path, file_to_download)
        # Local file path after uncompression
        self.file_to_parse = '{}/{}'.format(
            local_path, Path(self.path_to_downloaded_file).stem)
        # Flag to indicate if the temporary files need to be kept
        self.keep_files = keep_files
        # Number of row-entries to print in the result
        self.number_of_rows = number_of_rows_to_print

    @utils.timeit
    def download(self):
        ''' Download the given package content-index compressed file '''
        url_final = '{}/{}'.format(self.deb_mirror_url, self.file_to_download)
        utils.cre_print.info('Downloading {} from {} ...'.format(
            self.file_to_download, self.deb_mirror_url))
        with requests.get(url_final, stream=True) as f_input:
            with open(self.path_to_downloaded_file, 'wb') as f_output:
                shutil.copyfileobj(f_input.raw, f_output)
        if os.path.exists(self.path_to_downloaded_file):
            utils.cre_print.info(
                'Successfully downloaded deb package content'
                '-index file: {}'.format(self.path_to_downloaded_file))

    @utils.timeit
    def parse(self):
        ''' Parse the downloaded file and update package statistics '''
        for line in utils.read_line_by_Line(self.file_to_parse):
            words = line.split()
            # Ignore a line if it does not contain two delimted words:
            #  intent here is to consider a line only if it has two columns
            #  (FILE, LOCATION) delimited by one or more spaces
            if len(words) != 2:
                continue
            # Convert the LOCATION field into a list of package names:
            # LOCATION - a list of qualified package names, separated by comma.
            #   A qualified package name has the form [[$AREA/]$SECTION/]$NAME,
            #   where $AREA is the archive area, $SECTION the package section,
            #   and $NAME the name of the package.
            # Inclusion of area in the name should be considered deprecated.
            packages = words[1].split(',')
            for package in packages:
                # Consider only the package name (i.e., ignore $AREA/$SECTION/)
                package = package.split('/')[-1]
                if package in self.package_stats.keys():
                    self.package_stats[package] += 1
                else:
                    self.package_stats[package] = 1
        # Now sort the dict by descending order of its values
        self.package_stats = utils.sort_dict_by_value(self.package_stats)
        utils.cre_print.info('Generated package statistics')

    def print_results(self):
        ''' Print the statistics on the terminal in this format:
        1.  <package name 1>         <number of files>
        2.  <package name 2>         <number of files>
        ......
        10. <package name 10>       <number of files>
        '''
        print('{}'.format('-'*70))
        print('\t\t\tPackage Statistics')
        print('{}'.format('-'*70))
        print('{:4s} {:40s} {:15s}'.format(
            'SrNo', 'Package Name', 'Number of files'))
        for index, (k, v) in enumerate(self.package_stats.items()):
            print('{:3d}. {:40s} {:15d}'.format(index+1, k, v))
            if index == self.number_of_rows-1:
                break

    def run(self):
        # Download the compressed content-index file from the given mirror
        self.download()
        # Uncompress the downloaded index file
        utils.gunzip_file(self.path_to_downloaded_file, self.file_to_parse)
        # Parse the file and display the results { package:file_count }
        self.parse()
        # Display the results
        self.print_results()

    def __del__(self):
        ''' Cleanup files '''
        if not self.keep_files:
            utils.cre_print.debug('Cleaning up downloaded and parsed files')
            utils.cre_print.debug('Removing {}'.format(
                self.path_to_downloaded_file))
            if os.path.exists(self.path_to_downloaded_file):
                os.remove(self.path_to_downloaded_file)
            utils.cre_print.debug('Removing {}'.format(
                self.file_to_parse))
            if os.path.exists(self.file_to_parse):
                os.remove(self.file_to_parse)

    def __repr__(self):
        output = 'url: {}, file_to_download: {}, downloaded_file: {}, '\
                'local_file_to_parse: {}'.format(
                       self.deb_mirror_url,
                       self.file_to_download,
                       self.path_to_downloaded_file,
                       self.file_to_parse)
        return '{' + output + '}'
