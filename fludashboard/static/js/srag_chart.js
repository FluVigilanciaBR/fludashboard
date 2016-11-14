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
   * @constructs
   * @param {string} bindTo - DOM ID of the chart container (e.g. "#container").
   */
  constructor(bindTo) {
    this.bindTo = bindTo;
  }

  /**
   * Shows activity information about the criteria established on the chart.
   * @param {number} year - SRAG incidence year (e.g. 2013).
   * @param {number} week - SRAG incidence week (e.g. 2).
   * @param {string} stateName - Federal state name (e.g. "Acre").
   */
  displayInfo(year, week, stateName) {
    $.getJSON({
      url: '/data/incidence-levels/' + year + '/' + week + '/' +  stateName,
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
            data['l0'] == 1 ?
              'Baixa' : data['l1'] == 1 ?
              'Epidêmica' : data['l2'] == 1 ?
              'Alta' : data['l3'] == 1 ?
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
   * @param {number} year - SRAG incidence year (e.g. 2013).
   * @param {number} week - SRAG incidence week (e.g. 2).
   * @param {string} stateName- Federal state name (e.g. "Acre").
   * @return {object} - Chart object.
   */
  plot(year, week, stateName) {
    var _this = this;

    $(this.bindTo).empty();

    /*if (stateName == '') {
      return;
    }*/

    var chart = c3.generate({
      bindto: _this.bindTo,
      data: {
        url: './data/weekly-incidence-curve/' + year + '/' + stateName,
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
          estimated_cases: '#ff0000',
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
        }
        },
        y: {
        label: {
          text: 'Incidência (por 100 mil habitantes)',
          position: 'outer-middle'
        }
        },
      },
      regions: [
        {start:0, end:52, class: 'alert-red'}
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

    this.displayInfo(year, week, stateName);

    return chart;
  }
}

/**
 * SRAG Incidence Chart by Age
 * @class
 */
class SRAGAgeChart{
  /**
   * @constructs
   * @param {string} bindTo - DOM ID of the chart container (e.g. "#container").
   */
  constructor(bindTo) {
    this.bindTo = bindTo;
  }

  /**
   * Plots SRAG incidence chart by age
   * @param {number} year - SRAG incidence year.
   * @param {number} week - SRAG incidence week.
   * @param {string} stateName- Federal state name (e.g. "Acre").
   */
  plot(year, week, stateName) {
    var _this = this;

    $(this.bindTo).empty();

    /*if (stateName == '') {
      return;
    }*/

    return c3.generate({
      bindto: _this.bindTo,
      data: {
        url: './data/age-distribution/' + year + '/' +
          week + '/' + stateName,
        type: 'bar',
        names: {
          '0_4_anos': '0-4 anos',
          '5_9_anos': '5-9 anos',
          '10_19_anos': '10-19 anos',
          '20_29_anos': '20-29 anos',
          '30_39_anos': '30-39 anos',
          '40_49_anos': '40-49 anos',
          '50_59_anos': '50-59 anos',
          '60+_anos': '60+ anos'
        },
      },
      axis: {
        x: {
          label: {
            text: 'Faixa Etária',
            position: 'outer-center'
          },
          type: 'category',
          categories: [
            ''
          ]
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