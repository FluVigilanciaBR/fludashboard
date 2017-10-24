"""
---------------------------------------------------
clean_data_epiweek-weekly-incidence_w_situation.csv
---------------------------------------------------

Fields:

* 0-4 anos
* 10-19 anos
* 20-29 anos
* 30-39 anos
* 40-49 anos
* 5-9 anos
* 50-59 anos
* 60+ anos
* DELAYED
* FLU_A
* FLU_B
* INCONCLUSIVE
* NEGATIVE
* NOTTESTED
* OTHERS
* POSITIVE_CASES
* SRAG
* Situation
* TESTING_IGNORED
* Tipo
* Total
* UF
* Unidade da Federação
* VSR
* dado
* epiweek
* epiyear
* epiyearweek
* escala
* sexo

---------------------------------------------------
current_estimated_values.csv
---------------------------------------------------

Fields:

* UF
* epiyear
* epiweek
* SRAG
* Tipo
* Situation
* mean
* 50%
* 2.5%
* 97.5%
* L0
* L1
* L2
* L3
* Run date
* dado
* escala

---------------------------------------------------
mem-report.csv
---------------------------------------------------

Fields:

* UF
* População
* Média geométrica do pico de infecção das temporadas regulares
* regiã* o de baixa atividade típica
* limiar pré-epidêmico
* intensidade alta
* intensidade muito alta
* SE típica do início do surto
* "SE típica do início do surto - IC inferior (2,5%)"
* "SE típica do início do surto - IC superior (97,5%)"
* duração típica do surto
* "duração típica do surto - IC inferior (2,5%)"
* "duração típica do surto - IC superior (97,5%)"
* ano
* Unidade da Federação
* Tipo
* dado
* escala

---------------------------------------------------
mem-typical.csv
---------------------------------------------------

Fields:

* UF
* População
* epiweek
* corredor baixo
* corredor mediano
* corredor alto
* ano
* Unidade da Federação
* Tipo
* dado
* escala

"""
from unidecode import unidecode
# local
from .utils import recursive_dir_name

import pandas as pd
import os


def prepare_keys_name(df):
    """
    Standardises data frame keys

    :param df:
    :type df: pd.DataFrame
    :return: pd.DataFrame
    """
    for k in df.keys():
        df.rename(columns={
            k: unidecode(
                k.replace(' ', '_').replace('-', '_').lower()
            ).encode('ascii').decode('utf8')
        }, inplace=True)
    return df


def get_season_situation(df):
    """

    :param df:
    :return:
    """
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
    elif se.l2 + se.l3 >= 1:
        return 3  # 'orange'
    elif se.l1 >= 1:
        return 2  # 'yellow'
    # else
    return 1 # 'green'


def group_data_by_season(df, df_age_dist=None, season=None):
    """

    :param df:
    :param df_age_dist:
    :param season:
    :return:
    """
    level_dict = {
        'l0': 'Baixa', 'l1': 'Epidêmica',
        'l2': 'Alta', 'l3': 'Muito alta'
    }
    season_basic_cols = [
        'uf', 'unidade_da_federacao', 'epiyear', 'srag'
    ]
    season_cols = season_basic_cols + ['tipo', 'situation', 'level']

    df['level'] = df[list(level_dict.keys())].idxmax(axis=1)

    df_tmp = df[season_cols].copy()

    situation = list(
        df_tmp[df_tmp.epiyear == season].situation.unique()
    )
    l_incomplete = ['unknown', 'estimated', 'incomplete', 'Incompleto']
    if set(l_incomplete).intersection(situation):
        df_tmp.loc[df_tmp.epiyear == season, 'situation'] = 'incomplete'
    else:
        df_tmp.loc[df_tmp.epiyear == season, 'situation'] = 'stable'

    if df_age_dist is not None:
        df_by_season = df_age_dist[[
            'uf', 'unidade_da_federacao', 'epiyear', 'sexo', 'srag',
            '0_4_anos', '5_9_anos', '10_19_anos', '20_29_anos', '30_39_anos',
            '40_49_anos', '50_59_anos', '60+_anos'
        ]].groupby([
            'uf', 'unidade_da_federacao', 'epiyear', 'sexo'
        ], as_index=False).sum()
    else:
        df_by_season = df_tmp[season_basic_cols].groupby(
            ['uf', 'unidade_da_federacao', 'epiyear'],
            as_index=False
        ).sum()

    df_by_season['situation'] = df_by_season.apply(
        get_season_situation(df_tmp), axis=1
    )

    df_by_season_level = pd.crosstab([
        df_tmp.uf, df_tmp.unidade_da_federacao, df_tmp.epiyear
    ], df_tmp.level).reset_index()

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

    df_by_season['epiweek'] = 0

    return df_by_season


