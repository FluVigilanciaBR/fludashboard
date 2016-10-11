from unidecode import unidecode

import pandas as pd


def _prepare_srag_data(year=2013):
    """

    """
    df_incidence = pd.read_csv(
        '../data/clean_data_filtro_sintomas_dtnotific4mem-incidence.csv'
    )[['UF', 'isoweek', 'SRAG{}'.format(year)]]
    df_typical = pd.read_csv(
        '../data/mem-typical-clean_data_filtro_sintomas_dtnotific4mem-' +
        'criterium-method.csv')
    df_thresholds = pd.read_csv(
        '../data/mem-report-clean_data_filtro_sintomas_dtnotific4mem-' +
        'criterium-method.csv')
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
    ).rename(columns={'srag{}'.format(year): 'srag'})

    return {
        'df_incidence': df_incidence,
        'df_typical': df_typical,
        'df_thresholds': df_thresholds,
        'df_population': df_population,
        'df': df
    }


def get_incidence_color_alerts(year=2013, isoweek=None):
    """

    """
    result = _prepare_srag_data(year=year)
    df = result['df']

    mask = df.keys()
    if isoweek is not None:
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


def get_curve_data(year, uf_name=None, isoweek=0):
    """

    """
    # data
    df = _prepare_srag_data(year=year)['df']
    mask = df.keys()

    if uf_name:
        mask = df.unidade_da_federacao == uf_name

    if isoweek:
        if uf_name:
            mask &= df.isoweek == isoweek
        else:
            mask = df.isoweek == isoweek

    df = df[mask]
    return df
