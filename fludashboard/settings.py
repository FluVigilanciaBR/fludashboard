import os

# variables about app configuration
DEBUG = False  # bool
HOST = "0.0.0.0"  # str
PATH = os.path.dirname(os.path.abspath(__file__))  # str
PORT = 5000  # int
UPDATE_DATA = True  # bool

DATABASE = {
    'NAME': 'fludashboard',  # database name
    'USER': 'root',
    'PASSWORD': '',
    'HOST': 'localhost',
    'PORT': '',
}

try:
    from .local_settings import *
except:
    pass
