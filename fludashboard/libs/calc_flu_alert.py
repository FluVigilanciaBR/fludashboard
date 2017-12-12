"""


"""
import numpy as np
import pandas as pd


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
        3 if high_threshold > 1 else
        2 if se.epidemic_level >= 1 else
        1
    )


def apply_filter_alert_by_epiweek(
    df: pd.DataFrame, epiweek: int=None
):
    """

    :param df:
    :param epiweek:
    :return:
    """
    if epiweek is not None:
        mask = df.eval('epiweek=={}'.format(epiweek))
    else:
        mask = df.keys()

    df_alert = df[mask].copy().reset_index()

    # alert
    alert_col = df_alert.T.apply(get_season_level)
    df_alert = df_alert.assign(alert=alert_col)

    return df_alert
