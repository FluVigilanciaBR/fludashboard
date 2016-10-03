from unidecode import unidecode

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.font_manager as fm
import numpy as np


def _prepare_srag_data(season=2013):
    """

    """
    df_incidence = pd.read_csv(
        '../data/clean_data_filtro_sintomas_dtsin4mem-incidence-{}.csv'.format(season)
    )
    df_typical = pd.read_csv('../data/mem-typical-2016-uf.csv')
    df_thresholds = pd.read_csv('../data/mem-report-2016-uf.csv')
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
        df_thresholds.drop(['unidade_da_federacao', 'populacao'], axis=1), on='uf'
    ).rename(columns={'srag{}'.format(season): 'srag'})
    
    return {
        'df_incidence': df_incidence,
        'df_typical': df_typical,
        'df_thresholds': df_thresholds,
        'df_population': df_population,
        'df': df
    }


def get_incidence_color_alerts(season=2013, isoweek=None):
    """

    """
    result = _prepare_srag_data()
    df = result['df']

    mask = df.keys()
    if not isoweek is None:
        mask = df.eval('isoweek=={}'.format(isoweek))

    df_alert = df[mask].reset_index()
    # * Low: incidence < epidemic threshold | green
    df_alert = df_alert.assign(
        low_incidence=lambda se: se.eval('incidence < limiar_pre_epidemico')
    )

    # * Medium: epi. thresh. < incidence < high thresh. | yellow
    df_alert = df_alert.assign(
        medium_incidence=lambda se: se.eval(
            'limiar_pre_epidemico <= incidence < intensidade_alta'
    ))

    # * High: high thresh. < incidence < very high thresh. | orange
    df_alert = df_alert.assign(
        high_incidence=lambda se: se.eval(
            'intensidade_alta <= incidence < intensidade_muito_alta '
    ))

    # * Very high: very high thresh. < incidence | red
    df_alert = df_alert.assign(
        very_high_incidence=lambda se: se.eval(
            'intensidade_muito_alta <= incidence'
    ))

    # alert
    alert_col = df_alert.T.apply(
        lambda se: (
            4 if se.very_high_incidence else
            3 if se.high_incidence else
            2 if se.medium_incidence else
            1
        )
    )

    df_alert = df_alert.assign(alert=alert_col)

    return df_alert[[
        'uf', 'unidade_da_federacao', 'alert'
    ]].to_json(orient='records')



def get_curve_data(season=2013, uf_name='Rio Grande do Sul', isoweek=1):
    """

    """
    # data
    df = _prepare_srag_data(season=season)['df']
    df = df[df.unidade_da_federacao==uf_name]
    return df

