from fludashboard.libs.views import app
from fludashboard import settings


def startup():
    """

    :return:
    """
    app.run(
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        debug=settings.DEBUG
    )

    return app


if __name__ == "__main__":
    startup()
