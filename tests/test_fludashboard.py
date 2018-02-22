#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_fludashboard
----------------------------------

Tests for `fludashboard` module.

"""
# local
from fludashboard.app import app
from fludashboard.libs.migration import update_data_files

import os
import unittest


class TestFludashboard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # /data/<data_source>/<scale>
        cls.url = '/data/1/1/'
        cls.app = app
        # get data when necessary
        update_data_files(update_data=False)

    def tearDown(self):
        pass

    def test_index(self):
        with self.app.test_client() as c:
            resp = c.get('/')
            assert resp._status_code == 200

    def test_get_incidence_data(self):
        with self.app.test_client() as c:
            # /data/<string:dataset>/<string:scale>/<int:year>/
            # <int:territory_type_id>
            resp = c.get(self.url + '2015/2')
            assert resp._status_code == 200

    def data__weekly_incidence_curve(self):
        with self.app.test_client() as c:
            # /data/<string:dataset>/<string:scale>/<int:year>/
            # weekly-incidence-curve
            resp = c.get(self.url + '2015/weekly-incidence-curve')
            assert resp._status_code == 200

            # /data/<string:dataset>/<string:scale>/<int:year>
            # /<string:territory_id>/weekly-incidence-curve
            resp = c.get(self.url + '2015/Acre/weekly-incidence-curve')
            assert resp._status_code == 200

    def test_data__incidence_levels(self):
        with self.app.test_client() as c:
            # /data/<string:dataset>/<string:scale>/<int:year>/levels
            resp = c.get(self.url + '2015/levels')
            assert resp._status_code == 200

            # /data/<string:dataset>/<string:scale>/<int:year>/<int:epiweek>/
            # levels
            resp = c.get(self.url + '2015/25/levels')
            assert resp._status_code == 200

            # /data/<string:dataset>/<string:scale>/<int:year>/<int:epiweek>/
            # <string:state_name>/levels
            resp = c.get(self.url + '2015/25/Acre/levels')
            assert resp._status_code == 200

    def test_data__data_table(self):
        with self.app.test_client() as c:
            # /data/<string:dataset>/<string:scale>/<int:year>/data-table
            resp = c.get(self.url + '2015/data-table')
            assert resp._status_code == 200

            # /data/<string:dataset>/<string:scale>/<int:year>/<int:epiweek>/
            # data-table
            resp = c.get(self.url + '2015/25/data-table')
            assert resp._status_code == 200

            # /data/<string:dataset>/<string:scale>/<int:year>/<int:epiweek>/
            # <string:territory_type>/data-table
            resp = c.get(self.url + '2015/25/1/data-table')
            assert resp._status_code == 200

            resp = c.get(self.url + '2015/25/2/data-table')
            assert resp._status_code == 200

            # /data/<string:dataset>/<string:scale>/<int:year>/<int:epiweek>/
            # <string:territory_type>/<string:state_name>/data-table
            resp = c.get(self.url + '2015/25/1/Acre/data-table')
            assert resp._status_code == 200

            resp = c.get(self.url + '2015/25/2/Regional Centro/data-table')
            assert resp._status_code == 200

    def test_data__age_distribution(self):
        with self.app.test_client() as c:
            # /data/<string:dataset>/<string:scale>/<int:year>/age-distribution
            resp = c.get(self.url + '2015/age-distribution')
            print(resp._status_code)
            assert resp._status_code == 200

            # /data/<string:dataset>/<string:scale>/<int:year>/<int:week>/
            # age-distribution
            resp = c.get(self.url + '2015/25/age-distribution')
            assert resp._status_code == 200

            # /data/<string:dataset>/<string:scale>/<int:year>/<int:week>/
            # <string:state>/age-distribution
            resp = c.get(self.url + '2015/25/Acre/age-distribution')
            assert resp._status_code == 200


if __name__ == '__main__':
    unittest.main()
