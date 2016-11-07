from flask import Flask
from flask import render_template

import click
import pandas as pd
import datetime
import sys
import os

# local
sys.path.insert(0, os.path.dirname(os.getcwd()))
from fludashboard.srag_data import (
    get_srag_data, prepare_srag_data, report_incidence,
    group_data_by_season
)
from fludashboard.calc_srag_alert import (
    apply_filter_alert_by_epiweek,
    calc_alert_rank_whole_year)
from fludashboard.utils import prepare_keys_name
from fludashboard.episem import episem

app = Flask(__name__)


@app.route("/")
def index():
    """

    :return:
    """
    df_incidence = pd.read_csv(
        '../data/current_estimated_values.csv'
    )
    # prepare dataframe keys
    prepare_keys_name(df_incidence)

    # Here the code should recieve the user-requested year.
    # By default should be the current or latest available
    list_of_years = list(set(df_incidence.epiyear))

    year = max(list_of_years) if list_of_years else 0
    epiweek = episem(datetime.datetime.now().strftime('%Y-%m-%d'))[-2:]

    return render_template(
        "index.html",
        current_epiweek=epiweek,
        list_of_years=sorted(list_of_years, reverse=True),
        last_year=year
    )


@app.route('/data/incidence/<int:year>/<string:territory_type>')
def get_incidence_data(year, territory_type):
    """

    :param territory_type: state or region
    :param year:
    :return:
    """
    df = prepare_srag_data(year)['df']
    df = df[
        df.tipo == ('Estado' if territory_type == 'state' else 'Regional')
    ]

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
    return get_srag_data(year=year, state_name=state)[ks].to_csv(index=False)


@app.route('/data/incidence-levels/<int:year>')
@app.route('/data/incidence-levels/<int:year>/<int:epiweek>/')
@app.route(
    '/data/incidence-levels/<int:year>/<int:epiweek>/<string:state_name>')
def data__incidence_levels(
    year, epiweek=None, state_name=None
):
    """
    When epiweek==None, the system will assume the whole year view.
    When state_name==None, the system will assume state_name=='Brasil'

    :param year:
    :param epiweek:
    :param state_name:
    :return:
    """
    if not year > 0:
        return '[]'

    if not state_name:
        state_name = 'Brasil'

    df = get_srag_data(year=year, state_name=state_name, epiweek=epiweek)

    if epiweek is not None and epiweek > 0:
        ks = ['l0', 'l1', 'l2', 'l3', 'situation']
        return df[ks].to_json(orient='records')

    # prepare data for the whole year
    df = apply_filter_alert_by_epiweek(df=df)

    se = pd.Series({
        'l0': df[df.alert == 1].count().l0,
        'l1': df[df.alert == 2].count().l1,
        'l2': df[df.alert == 3].count().l2,
        'l3': df[df.alert == 4].count().l3
    })

    rank = calc_alert_rank_whole_year(se)

    se.l0 = 0
    se.l1 = 0
    se.l2 = 0
    se.l3 = 0
    se['l%s' % (rank-1)] = 1
    se['situation'] = ''

    return pd.DataFrame(se).T.to_json(orient='records')




@app.route('/data/data-table/<int:year>')
@app.route('/data/data-table/<int:year>/<int:epiweek>')
@app.route('/data/data-table/<int:year>/<int:epiweek>/<string:territory_type>')
@app.route(
    '/data/data-table/<int:year>/<int:epiweek>/' +
    '<string:territory_type>/<string:state_name>')
def data__data_table(year, epiweek=None, territory_type=None, state_name=None):
    """
    1. Total number of cases in the selected year for eac
       State + same data for the Country
    2. Number of cases in the selected week for each
       State + same data for the Country
    3. Total number of cases in the selected year for selected State
    4. Number of cases in the selected week for selected State.

    :param year:
    :param epiweek:
    :param territory_type:
    :param state_name:
    :return:

    """
    if not year > 0:
        return '{"data": []}'

    ks = [
        'unidade_da_federacao',
        'epiweek',
        'situation',
        'srag'
    ]

    df = get_srag_data(year=year, state_name=state_name, epiweek=epiweek)

    if territory_type == 'state':
        mask = ~(df.tipo=='Regional')
    else:
        mask = ~(df.tipo=='Estado')

    df = df[mask]

    # for a whole year view
    if not epiweek:
        df = group_data_by_season(df, year)

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

    # add more information into srag field
    if df.shape[0]:
        df.srag = df[['50%', '2.5%', '97.5%', 'situation']].apply(
            lambda row: report_incidence(
                row['50%'], row['2.5%'], row['97.5%'], row['situation']
        ), axis=1)

        # change situation value by a informative text
        situation_dict = {
            'stable': 'Dado estável. Sujeito a pequenas alterações.',
            'estimated': 'Estimado. Sujeito a alterações.',
            'unknown': 'Dados incompletos. Sujeito a grandes alterações.'
        }
        df.situation = df.situation.map(
            lambda x: situation_dict[x] if x else ''
        )

    return '{"data": %s}' % df[ks].to_json(orient='records')


@app.route('/data/age-distribution/<int:year>/')
@app.route('/data/age-distribution/<int:year>/<int:week>/')
@app.route('/data/age-distribution/<int:year>/<int:week>/<string:state>')
def data__age_distribution(year, week=None, state=None):
    """

    :param year:
    :param week:
    :param state:
    :return:
    """
    if not year > 0:
        return '[]'

    ks = [
        '0_4_anos', '5_9_anos', '10_19_anos', '20_29_anos',
        '30_39_anos', '40_49_anos', '50_59_anos', '60+_anos'
    ]

    if not state:
        state = 'Brasil'

    df = pd.DataFrame(
        get_srag_data(year=year, state_name=state, epiweek=week)[ks].sum()
    ).T
    return df.to_csv(index=False)


@click.command()
@click.option('-p', default=5000, help='Port Number')
def startup(p):
    """

    :param p:
    :return:
    """
    app.run(host='0.0.0.0', port=p, debug=True)


if __name__ == "__main__":
    startup()
