from flask import Flask
from flask import render_template
from unidecode import unidecode

import click
import pandas as pd
import datetime

# local
from curve_chart import get_curve_data, get_incidence_color_alerts
from calc_alert import apply_filter_alert_by_isoweek

app = Flask(__name__)


@app.route("/")
def index():
    with open('./data/br-states.json') as f:
        br_states = f.read()

    df_incidence = pd.read_csv(
        '../data/clean_data_filtro_sintomas_dtnotific4mem-incidence.csv'
    )
    df_typical = pd.read_csv('../data/mem-typical-clean_data_filtro_sintomas_dtnotific4mem-criterium-method.csv')
    df_thresholds = pd.read_csv('../data/mem-report-clean_data_filtro_sintomas_dtnotific4mem-criterium-method.csv')
    df_population = pd.read_csv('../data/populacao_uf_regional_atual.csv')

    # prepare dataframe keys
    for _df in [df_incidence, df_typical, df_thresholds, df_population]:
        for k in _df.keys():
            _df.rename(columns={
                k: unidecode(
                    k.replace(' ', '_').replace('-', '_').lower()
                ).encode('ascii').decode('utf8')
            }, inplace=True)

    df = pd.merge(
        df_incidence, df_typical, on=['uf', 'isoweek'], how='right'
    ).merge(
        df_thresholds.drop(['unidade_da_federacao', 'populacao'], axis=1), 
        on='uf'
    )

    # Here the code should recieve the user-requested year.
    # By default should be the current or latest available
    year = 2016
    df_alert = apply_filter_alert_by_isoweek(df, year=year)

    isoweek = datetime.datetime.now().isocalendar()[1]
    return render_template(
        "index.html", 
        data=df_alert.to_json(orient='records'),
        br_states=br_states,
        current_isoweek=isoweek,
    )


@app.route("/data/weekly-incidence-curve/<string:state>")
def data__weekly_incidence_curve(state, year=2016):
    ks = [
        'corredor_baixo', 'corredor_mediano', 'corredor_alto', 'srag',
        'limiar_pre_epidemico', 'intensidade_alta', 'intensidade_muito_alta'
    ]
    return get_curve_data(year=year, uf_name=state)[ks].to_csv(index=None)


@app.route("/data/incidence-color-alerts/<isoweek>")
def data__incidence_color_alerts(isoweek, year=2016):
    return get_incidence_color_alerts(year=year, isoweek=isoweek)


@click.command()
@click.option('-p', default=5000, help='Port Number')
def startup(p):
    """
    """
    app.run(host='0.0.0.0', port=p, debug=True)

if __name__ == "__main__":
    startup()
