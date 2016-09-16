from flask import Flask
from flask import render_template

import pandas as pd

# local
from curve_chart import get_curve_data

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/data/weekly-incidence-curve")
def data__weekly_incidence_curve():
    return get_curve_data()

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
