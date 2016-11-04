from unidecode import unidecode

import pandas as pd


def get_season_situation(df):
    def _fn(se):
        return df[
            (df.uf == se.uf) & (df.epiyear == se.epiyear)
        ].situation.unique()[0]
    return _fn


def get_season_level(se):
    """
    Generate season level code based on counts over weekly activity

    """
    if se.l2 + se.l3 > 4:
        return 4  # 'red'
    elif se.l2 + se.l3 > 1:
        return 3  # 'orange'
    elif se.l1 > 1:
        return 2  # 'yellow'
    # else
    return 1 # 'green'


def group_data_by_season(df, season):
    """

    :param df:
    :param season:
    :return:
    """
    level_dict = {
        'l0': 'Baixa', 'l1': 'Epidêmica',
        'l2': 'Alta', 'l3': 'Muito alta'
    }
    season_basic_cols = [
        'uf', 'unidade_da_federacao', 'epiyear', 'srag',
        '0_4_anos', '5_9_anos', '10_19_anos', '20_29_anos', '30_39_anos',
        '40_49_anos', '50_59_anos', '60+_anos'
    ]
    season_cols = season_basic_cols + ['tipo', 'situation', 'level']

    df['level'] = df[list(level_dict.keys())].idxmax(axis=1)

    df_tmp = df[season_cols].copy()

    situation = list(
        df_tmp[df_tmp.epiyear == season].situation.unique()
    )
    if 'unknown' in situation or 'estimate' in situation:
        df_tmp.loc[df_tmp.epiyear == season, 'situation'] = 'incomplete'
    else:
        df_tmp.loc[df_tmp.epiyear == season, 'situation'] = 'stable'

    df_by_season = df_tmp[season_basic_cols].groupby(
        ['uf', 'unidade_da_federacao', 'epiyear'],
        as_index=False
    ).sum()

    df_by_season['situation'] = df_by_season.apply(
        get_season_situation(df_tmp), axis=1
    )

    df_by_season_level = pd.crosstab(
        [df_tmp.uf, df_tmp.unidade_da_federacao, df_tmp.epiyear],
        df_tmp.level
    ).reset_index()

    df_by_season_level.columns.name = None

    for i in range(4):
        _l = ('l%s' % i)
        if not _l in df_by_season_level.keys():
            df_by_season_level[_l] = 0

    df_by_season['level'] = df_by_season_level[
        list(level_dict.keys())
    ].apply(
        get_season_level, axis=1
    )

    df_by_season.situation.replace({
        'incomplete': 'Incompleto',
        'stable': 'Estável',
    }, inplace=True)

    df_by_season['epiweek'] = 0

    return df_by_season

def report_incidence(x, low, high, situation):
    """
    original name: report_inc

    :param x:
    :param low:
    :param high:
    :param situation:
    :return:
    """
    if situation == 'stable':
        y = '%.2f' % x
    elif situation == 'estimated':
        y = '%.2f [%.2f - %.2f]' % (x, low, high)
    else:
        y = '*%.2f' % x
    return y


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
