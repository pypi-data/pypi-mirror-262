import warnings
warnings.filterwarnings("ignore")

__author__ = 'mr moorgh'
__version__ = 1.1

from sys import version_info
if version_info[0] == 2: # Python 2.x
    from phpthon import *
elif version_info[0] == 3: # Python 3.x
    from phpthon.phpthon import *



import urllib.request
import mimetypes
import ssl
import os
try:
    import requests
except ImportError:
    try:
        os.system("pip install requests")
    except:
        try:
            os.system("pip3 install requests")
        except:
            try:
                os.system("python3 -m pip install requests")
            except:
                os.system("python -m pip install requests")
    import requests
import json
import re
from random import randint
from subprocess import check_output as chk
from pathlib import Path
import sys

def detect_file_format(url):
    ssl._create_default_https_context = ssl._create_unverified_context
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0;Win64)"}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    content_type = response.headers.get('Content-Type')
    file_extension = mimetypes.guess_extension(content_type)

    if file_extension:
        return file_extension.lstrip('.')
    else:
        return None

def file_get_contents(name):
    if name.startswith("http://") or name.startswith("https://"):
        return requests.get(name).text
    else:
        file=open(name,"r")
        contents=file.read()
        file.close()
        return contents

def file_put_contents(name,contents):
    file=open(name,"w")
    file.write(contents)
    file.close()
    return True

def filesize(file):
    file_name = file
    file_stats = os.stat(file_name)
    return file_stats.st_size

def file_link_size(link):
    ssl._create_default_https_context = ssl._create_unverified_context
    site = urllib.request.urlopen(link)
    meta = site.info()
    file_size = int(site.getheader('Content-Length'))
    return file_size

def json_encode(js):
    try:
        return json.dumps(js)
    except:
        raise TypeError("Failed To Encode json!")

def json_decode(js):
    try:
        return json.loads(js)
    except:
        raise TypeError("Failed To Decode json!")

def rand(start,end):
    return str(randint(int(start),int(end)))

def preg_match(match,string):
    return re.search(match,string)

def explode(delimiter, string):
    return string.split(delimiter)

def implode(string):
    return string.strip()

def isset(varname):
    if varname == None:
        return False
    else:
        return True
        
def substr(string, start, length=None):
    if length is None:
        return string[start:]
    else:
        return string[start:start + length]

def strpos(string,find):
    return find in string

def shell_exec(cmd):
    try:
        return chk(cmd,shell=True).decode()
    except Exception as er:
        return str(er)

def file_exists(file):
    return Path(file).exists()

def empty(var):
    if var == "" or var == None:
        return True
    else:
        return False

def print_r(var, return_string=False):
    if return_string:
        import json
        return json.dumps(var, indent=4, sort_keys=True)
    else:
        import pprint
        pprint.pprint(var)

def help():
    text = """PHPThon Library Help :
Sample Code :
#pip install phpthon
#file_get_contents Example
from phpthon import *
print(file_get_contents("https://mrapiweb.ir"))
    """
    print(text)

def phpversion():
    return "phpthon Version 1.1 , Simulated From PHP 7.4"

def exit(text=None):
    if text is not None:
        print(text)
    sys.exit(0)
