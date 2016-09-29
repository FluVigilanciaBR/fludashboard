
def apply_filter_alert_by_isoweek(
    df, year=2013, isoweek=None, verbose=False
):
    """
    """
    if isoweek is not None:
        mask = df.eval('isoweek=={}'.format(isoweek))
    else:
        mask = df.keys()

    df_alert = df[mask].reset_index()
    df_alert = df_alert.assign(incidence=df['SRAG{}'.format(year)])
    
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
    
    return df_alert
