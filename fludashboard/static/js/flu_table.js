/* -*- Mode: JavaScript; tab-width: 8; indent-tabs-mode: nil; c-basic-offset: 2 -*- */
/* vim: set ts=8 sts=2 et sw=2 tw=80: */
/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/**
 * SRAGTable allows create data table with SRAG data dynamically.
 * @property {object} dataTable - DataTable object.
 */
class SRAGTable {
  /**
   */
  constructor(){
    $('#divTable').html(this.getDataTableContent());
    this.dataTable = $('#data-table').DataTable({
      "autoWidth": false
    });
  }

  /**
   * Returns HTML table that will be created.
   * @returns {string}
   */
  getDataTableContent(scale) {
    var label = (
        scale == 'incidence' ?
        'Incidência (por 100 mil habitantes)' :
        'Número de casos'
    );

    return  '' +
      '<table id="data-table" ' +
      '  class="display table table-striped table-condensed">' +
      '  <!-- create a custom header -->' +
      '  <thead class="header">' +
      '    <tr class="header">' +
      '      <th>Unidade da Federa&ccedil;&atilde;o</th>' +
      '      <th>Situa&ccedil;&atilde;o</th>' +
      '      <th>' + label + '</th>' +
      '    </tr>' +
      '  </thead>' +
      '</table>';
  }

  /**
   * Builds the SRAG incidence table.
   * @param {string} dataset - dataset
   * @param {string} scale - data scale
   * @param {number} year - SRAG incidence year (e.g. 2013).
   * @param {number} week - SRAG incidence week (e.g. 2).
   * @param {string} stateName - Federal state name (e.g. "Acre").
   */
  makeTable(dataset, scale, year, week, stateName) {
    var columns = [];
    var _tmp = '';
    var territoryType = (
      $('input[name="radType[]"]:checked').attr('id') == 'radTypeState' ?
      'state' : 'region'
    );
    var tableSettings = {
      "dom": 'Bfrt',
      "language": {
        "url": "/static/libs/datatables/i18n/Portuguese-Brasil.json"
      },
      "buttons": [
        'excelHtml5',
        'csvHtml5'
      ],
      "paging": false,
      //"pageLength": 100,
      "fixedColumns": true,
      "ordering": false
    };

    tableSettings['columnDefs'] = [{width: '50%', targets: 1}];

    var _tmp = territoryType;

    if (stateName) {
      _tmp = _tmp + '/' + stateName;
    }

    var url = [
        '.', 'data', dataset, scale, year, week, _tmp, 'data-table'
    ].join('/');

    tableSettings['ajax'] = url;
    tableSettings['columns'] = [
      {'data': 'unidade_da_federacao'},
      {'data': 'situation'},
      {'data': 'srag'}
    ];
    tableSettings["autoWidth"] = false;

    // title
    if (scale == 'incidence') {
        $('#table-incidence-case-title').text('Incidência');
    } else {
        $('#table-incidence-case-title').text('Número de casos');
    }

    // create new table
    $('#divTable').html(this.getDataTableContent(scale));
    this.dataTable = $('#data-table').DataTable(tableSettings);
  }
}