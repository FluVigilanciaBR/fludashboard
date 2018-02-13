from unidecode import unidecode
# local
from ..settings import DATABASE

import pandas as pd
import sqlalchemy as sqla


# @deprecated
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


class FluDB:
    conn = None

    def __init__(self):
        dsn = 'postgresql://%(USER)s:%(PASSWORD)s@%(HOST)s/%(NAME)s'
        self.conn = sqla.create_engine(dsn % DATABASE)

    def get_territory_id_from_name(self, state_name: str) -> int:
        """

        :param state_name:
        :return:
        """

        state_name = state_name.upper()
        with self.conn.connect() as conn:
            sql = '''
            SELECT id FROM territory 
            WHERE UPPER(name)='%s'
            ''' % state_name

            result = conn.execute(sql).fetchone()

            if not result:
                raise Exception('State not found.')

            return result[0]

    def get_season_situation(self, df):
        """

        :param df:
        :return:
        """
        def _fn(se):
            return df[
                (df.territory_id == se.territory_id) &
                (df.epiyear == se.epiyear)
            ].situation_id.unique()[0]
        return _fn

    def get_season_level(self, se):
        """
        Generate season level code based on counts over weekly activity

        """
        if se.high_level + se.very_high_level > 4:
            return 4  # 'red'
        elif se.high_level + se.very_high_level >= 1:
            return 3  # 'orange'
        elif se.epidemic_level >= 1:
            return 2  # 'yellow'
        # else
        return 1  # 'green'

    def group_data_by_season(self, df, df_age_dist=None, season=None):
        """

        :param df:
        :param df_age_dist:
        :param season:
        :return:
        """
        level_dict = {
            'low_level': 'Baixa', 'epidemic_level': 'Epidêmica',
            'high_level': 'Alta', 'very_high_level': 'Muito alta'
        }
        season_basic_cols = [
            'territory_id', 'territory_name', 'epiyear', 'value'
        ]
        season_cols = season_basic_cols + [
            'territory_type_name', 'situation_id', 'situation_name', 'level'
        ]

        df['level'] = df[list(level_dict.keys())].idxmax(axis=1)

        df_tmp = df[season_cols].copy()

        situation = list(
            df_tmp[df_tmp.epiyear == season].situation_id.unique()
        )
        l_incomplete = [1, 2, 4]
        if set(l_incomplete).intersection(situation):
            # incomplete
            df_tmp.loc[df_tmp.epiyear == season, 'situation_id'] = 4
        else:
            # stable
            df_tmp.loc[df_tmp.epiyear == season, 'situation_id'] = 3

        if df_age_dist is not None:
            tgt_cols = ['territory_id', 'territory_name', 'epiyear', 'gender',
                        'value', 'years_lt_2', 'years_2_4', 'years_0_4', 'years_5_9', 'years_10_19',
                        'years_20_29', 'years_30_39', 'years_40_49', 'years_50_59',
                        'years_60_or_more']

            df_by_season = df_age_dist[tgt_cols].groupby([
                'territory_id', 'territory_name', 'epiyear', 'gender'
            ], as_index=False).sum()
        else:
            df_by_season = df_tmp[season_basic_cols].groupby(
                ['territory_id', 'territory_name', 'epiyear'],
                as_index=False
            ).sum()

        situations_id = {
            1: 'unknown',
            2: 'estimated',
            3: 'stable',
            4: 'incomplete'
        }

        df_by_season['situation_id'] = df_by_season.apply(
            self.get_season_situation(df_tmp), axis=1
        )

        df_by_season['situation_name'] = df_by_season['situation_id'].map(
            situations_id
        )

        df_by_season_level = pd.crosstab([
            df_tmp.territory_id, df_tmp.territory_name, df_tmp.epiyear
        ], df_tmp.level).reset_index()

        df_by_season_level.columns.name = None

        for lv in (
            'low_level', 'epidemic_level', 'high_level', 'very_high_level'
        ):
            if not lv in df_by_season_level.keys():
                df_by_season_level[lv] = 0

        df_by_season['level'] = df_by_season_level[
            list(level_dict.keys())
        ].apply(
            self.get_season_level, axis=1
        )

        df_by_season['epiweek'] = 0

        return df_by_season

    def report_incidence(self, x, situation, low=None, high=None):
        """
        original name: report_inc

        :param x:
        :param situation:
        :param low:
        :param high:
        :return:
        """
        if situation == 3:
            y = '%.2f' % x
        elif situation == 2:
            y = '%.2f [%.2f - %.2f]' % (x, low, high)
        else:
            y = '*%.2f' % x
        return y

    def read_data(
        self, table_name: str, dataset_id: int, scale_id: int,
        territory_id: int=None, year: int=None, week: int=None,
        base_year: int=None, base_week: int=None,
        historical_week: int=None, return_sql=False,
        extra_fields: list=None, selected_fields: list=None, **kwargs
    ):
        """

        :param table_name:
        :param dataset_id:
        :param scale_id:
        :param territory_id:
        :param year:
        :param week:
        :param base_year:
        :param base_week:
        :param historical_week:
        :param return_sql:
        :param extra_fields:
        :param selected_fields:
        :param kwargs:
        :return:

        """
        if selected_fields is None:
            # get all fields from the table
            sql = '''
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name   = '%s'
            ORDER BY ordinal_position
            ''' % table_name

            with self.conn.connect() as conn:
                selected_fields = conn.execute(sql).fetchall()

            selected_fields = [
                f[0] for f in selected_fields
                if f[0] not in ['dataset_id', 'scale_id']
            ]

        if extra_fields is not None:
            selected_fields += extra_fields

        sql_param = {
            'table_name': table_name,
            'dataset_id': dataset_id,
            'scale_id': scale_id,
            'fields': ','.join(selected_fields)
        }

        sql = '''
        SELECT %(fields)s, territory.name AS territory_name
        FROM %(table_name)s 
          INNER JOIN territory
            ON (%(table_name)s.territory_id = territory.id)
        WHERE dataset_id=%(dataset_id)s 
          AND scale_id=%(scale_id)s
        '''

        if territory_id is not None:
            sql += " AND territory_id=%(territory_id)s"
            sql_param['territory_id'] = territory_id

        if year is not None:
            sql += " AND epiyear=%(year)s"
            sql_param['year'] = year

        if base_year is not None:
            sql += " AND base_epiyear=%(base_year)s"
            sql_param['base_year'] = base_year

        if week is not None and week > 0:
            sql += " AND epiweek=%(week)s"
            sql_param['week'] = week
        elif base_week is not None:
            sql += " AND base_epiweek=%(base_week)s"
            sql_param['base_week'] = base_week
        elif historical_week is not None:
            sql += " AND epiweek<=%(historical_week)s"
            sql_param['historical_week'] = historical_week

        if return_sql:
            return sql % sql_param

        with self.conn.connect() as conn:
            return pd.read_sql(sql % sql_param, conn)

    def get_data(
        self, dataset_id: int, scale_id: int, year: int,
        territory_id: int=None, week: int=None,
        show_historical_weeks: bool=False,
        territory_type_id: int=None
    ):
        """

        :param dataset_id:
        :param scale_id:
        :param year:
        :param territory_id:
        :param week: 0 week == all weeks
        :param show_historical_weeks:
        :param territory_type_id:
        :return:
        """
        sql = '''
        SELECT
          mem_typical.dataset_id AS dataset_id,
          mem_typical.scale_id AS scale_id,
          mem_typical.territory_id AS territory_id,
          incidence.epiyear AS epiyear,
          mem_typical.epiweek AS epiweek,
          incidence.value, 
          incidence.low_level as low_level,
          incidence.epidemic_level as epidemic_level,
          incidence.high_level as high_level,
          incidence.very_high_level as very_high_level,
          incidence.situation_id AS situation_id,
          incidence.run_date,
          %(estimates_columns_selection)s
          mem_typical.population, 
          mem_typical.low AS typical_low, 
          mem_typical.median AS typical_median, 
          mem_typical.high AS typical_high,
          mem_report.geom_average_peak, 
          mem_report.low_activity_region, 
          mem_report.pre_epidemic_threshold as pre_epidemic_threshold, 
          mem_report.high_threshold as high_threshold, 
          mem_report.very_high_threshold as very_high_threshold, 
          mem_report.epi_start, 
          mem_report.epi_start_ci_lower,
          mem_report.epi_start_ci_upper, 
          mem_report.epi_duration, 
          mem_report.epi_duration_ci_lower, 
          mem_report.epi_duration_ci_upper,
          mem_report.regular_seasons,
          historical.base_epiyear, 
          historical.base_epiweek,
          territory.name AS territory_name,
          territory_type.name AS territory_type_name,
          situation.name AS situation_name
        FROM
          (
            SELECT
            epiyear,
            epiweek,
            dataset_id,
            scale_id,
            territory_id,
            situation_id,
            "value",
            low_level,
            epidemic_level,
            high_level,
            very_high_level,
            run_date 
            %(incidence_table_select)s
            FROM current_estimated_values
            WHERE dataset_id=%(dataset_id)s 
              AND scale_id=%(scale_id)s 
              AND epiyear=%(epiyear)s 
              AND epiweek %(incidence_week_operator)s %(epiweek)s
              %(territory_id_condition)s
              %(situation_id_condition)s
          ) AS incidence 
          INNER JOIN situation
            ON (incidence.situation_id=situation.id)
          FULL OUTER JOIN (
            SELECT * FROM mem_typical
            WHERE dataset_id=%(dataset_id)s 
              AND scale_id=%(scale_id)s
              %(territory_id_condition)s 
            ) AS mem_typical
            ON (
              incidence.dataset_id=mem_typical.dataset_id
              AND incidence.scale_id=mem_typical.scale_id
              AND incidence.territory_id=mem_typical.territory_id
              AND incidence.epiweek=mem_typical.epiweek
            )
          INNER JOIN territory
            ON (mem_typical.territory_id=territory.id)
          INNER JOIN territory_type
            ON (territory.territory_type_id=territory_type.id)
          %(historical_table)s
          FULL OUTER JOIN (
            SELECT * FROM mem_report
            WHERE dataset_id=%(dataset_id)s 
              AND scale_id=%(scale_id)s
              %(territory_id_condition)s
            ) AS mem_report
            ON (
              mem_typical.dataset_id=mem_report.dataset_id
              AND mem_typical.scale_id=mem_report.scale_id
              AND mem_typical.territory_id=mem_report.territory_id
              AND mem_typical.year=mem_report.year
            )
         WHERE 1=1
           %(where_extras)s
        ORDER BY epiyear, epiweek
        '''

        sql_param = {
            'dataset_id': dataset_id,
            'scale_id': scale_id,
            'territory_id': territory_id,
            'epiweek': week,
            'epiyear': year,
            'base_epiweek_condition': ' AND base_epiweek = %s' % week,
            'estimates_columns_selection': '''
            incidence.mean  AS "mean",
            incidence.median AS estimated_cases, 
            incidence.ci_lower AS ci_lower, 
            incidence.ci_upper AS ci_upper, 
            ''',
            'where_extras': '',
            'historical_table': '''
            FULL OUTER JOIN (
              SELECT * 
              FROM historical_estimated_values LIMIT 0
            ) AS historical ON (1=1)
            ''',
            'incidence_week_operator': '=',
            'territory_id_condition': '',
            'situation_id_condition': '',
            'incidence_table_select': ''' 
            ,mean,
            median,
            ci_lower,
            ci_upper
            '''

        }

        if territory_id is not None:
            sql_param['territory_id_condition'] += (
                ' AND territory_id=%s ' % territory_id
            )

        if week is None or week == 0:
            sql_param['epiweek'] = 54
            sql_param['incidence_week_operator'] = '<='
            sql_param['base_epiweek_condition'] = '''
            AND base_epiweek = (
                SELECT MAX(base_epiweek)
                FROM historical_estimated_values
                WHERE base_epiyear = %(epiyear)s\
                AND dataset_id = %(dataset_id)s
                AND scale_id = %(scale_id)s
                %(territory_id_condition)s )
            ''' % sql_param

        # force week filter (week 0 == all weeks)
        if show_historical_weeks:
            sql_param['situation_id_condition'] = ' AND situation_id = 3'
            sql_param['estimates_columns_selection'] = '''
            historical.mean  AS mean,
            historical.median AS estimated_cases, 
            historical.ci_lower AS ci_lower, 
            historical.ci_upper AS ci_upper, 
            '''
            sql_param['incidence_table_select'] = ''
            sql_param['historical_table'] = '''
          LEFT JOIN (
            SELECT territory_id,
                epiweek,
                mean,
                median,
                ci_lower,
                ci_upper,
                low_level,
                epidemic_level,
                high_level,
                very_high_level,
                base_epiyear,
                base_epiweek,
                base_epiyearweek
            FROM historical_estimated_values
            WHERE dataset_id=%(dataset_id)s 
             AND scale_id=%(scale_id)s 
             AND territory_id=%(territory_id)s 
             AND base_epiyear=%(epiyear)s
             AND situation_id = 2
             %(base_epiweek_condition)s
          ) AS historical
            ON (
              mem_typical.epiweek=historical.epiweek
            )
            ''' % sql_param
            sql_param['incidence_week_operator'] = '<='
        else:
            sql_param['where_extras'] += ' AND incidence.epiweek %s %s' % (
                sql_param['incidence_week_operator'], sql_param['epiweek']
            )

        if territory_type_id is not None and territory_type_id > 0:
            sql_param['where_extras'] += (
                ' AND territory.territory_type_id=%s' % territory_type_id
            )

        sql = sql % sql_param

        with self.conn.connect() as conn:
            return pd.read_sql(sql, conn)

    def get_data_age_sex(
        self, dataset_id: int, scale_id: int, year: int,
        territory_id: int=0, week: int=0
    ):
        """

        :param dataset_id:
        :param scale_id:
        :param year:
        :param territory_id:
        :param week:
        :return:

        """
        season = year  # alias

        if scale_id == 1:
            age_cols = ['years_0_4']
        else:
            age_cols = ['years_lt_2', 'years_2_4']

        age_cols.extend([
            'years_5_9', 'years_10_19', 'years_20_29',
            'years_30_39', 'years_40_49', 'years_50_59', 'years_60_or_more'
        ])

        # data
        df_age_dist = self.read_data(
            'clean_data_epiweek_weekly_incidence_w_situation',
            dataset_id=dataset_id, scale_id=scale_id, year=season,
            territory_id=territory_id,
            low_memory=False
        )

        if week is not None and week > 0:
            df_age_dist = df_age_dist[df_age_dist.epiweek == week]
            df = df_age_dist
        else:
            df = self.get_data(
                dataset_id=dataset_id, scale_id=scale_id,
                year=year, territory_id=territory_id
            )
            df = self.group_data_by_season(
                df=df, df_age_dist=df_age_dist, season=season
            )

        df = df[age_cols + ['gender']].set_index('gender').transpose()
        df.rename(columns={'F': 'Mulheres', 'M': 'Homens'}, inplace=True)
        if 'I' in df.columns:
            df.rename(columns={'I': 'Sexo ignorado'}, inplace=True)
            df = df[['Mulheres', 'Homens', 'Sexo ignorado', 'Total']]

        return df
