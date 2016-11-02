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
    var _this = this;
    this.group_by = 'week'; // year or week
    // state or region
    this.delimitation = (
      $('input[name="radType[]"]:checked').attr('id') == 'radTypeState' ?
      'state' : 'region'
    );
    this.lastWeek = $('#week').val() || 0;
    this.sragData = {};

    // table
    this.sragTable = new SRAGTable();
    this.sragMap = new SRAGMap();
    this.sragIncidenceChart = new SRAGIncidenceChart(
      '#weekly-incidence-curve-chart'
    );

    this.sragAgeChart = new SRAGAgeChart(
      '#age-chart'
    );

    $('#year').change(function () {_this.load_graphs();});

    $('#btn-detailed').click(function(){
      $('#week').attr('min', 1);
      $('#week').val(_this.lastWeek);
      $('#div-week').removeClass('hidden');
      $('#btn-resumed').removeClass('selected');
      $('#btn-detailed').addClass('selected');
      $('.period-display').text('na semana epidemiológica');

      _this.changeWeek();
    });

    $('#btn-resumed').click(function(){
      $('#div-week').addClass('hidden');
      var _week = parseInt($('#week').val() || 0);

      if (_week > 0) {
        _this.lastWeek = _week;
      }

      $('#week').attr('min', 0);
      $('#week').val(0);
      $('#btn-detailed').removeClass('selected');
      $('#btn-resumed').addClass('selected');
      $('.period-display').text('no ano epidemiológico');

      _this.changeWeek();
    });

    d3.select('#week').on('change', function(){_this.changeWeek();});
    $('#week').on('input', function(){
      $('#week-display').val($('#week').val());
    });
    $('#week-display').change(function(){
      var _week = $('#week-display').val();

      if (!(_week >= 1 && _week <= 52)) {
        $('#week-display').val($('#week').val());
        return;
      }

      $('#week').val($('#week-display').val());
      _this.changeWeek();
    });

    $('#radTypeState').change(function(){
      $('#selected-state').val('');
      _this.load_graphs();
    });
    $('#radTypeRegion').change(function(){
      $('#selected-state').val('');
      _this.load_graphs();
    });
  }

  /**
   * start up the charts
   *
   */
  init() {
    this.load_graphs();
    $('.week-display').text($('#week').val() || 0);
  }

  /**
   * load data and build charts
   *
   */
  load_graphs() {
    var _this = this;

    var fn = function(error, statesBR, sragData){
      _this.sragData = sragData;
      _this.statesBR = statesBR;
      _this.makeGraphs(error);
    };

    var delimitation = (
      $('input[name="radType[]"]:checked').attr('id') == 'radTypeState' ?
      'state' : 'region'
    );

    queue()
      .defer(d3.json, 'static/data/br-states.json')
      .defer(d3.json, (
        '/data/incidence/' + ($('#year').val() || 0) + '/' + delimitation))
      .await(fn);
  }

  /**
   * When a week mark is changed, this function should update and trigger
   * some information and chart
   * @param {dict} sragData - srag data
   */
  changeWeek() {
    var _this = this;

    var week = parseInt($('#week').val() || 0);
    var year = parseInt($('#year').val() || 0);

    $('.week-display').text(week);

    var styleProperties = {
      fillColor: 'white',
      weight: 1
    };

    if(week>0) {
      var df = $.grep(_this.sragData, function(n,i){
          return n.epiweek==week
      });
    } else {
      $('.week-display').text('');
      var df = _this.sragData;
    }

    //print_filter(df);
    var stateName = $('#selected-state').val();

    _this.sragMap.changeColorMap(_this.sragData);
    _this.sragIncidenceChart.plot(year, week, stateName);
    _this.sragAgeChart.plot(year, week, stateName);
    _this.sragTable.makeTable(year, week, stateName);
  }

  /**
   *
   *
   */
  makeGraphs(error) {
    var stateName = $('#selected-state').val();
    var week = parseInt($('#week').val() || 0);
    var year = parseInt($('#year').val() || 0);
    var _this = this;

    this.sragMap.makeMap(
      this.statesBR, this.sragData, year, week,
      function(
        year, stateName, week
      ) {
        _this.sragIncidenceChart.plot(year, week, stateName);
        _this.sragAgeChart.plot(year, week, stateName);
        _this.sragTable.makeTable(year, week, stateName);
      }
    );

    this.changeWeek();

    /*if (stateName) {
      this.sragIncidenceChart.plot(year, week, stateName);
      this.sragAgeChart.plot(year, week, stateName);
    }*/

    this.sragIncidenceChart.plot(year, week, stateName);
    this.sragAgeChart.plot(year, week, stateName);
    this.sragTable.makeTable(year, week, stateName);
  }
}

dashboard = new Dashboard();

$(document).ready(function(){dashboard.init()});
