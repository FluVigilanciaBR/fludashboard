from flask import Flask
from flask import render_template

import click
import pandas as pd
import datetime
import sys
import os

# local
sys.path.insert(0, os.path.dirname(os.getcwd()))
from fludashboard.srag_data import get_srag_data, prepare_srag_data
from fludashboard.calc_srag_alert import apply_filter_alert_by_epiweek
from fludashboard.utils import prepare_keys_name

app = Flask(__name__)


@app.route("/")
def index():
    df_incidence = pd.read_csv(
        '../data/current_estimated_values.csv'
    )
    # prepare dataframe keys
    prepare_keys_name(df_incidence)

    # Here the code should recieve the user-requested year.
    # By default should be the current or latest available
    list_of_years = list(set(df_incidence.epiyear))

    year = max(list_of_years) if list_of_years else 0
    epiweek = datetime.datetime.now().isocalendar()[1]

    return render_template(
        "index.html",
        current_epiweek=epiweek,
        list_of_years=sorted(list_of_years, reverse=True),
        last_year=year
    )


@app.route('/data/incidence/<int:year>')
def get_incidence_data(year):
    df = prepare_srag_data(year)['df']

    return apply_filter_alert_by_epiweek(df).to_json(orient='records')


@app.route('/data/weekly-incidence-curve/<int:year>/')
@app.route('/data/weekly-incidence-curve/<int:year>/<string:state>')
def data__weekly_incidence_curve(year, state=None):
    if not year > 0:
        return '[]'

    if not state:
        state = 'Brasil'

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

    df = get_srag_data(year=year, uf_name=state_name, epiweek=epiweek)

    mask = (
        (~df.unidade_da_federacao.str.contains('Regi'))
    )
    df = df[mask]

    if not epiweek > 0:
        df = df.groupby('unidade_da_federacao', as_index=False).sum()
        df.epiweek = None

    # order by type
    df = df.assign(type_unit=1)

    try:
        df.loc[df.uf == 'BR', 'type_unit'] = 0
    except:
        pass

    df.sort_values(
        by=['type_unit', 'unidade_da_federacao', 'epiyear', 'epiweek'],
        inplace=True
    )
    df.reset_index(drop=True, inplace=True)
    df.drop('type_unit', axis=1, inplace=True)

    return '{"data": %s}' % df[ks].to_json(orient='records')


@app.route('/data/age-distribution/<int:year>/')
@app.route('/data/age-distribution/<int:year>/<int:week>/')
@app.route('/data/age-distribution/<int:year>/<int:week>/<string:state>')
def data__age_distribution(year, week=None, state=None):
    if not year > 0:
        return '[]'

    ks = [
        '0_4_anos', '5_9_anos', '10_19_anos', '20_29_anos',
        '30_39_anos', '40_49_anos', '50_59_anos', '60+_anos'
    ]

    if not state:
        state = 'Brasil'

    df = pd.DataFrame(
        get_srag_data(year=year, uf_name=state, epiweek=week)[ks].sum()
    ).T
    return df.to_csv(index=False)


@click.command()
@click.option('-p', default=5000, help='Port Number')
def startup(p):
    """
    """
    app.run(host='0.0.0.0', port=p, debug=True)


if __name__ == "__main__":
    startup()
