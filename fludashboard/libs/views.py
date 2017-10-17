from flask import render_template, Flask
# local
from . import flu_data
from .utils import cross_domain, calc_last_epiweek
from .calc_flu_alert import (
    apply_filter_alert_by_epiweek,
    calc_alert_rank_whole_year)
from .episem import episem

import datetime
import pandas as pd

app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static'
)


def compose_data_url(variables: str):
    """

    :param variables:
    :return:
    """
    url_var = {
        'data': '/data/<string:dataset>/<string:scale>',
        'year': '<int:year>',
        'epiweek': '<int:epiweek>',
        'territory_type': '<string:territory_type>',
        'state': '<string:state>',
        'state_name': '<string:state_name>'
    }

    url = [
        url_var[v] if v in url_var else v
        for v in ['data'] + variables.split('/')
    ]

    return '/'.join(url)


@app.route("/super-header")
def super_header():
    return render_template("super-header.html")


@app.route("/")
def index():
    """

    :return:
    """
    df = flu_data.read_data()

    # prepare dataframe keys
    flu_data.prepare_keys_name(df)

    # Here the code should recieve the user-requested year.
    # By default should be the current or latest available
    list_of_years = list(set(df.epiyear))
    year = max(list_of_years) if list_of_years else 0
    epiweek = episem(datetime.datetime.now().strftime('%Y-%m-%d'))[-2:]
    last_week_years = {
        y: calc_last_epiweek(y) for y in list_of_years
    }

    return render_template(
        "index.html",
        current_epiweek=epiweek,
        list_of_years=sorted(list_of_years, reverse=True),
        last_year=year,
        last_week_years=last_week_years
    )


@app.route("/help")
def app_help():
    """

    :return:
    """
    return render_template("help.html")


@app.route(compose_data_url('year/territory_type'))
def get_data(
    dataset: str, scale: str, year: int, territory_type: str
):
    """

    :param dataset:
    :param scale:
    :param year:
    :param territory_type:
    :return:
    """
    df = flu_data.prepare_data(dataset=dataset, scale=scale, year=year)['df']
    df = df[
        df.tipo == ('Estado' if territory_type == 'state' else 'Regional')
    ]

    return apply_filter_alert_by_epiweek(df).to_json(orient='records')


@app.route(compose_data_url('year/weekly-incidence-curve'))
@app.route(compose_data_url('year/state/weekly-incidence-curve'))
def data__weekly_incidence_curve(
    dataset: str, scale: str, year: int, state: str='Brasil'
):
    """

    :param dataset:
    :param scale:
    :param year:
    :param state:
    :return:
    """
    if not year > 0:
        return '[]'

    ks = [
        'epiweek', 'corredor_baixo', 'corredor_mediano', 'corredor_alto',
        'srag', 'limiar_pre_epidemico', 'intensidade_alta',
        'intensidade_muito_alta'
    ]

    df = flu_data.get_data(
        dataset=dataset, scale=scale, year=year, state_name=state
    )

    try:
        min_week = int(df.loc[df['situation'] == 'estimated', 'epiweek'].min())

        df['estimated_cases'] = None
        df['ci_lower'] = None
        df['ci_upper'] = None

        mask = df['epiweek'] >= min_week

        df.loc[mask, 'estimated_cases'] = df.loc[mask, '50%']
        df.loc[mask, 'ci_lower'] = df.loc[mask, '2.5%']
        df.loc[mask, 'ci_upper'] = df.loc[mask, '97.5%']

        ks += ['estimated_cases', 'ci_lower', 'ci_upper']
    except:
        pass

    try:
        min_week = int(df.loc[df['situation'] == 'unknown', 'epiweek'].min())

        df['incomplete_data'] = None

        mask = df['epiweek'] >= min_week
        df.loc[mask, 'incomplete_data'] = df.loc[mask, '97.5%']

        ks += ['incomplete_data']
    except:
        pass

    return df[ks].to_csv(index=False, na_rep='null')


