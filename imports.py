#sys, os 
import sys
sys.dont_write_bytecode = True
import os

#PyInstaller TempDir for Bundle Dir Path
frozen = 'not'
if getattr(sys, 'frozen', False):
    # we are running in a bundle
    frozen = 'ever so'
    bundle_dir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

#add lib to python path
sys.path.append(bundle_dir + "\lib")

#import pytan
from lib import *
from lib.pytan import *
from lib.requests import *
from lib.taniumpy import *

#others - all need to be referenced for the standalone package to work
import time
import math
import tempfile
import pprint
import traceback
import cgi
import Cookie
import getpass
import glob
import requests
import json
import csv
import shutil

#Specials
import getpass
from pptx import *
import pandas as pd
from pandas import *
import html5lib
import bs4

#helpers
import helper_getdata
import helper_prompt
import helper_hygieneclasses

#sensors
import sensors_java
import sensors_adobe
import sensors_sccm
import sensors_patch
import sensors_mcafee
import sensors_taniumstats
import sensors_security
