#!/usr/bin/env python3


###############################################################################
# Objective:
#
# This python command line tool takes the architecture (amd64, arm64 etc.)
# as an argument and downloads the compressed Contents file associated with it
# from a Debian mirror. Then this program parses the file and outputs the
# statistics of the top 10 packages that have the most files associated
# with them.

# An example output could be:
#
# python3 ./package_statistics.py amd64
#
# 1.  <package name 1>         <number of files>
# 2.  <package name 2>         <number of files>
# ......
# 10. <package name 10>        <number of files>
#
# References:
#
# Debian uses *deb packages to deploy and upgrade software.
# The packages are stored in repositories and each repository contains
# the so called "Contents index".
# The format of that file is well described here ->
#  https://wiki.debian.org/RepositoryFormat#A.22Contents.22_indices
#
# Use the following Debian mirror ->
#  http://ftp.uk.debian.org/debian/dists/stable/main/.
#
# linter used for compliance test: flake8
###############################################################################


import sys
import logging
import argparse

from package_stats_lib import index_parser, utils


if __name__ == '__main__':
    ''' Entry point for the package statistics tool '''
    # Parse command line arguments
    arg_p = argparse.ArgumentParser(
        usage='%(prog)s [OPTIONS]',
        description='CLI tool to download a debian package content index file \
            for the given architecture, parse the same and finally display \
            the correponding package statistics based on the number of files \
            it contains',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    arg_p.add_argument(
        '--arch',
        '-a',
        default='amd64',
        choices=['amd64', 'arm64', 'armel', 'armhf', 'i386', 'mips',
                 'mips64el', 'mipsel', 'ppc64el', 's390x'],
        help='Platform architecture for which the content index \
            file is to be downloaded and parsed')
    arg_p.add_argument(
        '--keep',
        '-k',
        action='store_true',
        help='Keep the downloaded/processed files')
    arg_p.add_argument(
        '--local_path',
        '-l',
        default='./tmp',
        help='Temporary folder to store logs and downloaded/parsed files')
    arg_p.add_argument(
        '--url',
        '-u',
        default='http://ftp.uk.debian.org/debian/dists/stable/main',
        help='Debian mirror URL')
    arg_p.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable additional log verbosity')
    args = arg_p.parse_args()
    utils.ensure_dir_exists(args.local_path)

    # Update logging preferences
    if (args.verbose):
        utils.cre_logger(console_level=logging.DEBUG,
                         file_level=logging.DEBUG,
                         log_dir=args.local_path)
    else:
        utils.cre_logger(console_level=logging.WARN,
                         file_level=logging.INFO,
                         log_dir=args.local_path)

    # Print a welcome message
    utils.print_welcome_msg()

    # Primary execution loop
    rc = 0
    file_to_download = 'Contents-{}.gz'.format(args.arch)
    try:
        # Instantiate ParseDebPackageContentIndex class and run the steps
        parser_obj = index_parser.ParseDebPackageContentIndex(
            args.url,
            file_to_download,
            args.local_path,
            args.keep)
        utils.cre_print.debug(repr(parser_obj))
        parser_obj.run()
    except Exception as e:
        utils.cre_print.error('{} failed to execute: {}'.format(
            sys.argv[0], e))
        rc = 1
    finally:
        utils.cre_print.debug('Preparing exit: rc = {}'.format(rc))

    sys.exit(rc)
