from . import settings

import os
import sys


def startup():
    try:
        import gunicorn
    except:
        raise Exception('[EE] GUNICORN NOT FOUND.')

    path_root = os.path.dirname(os.path.abspath(__file__))
    path_file = os.path.join(path_root, 'runwsgi.sh')

    for setting_variable in dir(settings):
        if setting_variable.startswith("__"):
            continue

        v = settings.__dict__[setting_variable]

        # apply just for string variables
        if isinstance(v, str):
            os.environ[setting_variable] = v

    os.environ['PYTHONPATH'] = os.path.dirname(sys.executable)
    os.environ['PATH'] += ':' + os.environ['PYTHONPATH']
    os.system('python --version')
    os.system('/bin/bash %s' % path_file)


if __name__ == '__main__':
    startup()