def report_incidence(x, situation, low=None, high=None):
    """
    original name: report_inc

    :param x:
    :param situation:
    :param low:
    :param high:
    :return:
    """
    if situation == 'stable':
        y = '%.2f' % x
    elif situation == 'estimated':
        y = '%.2f [%.2f - %.2f]' % (x, low, high)
    else:
        y = '*%.2f' % x
    return y


def read_data(dataset: str='srag', scale: str='incidence'):
    """

    :param dataset:
    :param scale:
    :return:
    """
    path_root = recursive_dir_name(os.path.abspath(__file__), steps_back=2)
    path_data = os.path.join(path_root, 'data')

    return pd.read_csv(
        os.path.join(path_data, 'current_estimated_values.csv')
    )


def prepare_data(
    dataset: str, scale: str, year: int = None
) -> {str: pd.DataFrame}:
    """

    :param year:
    :param dataset:
    :param scale:
    :return:
    """
    path_root = recursive_dir_name(__file__, steps_back=2)
    path_data = os.path.join(path_root, 'data')

    df_incidence = pd.read_csv(
        os.path.join(path_data, 'current_estimated_values.csv')
    )
    df_typical = pd.read_csv(
        os.path.join(path_data, 'mem-typical.csv')
    )
    df_thresholds = pd.read_csv(
        os.path.join(path_data, 'mem-report.csv')
    )

    # filter
    df_incidence.escala.replace({
        'incidência': 'incidence',
        'casos': 'cases'
    }, inplace=True)

    df_incidence = df_incidence[
        (df_incidence.dado == dataset) &
        (df_incidence.escala == scale)
    ]

    df_typical.escala.replace({
        'incidência': 'incidence',
        'casos': 'cases'
    }, inplace=True)
    df_typical = df_typical[
        (df_typical.dado == dataset) &
        (df_typical.escala == scale)
    ]

    df_thresholds.escala.replace({
        'incidência': 'incidence',
        'casos': 'cases'
    }, inplace=True)
    df_thresholds = df_thresholds[
        (df_thresholds.dado == dataset) &
        (df_thresholds.escala == scale)
    ]

    # prepare dataframe keys
    for _df in [df_incidence, df_typical, df_thresholds]:
        prepare_keys_name(_df)

    if year:
        df_incidence = df_incidence[df_incidence.epiyear == year]
        df_typical.assign(epiyear=year)

    df = pd.merge(
        df_incidence, df_typical, on=['uf', 'epiweek'], how='outer'
    ).merge(
        df_thresholds.drop(['unidade_da_federacao'], axis=1),
        on='uf', how='outer'
    )

    # resolve some conflicts
    df.situation.fillna('', inplace=True)

    return {
        'df_incidence': df_incidence,
        'df_typical': df_typical,
        'df_thresholds': df_thresholds,
        'df': df
    }


def get_data(
    dataset: str, scale: str, year: int,
    state_name: str=None, epiweek: int=0
):
    """

    :param dataset:
    :param scale:
    :param year:
    :param state_name:
    :param epiweek:
    :return:
    """
    # data
    df = prepare_data(dataset=dataset, scale=scale, year=year)['df']

    if state_name:
        df = df[df.unidade_da_federacao == state_name]

    if epiweek:
        df = df[df.epiweek == epiweek]

    return df


def get_data_age_sex(
    dataset: str, scale: str, year: int,
    state_name: str=None, epiweek: int=0
):
    """

    :param dataset:
    :param scale:
    :param year:
    :param state_name:
    :param epiweek:
    :return:

    """
    season = year  # alias
    path_root = recursive_dir_name(__file__, steps_back=2)
    path_data = os.path.join(path_root, 'data')

    age_cols = [
        '0_4_anos', '5_9_anos', '10_19_anos', '20_29_anos', '30_39_anos',
        '40_49_anos', '50_59_anos', '60+_anos'
    ]

    if not state_name:
        state_name = 'Brasil'

    # data
    df_age_dist = pd.read_csv(
        os.path.join(
            path_data,
            'clean_data_epiweek-weekly-incidence_w_situation.csv'
        ), low_memory=False, encoding='utf-8'
    )

    prepare_keys_name(df_age_dist)

    df_age_dist = df_age_dist[
        (df_age_dist.epiyear == season) &
        (df_age_dist.unidade_da_federacao == state_name)
    ]

    if epiweek is not None and epiweek > 0:
        df_age_dist = df_age_dist[df_age_dist.epiweek == epiweek]
        df = df_age_dist
    else:
        df = prepare_data(dataset=dataset, scale=scale, year=year)['df']
        df = df[df.unidade_da_federacao == state_name]
        df = group_data_by_season(
            df=df, df_age_dist=df_age_dist, season=season
        )

    df = df[age_cols + ['sexo']].set_index('sexo').transpose()
    df.rename(columns={'F': 'Mulheres', 'M': 'Homens'}, inplace=True)

    return df
