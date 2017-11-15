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
        if se.high + se.very_high > 4:
            return 4  # 'red'
        elif se.high + se.very_high >= 1:
            return 3  # 'orange'
        elif se.epidemic >= 1:
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
            'low': 'Baixa', 'epidemic': 'Epidêmica',
            'high': 'Alta', 'very_high': 'Muito alta'
        }
        season_basic_cols = [
            'territory_id', 'unidade_da_federacao', 'epiyear', 'value'
        ]
        season_cols = season_basic_cols + ['tipo', 'situation_id', 'level']

        df['level'] = df[list(level_dict.keys())].idxmax(axis=1)

        df_tmp = df[season_cols].copy()

        situation = list(
            df_tmp[df_tmp.epiyear == season].situation_id.unique()
        )
        l_incomplete = [1, 2, 'incomplete', 'Incompleto']
        if set(l_incomplete).intersection(situation):
            df_tmp.loc[df_tmp.epiyear == season, 'situation_id'] = 'incomplete'
        else:
            df_tmp.loc[df_tmp.epiyear == season, 'situation_id'] = 3

        if df_age_dist is not None:
            df_by_season = df_age_dist[[
                'territory_id', 'unidade_da_federacao', 'epiyear', 'sexo',
                'value', '0_4_anos', '5_9_anos', '10_19_anos', '20_29_anos',
                '30_39_anos', '40_49_anos', '50_59_anos', '60+_anos'
            ]].groupby([
                'territory_id', 'unidade_da_federacao', 'epiyear', 'sexo'
            ], as_index=False).sum()
        else:
            df_by_season = df_tmp[season_basic_cols].groupby(
                ['territory_id', 'unidade_da_federacao', 'epiyear'],
                as_index=False
            ).sum()

        df_by_season['situation_id'] = df_by_season.apply(
            self.get_season_situation(df_tmp), axis=1
        )

        df_by_season_level = pd.crosstab([
            df_tmp.territory_id, df_tmp.unidade_da_federacao, df_tmp.epiyear
        ], df_tmp.level).reset_index()

        df_by_season_level.columns.name = None

        for i in range(4):
            _l = ('l%s' % i)
            if not _l in df_by_season_level.keys():
                df_by_season_level[_l] = 0

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
        SELECT %(fields)s FROM %(table_name)s 
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
        territory_id: int=None, week: int=None, historical_week: int=None,
        territory_type_id: int=None
    ):
        """

        :param dataset_id:
        :param scale_id:
        :param year:
        :param territory_id:
        :param week: 0 week == all weeks
        :param historical_week:
        :param territory_type_id:
        :return:
        """
        settings = {
            'dataset_id': dataset_id,
            'scale_id': scale_id,
            'territory_id': territory_id
        }

        sql_incidence = self.read_data(
            'current_estimated_values', **settings,
            year=year, week=week, historical_week=historical_week,
            return_sql=True
        )
        sql_typical_param = {
           'extra_fields': ['%s AS epiyear' % year]
        } if year is not None else {}
        sql_typical = self.read_data(
            'mem_typical', **settings,
            **sql_typical_param,
            return_sql=True
        )
        sql_thresholds = self.read_data(
            'mem_report', **settings, return_sql=True
        )

        # First, last keep only stable weeks for notification curve:
        # df_incidence.loc[(df_incidence.situation_id != 3), 'value'] = np.nan
        sql_incidence = sql_incidence.replace(
            ',value', ''',
            (CASE 
             WHEN situation_id <> 3 THEN NULL
             ELSE value 
             END) AS value
            '''
        )

        if historical_week is not None and historical_week > 0:
            historical_fields = [
                'epiweek', 'median AS estimated_cases',
                'ci_lower', 'ci_upper'
            ]
            sql_incidence = sql_incidence\
                .replace(',median AS estimated_cases', '')\
                .replace(',ci_lower', '')\
                .replace(',ci_upper', '')

            sql_historical = self.read_data(
                'historical_estimated_values', **settings,
                year=year, week=week, base_week=historical_week,
                selected_fields=historical_fields,
                return_sql=True
            )

            sql_historical = '''
            FULL OUTER JOIN (%s) AS historical
              ON (incidence.epiweek=historical.epiweek)
            ''' % sql_historical
        else:
            sql_historical = ''
            sql_incidence = sql_incidence.replace(
                ',median', ',median AS estimated_cases'
            )

        sql = '''
        SELECT *
        FROM 
          (%s) AS incidence
          FULL OUTER JOIN territory
            ON (incidence.territory_id=territory.id)
          FULL OUTER JOIN (%s) AS typical
            ON (incidence.territory_id=typical.territory_id
                AND incidence.epiweek=typical.epiweek)
          FULL OUTER JOIN (%s) AS thresholds
            ON (incidence.territory_id=thresholds.territory_id)
          %s
        ''' % (sql_incidence, sql_typical, sql_thresholds, sql_historical)

        sql += ' WHERE 1=1 '

        # force week filter (week 0 == all weeks)
        if week is not None and week > 0:
            sql += ' AND incidence.epiweek=%s' % week

        if territory_type_id is not None and territory_type_id > 0:
            sql += ' AND territory_type_id=%s' % territory_type_id

        sql += ' ORDER BY incidence.epiweek'

        with self.conn.connect() as conn:
            df = pd.read_sql(sql, conn)

        return df.T.drop_duplicates().T

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

        age_cols = [
            '0_4_anos', '5_9_anos', '10_19_anos', '20_29_anos', '30_39_anos',
            '40_49_anos', '50_59_anos', '60+_anos'
        ]

        # data
        df_age_dist = self.read_data(
            'clean_data_epiweek-weekly-incidence_w_situation',
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

        df = df[age_cols + ['sexo']].set_index('sexo').transpose()
        df.rename(columns={'F': 'Mulheres', 'M': 'Homens'}, inplace=True)

        return df
