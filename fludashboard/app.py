from fludashboard.libs.views import app
from fludashboard.libs.utils import recursive_dir_name
from fludashboard import settings

import os


def update_data_files(update_data: bool):
    path_root = recursive_dir_name(os.path.abspath(__file__), steps_back=1)
    path_data = os.path.join(path_root, 'data')

    update_params = '-nc' if not update_data else '-N'
    wget_prefix = (
        ('wget %s ' % update_params) +
        'https://raw.githubusercontent.com/FluVigilanciaBR/data/master/data'
    )

    command = '''cd %(path_data)s && \
    %(wget_prefix)s/clean_data_epiweek-weekly-incidence_w_situation.csv && \
    %(wget_prefix)s/current_estimated_values.csv && \
    %(wget_prefix)s/historical_estimated_values.csv && \
    %(wget_prefix)s/mem-report.csv && \
    %(wget_prefix)s/mem-typical.csv''' % {
        'path_data': path_data,
        'wget_prefix': wget_prefix
    }
    print(command.replace('&&', ' && \ \n'))
    os.system(command)
    print('[II] DONE!')


def startup():
    """

    :return:
    """
    update_data_files(update_data=settings.APP_UPDATE_DATA)

    app.run(
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        debug=settings.APP_DEBUG
    )

    return app


if __name__ == "__main__":
    startup()
