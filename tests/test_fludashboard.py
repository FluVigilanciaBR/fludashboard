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
PATH_ROOT = os.path.dirname(os.getcwd())

if 'data' in os.listdir(PATH_ROOT):
    sys.path.insert(0, PATH_ROOT)
    os.chdir(PATH_ROOT)
else:
    os.chdir(os.path.join(PATH_ROOT, 'fludashboard', 'fludashboard'))
    sys.path.insert(0, os.getcwd())

from fludashboard.app import app
from contextlib import contextmanager


class TestFludashboard(unittest.TestCase):

    def setUp(self):
        print('S'*100)
        print(os.getcwd())

        if 'data' in os.listdir(PATH_ROOT):
            os.chdir(PATH_ROOT)
            sys.path.insert(0, PATH_ROOT)
        else:
            os.chdir(os.path.join(PATH_ROOT, 'fludashboard', 'fludashboard'))
            sys.path.insert(0, os.getcwd())

        self.app = app

    def tearDown(self):
        pass

    def test_index(self):
        print(os.getcwd())
        with self.app.test_client() as c:
            print('I'*100)
            print(os.getcwd())
            resp = c.get('/')
            assert resp._status_code == 200

    def test_get_incidence_data(self):
        with self.app.test_client() as c:
            # /data/incidence/<int:year>/<string:territory_type>'
            resp = c.get('/data/incidence/2015/Acre')
            assert resp._status_code == 200

    def data__weekly_incidence_curve(self):
        with self.app.test_client() as c:
            # '/data/weekly-incidence-curve/<int:year>/'
            resp = c.get('/data/weekly-incidence-curve/2015/')
            assert resp._status_code == 200

            # /data/weekly-incidence-curve/<int:year>/<string:state>
            resp = c.get('/data/weekly-incidence-curve/2015/Acre')
            assert resp._status_code == 200

    def test_data__incidence_levels(self):
        with self.app.test_client() as c:
            # /data/incidence-levels/<int:year>
            resp = c.get('/data/incidence-levels/2015')
            assert resp._status_code == 200

            # /data/incidence-levels/<int:year>/<int:epiweek>/
            resp = c.get('/data/incidence-levels/2015/25/')
            assert resp._status_code == 200

            # /data/incidence-levels/<int:year>/<int:epiweek>/
            # <string:state_name>
            resp = c.get('/data/incidence-levels/2015/25/Acre')
            assert resp._status_code == 200

    def test_data__data_table(self):
        with self.app.test_client() as c:
            # /data/data-table/<int:year>
            resp = c.get('/data/data-table/2015')
            assert resp._status_code == 200

            # /data/data-table/<int:year>/<int:epiweek>
            resp = c.get('/data/data-table/2015/25')
            assert resp._status_code == 200

            # /data/data-table/<int:year>/<int:epiweek>/<string:territory_type>
            resp = c.get('/data/data-table/2015/25/state')
            assert resp._status_code == 200

            resp = c.get('/data/data-table/2015/25/region')
            assert resp._status_code == 200

            # /data/data-table/<int:year>/<int:epiweek>/<string:territory_type>/
            # <string:state_name>
            resp = c.get('/data/data-table/2015/25/state/Acre')
            assert resp._status_code == 200

            resp = c.get('/data/data-table/2015/25/region/Região Central')
            assert resp._status_code == 200

    def test_data__age_distribution(self):
        with self.app.test_client() as c:
            # /data/age-distribution/<int:year>/
            resp = c.get('/data/age-distribution/2015/')
            assert resp._status_code == 200

            # /data/age-distribution/<int:year>/<int:week>/
            resp = c.get('/data/age-distribution/2015/25/')
            assert resp._status_code == 200

            # /data/age-distribution/<int:year>/<int:week>/<string:state>
            resp = c.get('/data/age-distribution/2015/25/Acre')
            assert resp._status_code == 200


if __name__ == '__main__':
    unittest.main()
