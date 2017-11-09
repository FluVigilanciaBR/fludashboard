import os

if __name__ == '__main__':
    try:
        import gunicorn
    except:
        raise Exception('[EE] GUNICORN NOT FOUND.')

    path_root = os.path.dirname(os.path.abspath(__file__))
    path_file = os.path.join(path_root, 'runwsgi.sh')
    os.system('bash %s' % path_file)

