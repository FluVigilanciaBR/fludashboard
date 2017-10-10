from fludashboard.libs.views import app

import click


@click.command()
@click.option('-p', default=5000, help='Port Number')
@click.option('-ip', default='0.0.0.0', help='Host address')
def startup(ip, p):
    """

    :param ip:
    :param p:
    :return:
    """
    app.run(host=ip, port=p, debug=True)


if __name__ == "__main__":
    startup()
