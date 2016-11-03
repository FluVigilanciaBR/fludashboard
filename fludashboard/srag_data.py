from unidecode import unidecode

import pandas as pd


def prepare_srag_data(year=None):
    """

    """
    df_incidence = pd.read_csv(
        '../data/current_estimated_values.csv'
    )
    df_typical = pd.read_csv('../data/mem-typical.csv')
    df_thresholds = pd.read_csv('../data/mem-report.csv')

    # prepare dataframe keys
    for _df in [df_incidence, df_typical, df_thresholds]:
        for k in _df.keys():
            _df.rename(columns={
                k: unidecode(
                    k.replace(' ', '_').replace('-', '_').lower()
                ).encode('ascii').decode('utf8')
            }, inplace=True)

    df = pd.merge(
        df_incidence, df_typical, on=['uf', 'epiweek'], how='right'
    ).merge(
        df_thresholds.drop(['unidade_da_federacao'], axis=1),
        on='uf'
    )

    if year:
        df = df[df.epiyear == year]

    return {
        'df_incidence': df_incidence,
        'df_typical': df_typical,
        'df_thresholds': df_thresholds,
        'df': df
    }


def get_srag_data(year, state_name=None, epiweek=0):
    """

    """
    # data
    df = prepare_srag_data(year=year)['df']
    mask = df.keys()

    if state_name:
        mask = df.unidade_da_federacao == state_name

    if epiweek:
        if state_name:
            mask &= df.epiweek == epiweek
        else:
            mask = df.epiweek == epiweek

    df = df[mask]
    return df
