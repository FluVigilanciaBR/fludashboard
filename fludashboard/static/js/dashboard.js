/* -*- Mode: JavaScript; tab-width: 8; indent-tabs-mode: nil; c-basic-offset: 2 -*- */
/* vim: set ts=8 sts=2 et sw=2 tw=80: */
/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/** Dashboard class */
class Dashboard {
  constructor(
      userInterface, mapId
  ) {
    this.group_by = 'week'; // year or week
    this.separated_by = 'state'; // state or region

    // table
    this.sragTable = new SRAGTable();
    this.sragMap = new SRAGMap();
    this.sragChart = new SRAGChart('#weekly-incidence-curve-chart');

    $('#year').change(this.load_graphs);
  }

  /**
   * start up the charts
   *
   */
  init() {
    this.load_graphs();
    $('.week-display').text($('#week').val() || 0);
  }

  geoJsonURL() {
    if ($('#radTypeState').attr('checked')) {
      return 'static/data/br-states.json';
    } else {
      return 'static/data/br-regions.json';
    }
  }

  /**
   * load data and build charts
   *
   */
  load_graphs() {
    if ($('#radTypeState').attr('checked')) {
      var url = 'static/data/br-states.json';
    } else {
      var url = 'static/data/br-regions.json';
    }

    var _this = this;

    var fn = function(error, statesBR, sragData){
      _this.makeGraphs(error, statesBR, sragData);
    };

    queue()
      .defer(d3.json, url)
      .defer(d3.json, '/data/incidence/' + ($('#year').val() || 0))
      .await(fn);
  }


  /**
   * Plot incidence chart using
   * @param {number} year - year to filter the data
   * @param {string} state_name - state_name to filter the data
   * @param {number} week- week to filter the data
   */
  plot_incidence_chart(year, state_name, week) {
    if (state_name == '') {
      $('.chart-incidence').addClass('hidden');
      $('.weekly-incidence-curve-chart').empty();
      return;
    } else {
      $('.chart-incidence').removeClass('hidden');
    }

    SRAGChart.plot(
      '#weekly-incidence-curve-chart',
      year, state_name, week
    );
  }

  /**
   * Get the alert level color using the follow criteria:
   *
   * Red (level 4) if the incidence was above the high threshold for at
   *  least 5 weeks;
   * Orange (level 3) if above the high threshold from 1 to 4 weeks;
   * Yellow (level 2) if crossed the epidemic threshold but not the high one;
   * Green (level 1) if it did not cross the epidemic threshold.
   * @param {dict} d - total number of alert occurrence
   * @return {number} alert level
   */
  getAlertLevelForWholeYear(d) {
    if (d[4] >= 5) return 4;
    if (d[4] >= 1 && d[4] < 5) return 3;
    if (d[2] >= 1 || d[3] >= 1) return 2;
    return 1;
  }

  /**
   * When a week mark is changed, this function should update and trigger
   * some information and chart
   * @param {dict} sragData - srag data
   */
  changeWeek(sragData) {
    d3.select('#week').on('change', function(){
      var week = parseInt($('#week').val() || 0);
      var year = parseInt($('#year').val() || 0);

      $('.week-display').text(week);

      style_properties = {
        fillColor: 'white',
        weight: 1
      };

      if(week>0) {
        df = $.grep(sragData, function(n,i){
            return n.isoweek==week
        });
      } else {
        $("#linechart").addClass('hidden');
        $('.week-display').text('');
        df = sragData;
      }

      //print_filter(df);
      state_name = $('#selected-state').val();

      this.sragMap.changeColorMap(sragData);
      this.sragChart.plot(year, state_name, week);
      this.sragTable.makeTable(year, week, state_name);
    });
  }

  /**
   *
   *
   */
  makeGraphs(
    error, statesBR, sragData
  ) {
    var state_name = $('#selected-state').val();
    var week = parseInt($('#week').val() || 0);
    var year = parseInt($('#year').val() || 0);
    var _this = this;

    this.sragMap.makeMap(statesBR, sragData, year, week,
      function(
        year, stateName, week
      ) {
        _this.sragChart.plot(year, stateName, week);
        _this.sragTable.makeTable(year, week, stateName);
      }
    );
    this.changeWeek(sragData);

    if (state_name) {
      this.sragChart.plot(year, state_name, week);
    }

    this.sragTable.makeTable(year, week, state_name);
  }
}


dashboard = new Dashboard();

$(document).ready(function(){dashboard.init()});