import os

if __name__ == '__main__':
    path_root = os.path.dirname(os.path.abspath(__file__))
    path_file = os.path.join(path_root, 'runwsgi.sh')
    os.system('bash %s' % path_file)

