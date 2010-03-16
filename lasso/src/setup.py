"""
This file is required to create
Windows executables. If you would like to do this, then
make sure you have setup "py2exe"
http://sourceforge.net/projects/py2exe/

To build on Windows enter the following on the Command Prompt

'python setup.py py2exe'
"""

from distutils.core import setup
import py2exe

setup(windows=['LL_main.py'])