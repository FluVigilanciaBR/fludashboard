"""


"""


def calc_alert_rank(se):
    """

    :param se: pd.Series
    :return: int
    """
    _max = max([se.l3, se.l2, se.l1, se.l0])

    return (
        1 if se.l0 == _max else
        2 if se.l1 == _max else
        3 if se.l2 == _max else
        4
    )


def calc_alert_rank_whole_year(se):
    """
    calculate the alert rank for the whole year

    :param se: pd.Series
    :return:
    """
    high_threshold = se.l3 + se.l2

    return (
        4 if high_threshold >= 5 else
        3 if high_threshold > 1 else
        2 if se.l1 >= 1 else
        1
    )


def apply_filter_alert_by_epiweek(
        df, epiweek=None, verbose=False
):
    """
    """
    if epiweek is not None:
        mask = df.eval('epiweek=={}'.format(epiweek))
    else:
        mask = df.keys()

    df_alert = df[mask].copy().reset_index()

    # alert
    alert_col = df_alert.T.apply(calc_alert_rank)
    df_alert = df_alert.assign(alert=alert_col)

    return df_alert
