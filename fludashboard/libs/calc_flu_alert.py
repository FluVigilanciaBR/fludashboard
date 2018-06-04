"""


"""
# local
from .migration import dataset_id as dataset_id_list
from .flu_data import FluDB

import numpy as np
import pandas as pd

contingency_name_from_id = {
    1: 'Nível basal',
    2: 'Nível 0',
    3: 'Nível 1',
    4: 'Nível 2',
}

db = FluDB()


def get_season_level(se):
    """

    :param se: pd.Series
    :return: int
    """
    _max = max([
        se.very_high_level, se.high_level, se.epidemic_level, se.low_level
    ])

    return (
        0 if np.isnan(_max) else
        1 if se.low_level == _max else
        2 if se.epidemic_level == _max else
        3 if se.high_level == _max else
        4
    )


def calc_alert_rank_whole_year(se):
    """
    calculate the alert rank for the whole year

    :param se: pd.Series
    :return:
    """
    high_threshold = se.very_high_level + se.high_level

    return (
        4 if high_threshold >= 5 else
        3 if high_threshold >= 1 else
        2 if se.epidemic_level >= 1 else
        1
    )


def apply_filter_alert_by_epiweek(
    df: pd.DataFrame, view_name: str, epiweek: int=None
):
    """

    :param df:
    :param view_name:
    :param epiweek:
    :return:
    """
    if epiweek is not None:
        mask = df.eval('epiweek=={}'.format(epiweek))
    else:
        mask = df.keys()

    df_alert = df[mask].copy().reset_index()

    return df_alert


def prepare_contingency_level(df: pd.DataFrame):
    epiyear = df.epiyear.max()
    territories_id = df.territory_id.unique()
    alerts = {}

    for territory_id in territories_id:
        alerts[territory_id] = contingency_level(epiyear, territory_id)

    return alerts


def get_contingency_level(se):
    """

    :param se: pd.Series
    :return: int
    """
    return contingency_level(se.epiyear, se.territory_id)


def show_contingency_alert(dataset_id: int, year: int, territory_id: int):
    """

    :param dataset_id:
    :param year:
    :param territory_id:
    :return:
    """
    df = db.get_data(
        dataset_id=dataset_id, scale_id=1, year=year,
        territory_id=territory_id
    )

    # If not obitoflu dataset (3), uses last 4 weeks, o.w. use 3:
    if dataset_id < 3:
        wdw = 4
    else:
        wdw = 3

    weeks = len(df)
    if weeks < wdw+1:
        alert_zone = False
        data_increase = False
    else:
        for i in range(wdw+1, weeks+1):
            alert_zone = any(df.estimated_cases[(i-wdw):i] > df.typical_high[(i-wdw):i])
            data_increase = all(
                df.estimated_cases[(i-wdw):i].values -
                df.estimated_cases[(i-wdw - 1):(i-1)].values > 0
            )
            if (alert_zone & data_increase):
                break

    dataset_from_id = dict(
        zip(dataset_id_list.values(), dataset_id_list.keys())
    )

    print('''
    Data: %s
    Entered alert zone? %s
    Steady increase in the window of interest? %s
    Trigger alert? %s
    ''' % (dataset_from_id[dataset_id], alert_zone, data_increase,
       alert_zone & data_increase)
    )

    return alert_zone & data_increase


def alert_trigger(dataset_id: int, year: int, territory_id: int):
    """

    :param dataset_id:
    :param year:
    :param territory_id:
    :return:
    """
    df = db.get_data(
        dataset_id=dataset_id, scale_id=1, year=year,
        territory_id=territory_id
    )

    # If not obitoflu dataset (3), uses last 4 weeks, o.w. use 3:
    if dataset_id < 3:
        wdw = 4
    else:
        wdw = 3

    weeks = df.shape[0]
    if weeks < wdw+1:
        alert_zone = False
        data_increase = False
    else:
        for i in range(wdw+1, weeks+1):
            alert_zone = any(df.estimated_cases[(i-wdw):i] > df.typical_high[(i-wdw):i])
            data_increase = all(
                df.estimated_cases[(i-wdw):i].values -
                df.estimated_cases[(i-wdw - 1):(i-1)].values > 0
            )
            if (alert_zone & data_increase):
                return alert_zone & data_increase

    return alert_zone & data_increase


def contingency_level(year: int, territory_id: int):
    """

    :param year:
    :param territory_id:
    :return:
    """
    if alert_trigger(dataset_id=3, year=year, territory_id=territory_id):
        return 4
    elif alert_trigger(dataset_id=2, year=year, territory_id=territory_id):
        return 3
    elif alert_trigger(dataset_id=1, year=year, territory_id=territory_id):
        return 2
    return 1