@app.route(compose_data_url('year/levels'))
@app.route(compose_data_url('year/epiweek/levels'))
@app.route(compose_data_url('year/epiweek/state_name/levels'))
def data__incidence_levels(
    dataset: str, scale: str, year: int,
    epiweek: int=None, state_name: str='Brasil'
):
    """
    When epiweek==None, the system will assume the whole year view.
    When state_name==None, the system will assume state_name=='Brasil'

    :param dataset:
    :param scale:
    :param year:
    :param epiweek:
    :param state_name:
    :return:
    """
    if not year > 0:
        return '[]'

    df = flu_data.get_data(
        dataset=dataset, scale=scale, year=year,
        state_name=state_name, epiweek=epiweek
    )

    if epiweek is not None and epiweek > 0:
        ks = ['l0', 'l1', 'l2', 'l3']
        df[ks] *= 100
        df[ks] = df[ks].round(2)

        ks += ['situation']
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

    return (pd.DataFrame(se).T*100).round(2).to_json(orient='records')


@app.route(compose_data_url('year/data-table'))
@app.route(compose_data_url('year/epiweek/data-table'))
@app.route(compose_data_url('year/epiweek/territory_type/data-table'))
@app.route(
    compose_data_url('year/epiweek/territory_type/state_name/data-table')
)
def data__data_table(
    dataset: str, scale: str, year: int, epiweek: int=None,
    territory_type: str=None, state_name: str=None
):
    """
    1. Total number of cases in the selected year for eac
       State + same data for the Country
    2. Number of cases in the selected week for each
       State + same data for the Country
    3. Total number of cases in the selected year for selected State
    4. Number of cases in the selected week for selected State.

    :param dataset:
    :param scale:
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

    df = flu_data.get_data(
        dataset=dataset, scale=scale, year=year,
        state_name=state_name, epiweek=epiweek
    )

    if territory_type == 'state':
        mask = ~(df.tipo == 'Regional')
    else:
        mask = ~(df.tipo == 'Estado')

    df = df[mask]

    # for a whole year view
    if not epiweek:
        df = flu_data.group_data_by_season(df, season=year)

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
        if epiweek:
            df.srag = df[['50%', '2.5%', '97.5%', 'situation']].apply(
                lambda row: flu_data.report_incidence(
                    row['50%'], row['situation'], row['2.5%'], row['97.5%']
                ), axis=1)
        else:
            df.srag = df[['srag', 'situation']].apply(
                lambda row: flu_data.report_incidence(
                    row['srag'], row['situation']
                ), axis=1)

        # change situation value by a informative text
        situation_dict = {
            'stable': 'Dado estável. Sujeito a pequenas alterações.',
            'estimated': 'Estimado. Sujeito a alterações.',
            'unknown': 'Dados incompletos. Sujeito a grandes alterações.',
            'incomplete': 'Dados incompletos. Sujeito a grandes alterações.'
        }

        df.situation = df.situation.map(
            lambda x: situation_dict[x] if x else ''
        )

    return '{"data": %s}' % df[ks].round({
        'srag': 2
    }).to_json(orient='records')


@app.route(compose_data_url('year/age-distribution'))
@app.route(compose_data_url('year/epiweek/age-distribution'))
@app.route(compose_data_url('year/epiweek/state/age-distribution'))
@cross_domain(origin='*')
def data__age_distribution(
    dataset: str, scale: str, year: int,
    epiweek: int=None, state: str=None
):
    """

    :param dataset:
    :param scale:
    :param year:
    :param epiweek:
    :param state:
    :return:
    """
    if not year > 0:
        return '[]'

    if not state:
        state = 'Brasil'

    df = pd.DataFrame(
        flu_data.get_data_age_sex(
            dataset=dataset, scale=scale,
            year=year, state_name=state, epiweek=epiweek
        )
    ).round(2)

    df.rename(index={
        '0_4_anos': '0-4 anos',
        '5_9_anos': '5-9 anos',
        '10_19_anos': '10-19 anos',
        '20_29_anos': '20-29 anos',
        '30_39_anos': '30-39 anos',
        '40_49_anos': '40-49 anos',
        '50_59_anos': '50-59 anos',
        '60+_anos': '60+ anos'
    }, inplace=True)

    # the replace is used when there is no data in the df
    return ('index' + df.to_csv()).replace('""', '')
