__author__ = 'mr moorgh'

from sys import version_info
if version_info[0] == 2: # Python 2.x
    from phpthon import *
elif version_info[0] == 3: # Python 3.x
    from phpthon.phpthon import *
