from flask import Flask
from flask import render_template

import click
import pandas as pd
import datetime

# local
from curve_chart import get_curve_data, get_incidence_color_alerts

app = Flask(__name__)


@app.route("/")
def index():
    isoweek = datetime.datetime.now().isocalendar()[1]
    return render_template("index.html", current_isoweek=isoweek)


@app.route("/data/weekly-incidence-curve/<isoweek>")
def data__weekly_incidence_curve(isoweek):
    return get_curve_data(isoweek=isoweek)


@app.route("/data/incidence-color-alerts/<isoweek>")
def data__incidence_color_alerts(isoweek):
    return get_incidence_color_alerts(isoweek=isoweek)


@click.command()
@click.option('-p', default=5000, help='Port Number')
def startup(p):
    """
    """
    app.run(host='0.0.0.0', port=p, debug=True)

if __name__ == "__main__":
    startup()
