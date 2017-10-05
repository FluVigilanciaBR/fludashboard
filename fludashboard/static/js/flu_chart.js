/* -*- Mode: JavaScript; tab-width: 8; indent-tabs-mode: nil;
   c-basic-offset: 2 -*- */
/* vim: set ts=8 sts=2 et sw=2 tw=80: */
/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/**
 * SRAGIncidenceChart is used to show Incidence Flu Chart.
  */
class SRAGIncidenceChart{
  /**
   * @param {string} bindTo - DOM ID of the chart container (e.g. "#container").
   * @param {dict} lastWeekYears- Dictionary with the last week of each
      available year (e.g. {2015: 53, 2016: 52}).
   */
  constructor(bindTo, lastWeekYears) {
    this.bindTo = bindTo;
    this.lastWeekYears = lastWeekYears;
  }

  /**
   * Shows activity information about the criteria established on the chart.
   * @param {string} dataset - dataset
   * @param {string} scale - data scale
   * @param {number} year - SRAG incidence year (e.g. 2013).
   * @param {number} week - SRAG incidence week (e.g. 2).
   * @param {string} stateName - Federal state name (e.g. "Acre").
   */
  displayInfo(dataset, scale, year, week, stateName) {
    var url = [
        '.', 'data', dataset, scale, year, week, stateName, 'levels'
    ].join('/');

    $.getJSON({
      url: url,
      success: function(d) {
        // hidden  all
        var _prob = $('#chart-incidence-activity-level-panel .prob');
        var _level = $('#chart-incidence-activity-level-panel .level');

        if (!_prob.hasClass('hidden')) {
          _prob.addClass('hidden');
        }

        if (!_level.hasClass('hidden')) {
          _level.addClass('hidden');
        }

        // if no data returned
        if (d.length <1) {
          return;
        }

        var data = d[0];

        if (data['situation'] == 'stable') {
          $('.classification', _level).text(
            data['l0'] == 100 ?
              'Baixa' : data['l1'] == 100 ?
              'Epidêmica' : data['l2'] == 100 ?
              'Alta' : data['l3'] == 100 ?
              'Muito Alta' : '(Não encontrada.)'
          );
          _level.removeClass('hidden');
        } else {
          $('.low', _prob).text(data['l0']);
          $('.epidemic', _prob).text(data['l1']);
          $('.high', _prob).text(data['l2']);
          $('.very-high', _prob).text(data['l3']);
          _prob.removeClass('hidden');
        }
      }
    });
  }

  /**
   * Plots SRAG incidence chart
   * @param {string} dataset - dataset
   * @param {string} scale - data scale
   * @param {number} year - SRAG incidence year (e.g. 2013).
   * @param {number} week - SRAG incidence week (e.g. 2).
   * @param {string} stateName- Federal state name (e.g. "Acre").
   * @return {object} - Chart object.
   */
  plot(dataset, scale, year, week, stateName) {
    var _this = this;
    var url = [
        '.', 'data', dataset, scale, year,
        stateName, 'weekly-incidence-curve'
    ].join('/');

    $(this.bindTo).empty();

    /*if (stateName == '') {
      return;
    }*/

    var chart = c3.generate({
      bindto: _this.bindTo,
      data: {
        url: url,
        x: 'epiweek',
        names: {
          corredor_baixo: null,
          corredor_mediano: null,
          corredor_alto: null,
          srag: 'Casos notificados',
          limiar_pre_epidemico: 'Limiar Pré epidêmico',
          intensidade_alta: 'Intensidade Alta',
          intensidade_muito_alta: 'Intensidade Muito Alta',
          estimated_cases: 'Casos estimados',
          ci_lower: 'Intervalo de confiança (2,5%)',
          ci_upper: 'Intervalo de confiança (97,5%)',
          incomplete_data: 'Dados Incompletos'
        },
        types: {
          corredor_baixo: 'area',
          corredor_mediano: 'area',
          corredor_alto: 'area',
          srag: 'line',
          limiar_pre_epidemico: 'line',
          intensidade_alta: 'line',
          intensidade_muito_alta: 'line'
        },
        colors: {
          corredor_baixo: '#00ff00',
          corredor_mediano: '#ffff00',
          corredor_alto: '#ff9900',
          srag: '#000000',
          limiar_pre_epidemico: '#0000ff',
          intensidade_alta: '#00ff00',
          intensidade_muito_alta: '#ff0000',
          estimated_cases: '#ff9900',
          ci_lower: '#ff0000',
          ci_upper: '#ff0000',
          incomplete_data: '#ff0000',
        }
      },
      axis: {
        x: {
          label: {
            text: 'SE',
            position: 'outer-center'
          },
          tick: {
            values: d3.range(1, _this.lastWeekYears[year], 2)
          },
          min: 1,
          max:_this.lastWeekYears[year]
        },
        y: {
        label: {
          text: 'Incidência (por 100 mil habitantes)',
          position: 'outer-middle'
        }
        },
      },
      regions: [
        {start: 1, end: _this.lastWeekYears[year], class: 'alert-red'}
      ],
      grid: {
        x: {
         lines: [
          {value: week, text: 'Semana Selecionada', position: 'middle'}
        ], show: false
        },
        y: {show: true}
      },
      zoom: {
        enabled: true
      },/*
      subchart: {
        show: true
      },*/
      tooltip: {
        show: false
      },
      point: {
        show: false
      }
    });

    this.displayInfo(dataset, scale, year, week, stateName);

    return chart;
  }
}

/**
 * SRAG Incidence Chart by Age
 * @class
 */
class SRAGAgeChart{
  /**
   * @param {string} bindTo - DOM ID of the chart container (e.g. "#container").
   */
  constructor(bindTo) {
    this.bindTo = bindTo;
  }

  /**
   * Plots SRAG incidence chart by age
   * @param {string} dataset - dataset
   * @param {string} scale - data scale
   * @param {number} year - SRAG incidence year.
   * @param {number} week - SRAG incidence week.
   * @param {string} stateName- Federal state name (e.g. "Acre").
   */
  plot(dataset, scale, year, week, stateName) {
    var _this = this;
    var url = [
        '.', 'data', dataset, scale, year, week,
        stateName, 'age-distribution'
    ].join('/');

    $(this.bindTo).empty();

    /*if (stateName == '') {
      return;
    }*/

    return c3.generate({
      bindto: _this.bindTo,
      data: {
        url: url,
        x: 'index',
        type: 'bar'
      },
      axis: {
        x: {
          label: {
            text: 'Faixa Etária',
            position: 'outer-center'
          },
          type: 'category',

        },
        y: {
          label: {
            text: 'Incidência (por 100 mil habitantes)',
            position: 'outer-middle'
          }
        },
      },
      grid: {
        x: { show: false },
        y: {show: true }
      },
    });
  }
}