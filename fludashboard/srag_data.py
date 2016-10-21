from unidecode import unidecode

import pandas as pd


def _prepare_srag_data(year=2013):
    """

    """
    df_incidence = pd.read_csv(
        '../data/clean_data_filtro_sintomas_dtnotific4mem-incidence.csv'
    )[['UF', 'epiweek', 'SRAG{}'.format(year)]]
    df_typical = pd.read_csv('../data/mem-typical.csv')
    df_thresholds = pd.read_csv('../data/mem-report.csv')
    df_population = pd.read_csv(
        '../data/PROJECOES_2013_POPULACAO-simples_agebracket.csv'
    )

    level_dict = {
        'L0': 'Baixa', 'L1': 'Epidêmica',
        'L2': 'Alta', 'L3': 'Muito alta'
    }

    # prepare dataframe keys
    for _df in [df_incidence, df_typical, df_thresholds, df_population]:
        for k in _df.keys():
            _df.rename(columns={
                k: unidecode(
                    k.replace(' ', '_').replace('-', '_').lower()
                ).encode('ascii').decode('utf8')
            }, inplace=True)

    df = pd.merge(
        df_incidence, df_typical, on=['uf', 'epiweek'], how='right'
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


def get_srag_data(year, uf_name=None, epiweek=0):
    """

    """
    # data
    df = _prepare_srag_data(year=year)['df']
    mask = df.keys()

    if uf_name:
        mask = df.unidade_da_federacao == uf_name

    if epiweek:
        if uf_name:
            mask &= df.epiweek == epiweek
        else:
            mask = df.epiweek == epiweek

    df = df[mask]
    return df
