# Make Package Selector

make_package_selector is a utility written in Python to clean and build multiple directories. It does it by allowing you to select one or multiple directory in a visual table through CLI. 

You can also customize the start path (default is current directory) and source path (default is src) and other parameter. 


## Pre-requisite
* Python >= 3.6
* simple-term-menu >= 1.6.4

### Usage

```
$ make_package_selector.py [-h] [-d DIR] [-s SOURCE] [-y] [-w WAIT] 

Clean and build selected directories.

options:
  -h, --help                    Show this help message and exit
  -d DIR, --dir DIR             Absolute or relative path to start directory scanning. Default is current directory.
  -s SOURCE, --source SOURCE    The source directory inside the selected directory. Default is src 
  -y, --yes                     Suppress confirmation. Default is do not suppress. 
  -w WAIT, --wait WAIT          Time to wait in seconds before executing the command. Default is 15 seconds.

```


## Installation

### Using Pip
```
pip install make-package-selector
``` 

### Using Git
#### Clone the repo
```
git clone https://github.com/animeshdas/make_package_selector.git
```
#### Install
```
cd make_package_selector/dist
python -m pip install make_package_selector-<version>-py3-none-any.whl
```
OR
```
cd make_package_selector/dist
python -m pip install make_package_selector-<version>.tar.gz
```

