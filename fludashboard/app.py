from flask import Flask
from flask import render_template

import click
import pandas as pd
import datetime
import sys
import os

# local
sys.path.insert(0, os.path.dirname(os.getcwd()))
from fludashboard.srag_data import get_srag_data  # get_incidence_color_alerts
from fludashboard.calc_srag_alert import apply_filter_alert_by_epiweek
from fludashboard.utils import prepare_keys_name

app = Flask(__name__)


@app.route("/")
def index_week():
    df_incidence = pd.read_csv(
        '../data/clean_data_filtro_sintomas_dtnotific4mem-incidence.csv'
    )
    # prepare dataframe keys
    prepare_keys_name(df_incidence)

    # Here the code should recieve the user-requested year.
    # By default should be the current or latest available
    list_of_years = []
    for col in df_incidence.columns:
        if 'srag' in col:
            list_of_years.append(int(col.replace('srag', '')))

    year = max(list_of_years)
    epiweek = datetime.datetime.now().isocalendar()[1]

    return render_template(
        "index.html",
        current_epiweek=epiweek,
        list_of_years=sorted(list_of_years, reverse=True),
        last_year=year
    )


@app.route("/year/")
def index_year():
    df_incidence = pd.read_csv(
        '../data/clean_data_filtro_sintomas_dtnotific4mem-incidence.csv'
    )
    # prepare dataframe keys
    prepare_keys_name(df_incidence)

    # Here the code should recieve the user-requested year.
    # By default should be the current or latest available
    list_of_years = []
    for col in df_incidence.columns:
        if 'srag' in col:
            list_of_years.append(int(col.replace('srag', '')))

    year = max(list_of_years)
    epiweek = datetime.datetime.now().isocalendar()[1]

    return render_template(
        "index-year.html",
        current_epiweek=epiweek,
        list_of_years=sorted(list_of_years, reverse=True),
        last_year=year
    )


@app.route('/data/incidence/<int:year>')
def get_incidence_data(year):
    df_incidence = pd.read_csv(
        '../data/clean_data_filtro_sintomas_dtnotific4mem-incidence.csv'
    )
    df_typical = pd.read_csv(
        '../data/mem-typical.csv'
    )
    df_thresholds = pd.read_csv(
        '../data/mem-report.csv'
    )
    df_population = pd.read_csv(
        '../data/PROJECOES_2013_POPULACAO-simples_agebracket.csv'
    )

    # prepare dataframe keys
    for _df in [df_incidence, df_typical, df_thresholds, df_population]:
        prepare_keys_name(_df)

    df = pd.merge(
        df_incidence, df_typical, on=['uf', 'epiweek'], how='right'
    ).merge(
        df_thresholds.drop(['unidade_da_federacao', 'populacao'], axis=1),
        on='uf'
    )

    return apply_filter_alert_by_epiweek(
        df, year=year
    ).to_json(orient='records')


@app.route('/data/weekly-incidence-curve/<int:year>/')
@app.route('/data/weekly-incidence-curve/<int:year>/<string:state>')
def data__weekly_incidence_curve(year, state=None):
    if not year > 0:
        return '[]'

    ks = [
        'epiweek', 'corredor_baixo', 'corredor_mediano', 'corredor_alto',
        'srag',
        'limiar_pre_epidemico', 'intensidade_alta', 'intensidade_muito_alta'
    ]
    return get_srag_data(year=year, uf_name=state)[ks].to_csv(index=False)


@app.route("/data/incidence-color-alerts/<int:year>/<int:epiweek>")
def data__incidence_color_alerts(year, epiweek):
    # return get_incidence_color_alerts(year=year, epiweek=epiweek)
    year, epiweek  # just to skip flake8 warnings
    return '[]'


@app.route("/data/data-table/<int:year>")
@app.route("/data/data-table/<int:year>/<int:epiweek>")
@app.route("/data/data-table/<int:year>/<int:epiweek>/<string:state_name>")
def data__data_table(year, epiweek=None, state_name=None):
    """
    1. Total number of cases in the selected year for eac
       State + same data for the Country
    2. Number of cases in the selected week for each
       State + same data for the Country
    3. Total number of cases in the selected year for selected State
    4. Number of cases in the selected week for selected State.

    """
    if not year > 0:
        return '{"data": []}'

    ks = [
        'unidade_da_federacao',
        'epiweek',
        'srag'
    ]

    df = get_srag_data(year=year, uf_name=state_name, epiweek=epiweek)[ks]

    if not epiweek > 0:
        df = df.groupby('unidade_da_federacao', as_index=False).sum()
        df.epiweek = None

    return '{"data": %s}' % df.to_json(orient='records')


@click.command()
@click.option('-p', default=5000, help='Port Number')
def startup(p):
    """
    """
    app.run(host='0.0.0.0', port=p, debug=True)


if __name__ == "__main__":
    startup()
