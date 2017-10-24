import os

# variables about app configuration
APP_DEBUG = False  # bool
APP_HOST = "0.0.0.0"  # str
APP_PATH = os.path.dirname(os.path.abspath(__file__))  # str
APP_PORT = 5000  # int
APP_UPDATE_DATA = True  # bool

try:
    from .local_settings import *
except:
    pass
