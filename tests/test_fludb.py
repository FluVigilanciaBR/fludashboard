#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_fludashboard
----------------------------------

Tests for `fludashboard` module.

"""
# local
from fludashboard.libs.flu_data import FluDB

import unittest
import pandas as pd


class TestFluDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fludb = FluDB()

    def tearDown(self):
        pass

    def test_get_territory_id_from_name(self):
        territory_id = self.fludb.get_territory_id_from_name('Rio de Janeiro')
        assert territory_id == 33

        territory_id = self.fludb.get_territory_id_from_name('SÃO PAULO')
        assert territory_id == 35

    def test_read_data(self):
        df = self.fludb.read_data(
            table_name='current_estimated_values',
            dataset_id=1, scale_id=1, territory_id=33,
            year=2017, week=25, base_year=None, base_week=None,
            historical_week=None
        )

        assert not df.empty
        assert df.loc[0, 'epiyear'] == 2017
        assert df.loc[0, 'epiweek'] == 25
        assert df.loc[0, 'territory_id'] == 33

    def test_get_data(self):
        df = self.fludb.get_data(
            dataset_id=1, scale_id=1, year=2017,
            territory_id=33, week=25, show_historical_weeks=True
        )

        # pandas configuration
        pd.set_option('display.max_columns', 99)
        assert not df.empty


if __name__ == '__main__':
    unittest.main()
