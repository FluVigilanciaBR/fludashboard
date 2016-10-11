from flask import Flask
from flask import render_template

import click
import pandas as pd
import datetime

# local
from curve_chart import get_curve_data, get_incidence_color_alerts
from calc_alert import apply_filter_alert_by_isoweek
from utils import prepare_keys_name

app = Flask(__name__)


@app.route("/")
def index():

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
          list_of_years.append(int(col.replace('srag','')))

    year = max(list_of_years)
    isoweek = datetime.datetime.now().isocalendar()[1]

    return render_template(
        "index.html", 
        current_isoweek=isoweek,
        list_of_years=sorted(list_of_years, reverse=True),
        last_year=year
    )


@app.route('/data/incidence/<int:year>')
def get_incidence_data(year):
    df_incidence = pd.read_csv(
        '../data/clean_data_filtro_sintomas_dtnotific4mem-incidence.csv'
    )
    df_typical = pd.read_csv(
        '../data/mem-typical-clean_data_filtro_sintomas_dtnotific4mem-criterium-method.csv'
    )
    df_thresholds = pd.read_csv(
        '../data/mem-report-clean_data_filtro_sintomas_dtnotific4mem-criterium-method.csv'
    )
    df_population = pd.read_csv('../data/populacao_uf_regional_atual.csv')

    # prepare dataframe keys
    for _df in [df_incidence, df_typical, df_thresholds, df_population]:
        prepare_keys_name(_df)

    df = pd.merge(
        df_incidence, df_typical, on=['uf', 'isoweek'], how='right'
    ).merge(
        df_thresholds.drop(['unidade_da_federacao', 'populacao'], axis=1), 
        on='uf'
    )

    return apply_filter_alert_by_isoweek(
        df, year=year
    ).to_json(orient='records')


@app.route('/data/weekly-incidence-curve/<int:year>/')
@app.route('/data/weekly-incidence-curve/<int:year>/<string:state>')
def data__weekly_incidence_curve(year, state=None):
    if not year > 0:
        return '[]'

    ks = [
        'isoweek', 'corredor_baixo', 'corredor_mediano', 'corredor_alto', 'srag',
        'limiar_pre_epidemico', 'intensidade_alta', 'intensidade_muito_alta'
    ]
    return get_curve_data(year=year, uf_name=state)[ks].to_csv(index=False)


@app.route("/data/incidence-color-alerts/<int:year>/<int:isoweek>")
def data__incidence_color_alerts(year, isoweek):
    return '[]'
    return get_incidence_color_alerts(year=year, isoweek=isoweek)


@app.route("/data/data-table/<int:year>")
@app.route("/data/data-table/<int:year>/<int:isoweek>")
@app.route("/data/data-table/<int:year>/<int:isoweek>/<string:state_name>")
def data__data_table(year, isoweek=None, state_name=None):
    """
    1. Total number of cases in the selected year for each 
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
      'isoweek',
      'srag'
    ]
    
    df = get_curve_data(year=year, uf_name=state_name, isoweek=isoweek)[ks]
    
    if not isoweek > 0:
        print(df[df.unidade_da_federacao=='Acre']['srag'])
        print(df[df.unidade_da_federacao=='São Paulo']['srag'])
        df = df.groupby('unidade_da_federacao', as_index=False).sum()
        df.isoweek = None
    
    return '{"data": %s}' % df.to_json(orient='records')


@click.command()
@click.option('-p', default=5000, help='Port Number')
def startup(p):
    """
    """
    app.run(host='0.0.0.0', port=p, debug=True)

if __name__ == "__main__":
    startup()
