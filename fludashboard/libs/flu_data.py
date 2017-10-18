"""
---------------------------------------------------
historical_estimated_values.csv
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
* base_epiyearweek
* base_epiyear
* base_epiweek
* dado
* escala

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

import numpy as np
import os
import pandas as pd

STATE_CODE = {
    '11': 'Rondônia',
    '12': 'Acre',
    '13': 'Amazonas',
    '14': 'Roraima',
    '15': 'Pará',
    '16': 'Amapá',
    '17': 'Tocantins',
    '21': 'Maranhão',
    '22': 'Piauí',
    '23': 'Ceará',
    '24': 'Rio Grande do Norte',
    '25': 'Paraíba',
    '26': 'Pernambuco',
    '27': 'Alagoas',
    '28': 'Sergipe',
    '29': 'Bahia',
    '31': 'Minas Gerais',
    '32': 'Espírito Santo',
    '33': 'Rio de Janeiro',
    '35': 'São Paulo',
    '41': 'Paraná',
    '42': 'Santa Catarina',
    '43': 'Rio Grande do Sul',
    '50': 'Mato Grosso do Sul',
    '51': 'Mato Grosso',
    '52': 'Goiás',
    '53': 'Distrito Federal',
    'BR': 'Brasil',
    'RegC': 'Regional Centro',
    'RegL': 'Regional Leste',
    'RegN': 'Regional Norte',
    'RegS': 'Regional Sul',
    'RegOfN': 'Norte',
    'RegOfNE': 'Nordeste',
    'RegOfSE': 'Sudeste',
    'RegOfCO': 'Centro-oeste',
    'RegOfS': 'Sul'
}


def get_state_code_from_name(state_name: str) -> str:
    """

    :param state_name:
    :return:
    """
    return [
        (k, v) for k, v in STATE_CODE.items()
        if v == state_name
    ][0][0]


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


def read_data(
    file_name: str, dataset: str, scale: str, state_code: str=None,
    year: int=None, week: int=None, base_year: int=None, base_week: int=None,
    historical_week: int=None, low_memory=True, **kwargs
):
    """

    :param file_name:
    :param dataset:
    :param scale:
    :param state_code:
    :param year:
    :param week:
    :param base_year:
    :param base_week:
    :param historical_week:
    :param kwargs:
    :return:
    """
    mask = True

    path_root = recursive_dir_name(__file__, steps_back=3)
    path_data = os.path.join(path_root, 'data')
    file_path = os.path.join(path_data, file_name)

    df = pd.read_csv(file_path, low_memory=low_memory)

    # prepare dataframe keys
    prepare_keys_name(df)
    # change escala text from Portuguese to English
    df.escala.replace({
        'incidência': 'incidence',
        'casos': 'cases'
    }, inplace=True)

    # filter
    mask &= (df.dado == dataset) & (df.escala == scale)

    if state_code is not None:
        mask &= df.uf == state_code

    if year is not None:
        mask &= df.epiyear == year

    if base_year is not None:
        mask &= df.base_epiyear == base_year

    if week is not None and week > 0:
        mask &= df.epiweek == week
    elif base_week is not None:
        mask &= df.base_epiweek == base_week
    elif historical_week is not None:
        mask &= df.epiweek <= historical_week

    # apply mask
    df = df[mask]

    # remove no necessaries fields
    df.drop(labels=['dado', 'escala'], axis=1, inplace=True)

    return df


def get_data(
    dataset: str, scale: str, year: int,
    state_code: str=None, week: int=None, historical_week: int=None
):
    """

    :param dataset:
    :param scale:
    :param year:
    :param state_code:
    :param week: 0 week == all weeks
    :param historical_week:
    :return:
    """
    settings = {
        'dataset': dataset,
        'scale': scale,
        'state_code': state_code
    }

    df_incidence = read_data(
        'current_estimated_values.csv', **settings,
        year=year, week=week, historical_week=historical_week
    )
    df_typical = read_data('mem-typical.csv', **settings)
    df_thresholds = read_data('mem-report.csv', **settings)

    if year is not None:
        df_typical.assign(epiyear=year)

    # First, last keep only stable weeksfor notification curve:
    df_incidence.loc[(df_incidence.situation != 'stable'), 'srag'] = np.nan

    df = pd.merge(
        df_incidence, df_typical,
        on=['uf', 'epiweek'], how='outer'
    ).merge(
        df_thresholds.drop(['unidade_da_federacao'], axis=1),
        on='uf', how='outer'
    )

    if historical_week is not None and historical_week > 0:
        ks = [
            k for k in df.keys()
            if k not in ['estimated_cases', '2.5%', '97.5%']
        ]

        df_historical = read_data(
            'historical_estimated_values.csv', **settings,
            year=year, week=week, base_week=historical_week
        )

        # Adapt historical dataset:
        df_historical.sort_values(['epiyear', 'epiweek'], inplace=True)
        df_historical['estimated_cases'] = df_historical['50%']

        df = pd.merge(
            df[ks], df_historical[['epiweek', 'estimated_cases', '2.5%', '97.5%']],
            on='epiweek', how='outer'
        )
    else:
        df['estimated_cases'] = df['50%']

    # force week filter (week 0 == all weeks)
    if week is not None and week > 0:
        df = df[df.epiweek == week]

    # resolve some conflicts
    df.situation.fillna('', inplace=True)

    return df


def get_data_age_sex(
    dataset: str, scale: str, year: int,
    state_code: str='BR', week: int=0
):
    """

    :param dataset:
    :param scale:
    :param year:
    :param state_code:
    :param week:
    :return:

    """
    season = year  # alias

    age_cols = [
        '0_4_anos', '5_9_anos', '10_19_anos', '20_29_anos', '30_39_anos',
        '40_49_anos', '50_59_anos', '60+_anos'
    ]

    # data
    df_age_dist = read_data(
        'clean_data_epiweek-weekly-incidence_w_situation.csv',
        dataset=dataset, scale=scale, year=season, state_code=state_code,
        low_memory=False
    )

    if week is not None and week > 0:
        df_age_dist = df_age_dist[df_age_dist.epiweek == week]
        df = df_age_dist
    else:
        df = get_data(
            dataset=dataset, scale=scale, year=year, state_code=state_code
        )
        df = group_data_by_season(
            df=df, df_age_dist=df_age_dist, season=season
        )

    df = df[age_cols + ['sexo']].set_index('sexo').transpose()
    df.rename(columns={'F': 'Mulheres', 'M': 'Homens'}, inplace=True)

    return df
