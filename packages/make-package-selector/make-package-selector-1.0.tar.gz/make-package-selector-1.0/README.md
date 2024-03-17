# Make Package Selector

make_package_selector is a utility written in Python to clean and build selected directories. It does it by allowing you to select one or multiple directory & its source path (default is src) to run : </br>

`make clean all -C <selected directory>/src`

#### Author : Animesh Das 
#### Email : &#106;&#111;&#98;&#115;&#52;&#97;&#110;&#105;&#64;&#103;&#109;&#97;&#105;&#108;&#46;&#99;&#111;&#109;


#### Github : https://github.com/animeshdas/make_package_selector


## Pre-requisite
Python >= 3.6

## Installation

### Using PIP
```
pip install make_package_selector
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