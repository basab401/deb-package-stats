
# package_statistics command line tool

* [About](#about)
* [Source tree](#tree)
* [Prerequisites](#prerequisites)
* [How to use it](#use)
* [Future work](#TODOs)
* [Maintainer](#maintainer)


## <a name="about">About</a>


This package_statistic command line tool is created to do the following:

* Take in the architecture (amd64, arm64, mips etc.) as an argument
* Download the compressed Contents file associated with the architecture from a given debian mirror
* Parse the file
* Output the statistics of the top 10 packages having most files

 
## <a name="tree">Source tree</a>

```
├── Dockerfile
├── package_statistics.py
├── package_stats_lib
│   ├── index_parser.py
│   ├── __init__.py
│   └── utils.py
├── README.md
├── requirements.txt
├── setup.py
└── tests
    ├── __init__.py
    └── test_package_stats.py
```


## <a name="prerequisites">Prerequisites</a>


* Primary requirements: Python3.6 or higher
  * For linting - flake8
* For details, please see requirements.txt


## <a name="use">How to use it</a>
**Tool help:**
```bash
usage: package_statistics.py [OPTIONS]

CLI tool to download a debian package content index file for the given
architecture, parse the same and finally display the correponding package
statistics based on the number of files it contains

optional arguments:
  -h, --help            show this help message and exit
  --arch {amd64,arm64,armel,armhf,i386,mips,mips64el,mipsel,ppc64el,s390x}, -a {amd64,arm64,armel,armhf,i386,mips,mips64el,mipsel,ppc64el,s390x}
                        Platform architecture for which the content index file
                        is to downloaded and parsed (default: amd64)
  --keep, -k            Keep the downloaded/processed files (default: False)
  --local_path LOCAL_PATH, -l LOCAL_PATH
                        Temporary folder to store logs and downloaded/parsed
                        files (default: ./tmp)
  --url URL, -u URL     Debian mirror URL (default:
                        http://ftp.uk.debian.org/debian/dists/stable/main)
  --verbose, -v         Enable additional log verbosity (default: False)
```

**To run unit tests and linting:**
```bash
$ python3 -m pytest -s tests -v
$ flake8 .
```

**Sample Output:**
```bash
$ ./package_statistics.py --arch mips
**********************************************************************
        Welcome to the package_statistics command line tool!


Please wait while it does the following...
1. take in the architecture (amd64, arm64, mips etc.) as an argument
2. download the compressed Contents file associated with the
   architecture from a given debian mirror
3. parse the file
4. output the statistics of the top 10 packages having most files
**********************************************************************


----------------------------------------------------------------------
                    Package Statistics
----------------------------------------------------------------------
SrNo Package Name                             Number of files
  1. fonts-cns11643-pixmaps                            110999
  2. papirus-icon-theme                                 69475
  3. texlive-fonts-extra                                65577
  4. flightgear-data-base                               62458
  5. piglit                                             49913
  6. trilinos-doc                                       49591
  7. obsidian-icon-theme                                48829
  8. widelands-data                                     34984
  9. libreoffice-dev-doc                                33667
 10. moka-icon-theme                                    33326

```


## <a name="TODOs">Future work</a>

* Analyse and improve tool performance (if any):
  * speed of download operation (network)
  * storage consumption (file save and uncompression)
  * memory usage (parsing)
* Build & Packaging:
  * Create a docker image for carrying out the unit tests and functional tests
  * Create a python package (egg/wheel/debian) for ease of distribution
* Analyse and remove any hard platform dependencies and assumptions


## <a name="maintainer">Maintainer</a>

* Basabjit Sengupta (basab401@yahoo.co.in)
