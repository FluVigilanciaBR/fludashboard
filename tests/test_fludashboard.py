#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_fludashboard
----------------------------------

Tests for `fludashboard` module.
"""
import flask
import os
import sys
import unittest

# local
sys.path.insert(0, os.path.dirname(os.getcwd()))
from fludashboard.app import app
from contextlib import contextmanager


class TestFludashboard(unittest.TestCase):

    def setUp(self):
        self.app = app

    def tearDown(self):
        pass

    def test_index(self):
        with self.app.test_client() as c:
            resp = c.get('/')
            assert resp._status_code in [400, 200, 304]

    def test_get_incidence_data(self):
        with self.app.test_client() as c:
            # /data/incidence/<int:year>/<string:territory_type>'
            resp = c.get('/data/incidence/2015/Acre')
            assert resp._status_code in [400, 200, 304]

    def data__weekly_incidence_curve(self):
        with self.app.test_client() as c:
            # '/data/weekly-incidence-curve/<int:year>/'
            resp = c.get('/data/weekly-incidence-curve/2015/')
            assert resp._status_code in [400, 200, 304]

            # /data/weekly-incidence-curve/<int:year>/<string:state>
            resp = c.get('/data/weekly-incidence-curve/2015/Acre')
            assert resp._status_code in [400, 200, 304]

    def test_data__incidence_levels(self):
        with self.app.test_client() as c:
            # /data/incidence-levels/<int:year>
            resp = c.get('/data/incidence-levels/2015')
            assert resp._status_code in [400, 200, 304]

            # /data/incidence-levels/<int:year>/<int:epiweek>/
            resp = c.get('/data/incidence-levels/2015/25/')
            assert resp._status_code in [400, 200, 304]

            # /data/incidence-levels/<int:year>/<int:epiweek>/
            # <string:state_name>
            resp = c.get('/data/incidence-levels/2015/25/Acre')
            assert resp._status_code in [400, 200, 304]

    def test_data__data_table(self):
        with self.app.test_client() as c:
            # /data/data-table/<int:year>
            resp = c.get('/data/data-table/2015')
            assert resp._status_code in [400, 200, 304]

            # /data/data-table/<int:year>/<int:epiweek>
            resp = c.get('/data/data-table/2015/25')
            assert resp._status_code in [400, 200, 304]

            # /data/data-table/<int:year>/<int:epiweek>/<string:territory_type>
            resp = c.get('/data/data-table/2015/25/state')
            assert resp._status_code in [400, 200, 304]

            resp = c.get('/data/data-table/2015/25/region')
            assert resp._status_code in [400, 200, 304]

            # /data/data-table/<int:year>/<int:epiweek>/<string:territory_type>/
            # <string:state_name>
            resp = c.get('/data/data-table/2015/25/state/Acre')
            assert resp._status_code in [400, 200, 304]

            resp = c.get('/data/data-table/2015/25/region/Região Central')
            assert resp._status_code in [400, 200, 304]

    @unittest.SkipTest
    def test_data__age_distribution(self):
        with self.app.test_client() as c:
            # /data/age-distribution/<int:year>/
            resp = c.get('/data/age-distribution/2015')
            assert resp._status_code in [400, 200, 304]

            # /data/age-distribution/<int:year>/<int:week>/
            resp = c.get('/data/age-distribution/2015/25/')
            assert resp._status_code in [400, 200, 304]

            # /data/age-distribution/<int:year>/<int:week>/<string:state>
            resp = c.get('/data/age-distribution/2015/25/Acre')
            assert resp._status_code in [400, 200, 304]


if __name__ == '__main__':
    unittest.main()