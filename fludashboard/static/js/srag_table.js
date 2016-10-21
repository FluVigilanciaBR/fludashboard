/* -*- Mode: JavaScript; tab-width: 8; indent-tabs-mode: nil; c-basic-offset: 2 -*- */
/* vim: set ts=8 sts=2 et sw=2 tw=80: */
/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/**
 *
 *
 */
class SRAGTable {
  constructor(){
    $('#divTable').html(this.getDataTableContent());
    this.dataTable = $('#data-table').DataTable();
  }

  getDataTableContent() {
    return  '' +
      '<table id="data-table" ' +
      '  class="display table table-striped table-condensed">' +
      '  <!-- create a custom header -->' +
      '  <thead class="header">' +
      '    <tr class="header">' +
      '      <th>Unidade da Federa&ccedil;&atilde;o</th>' +
      '      <th>Incidência (por 100 mil habitantes)</th>' +
      '    </tr>' +
      '  </thead>' +
      '</table>';
  }

  makeTable(year, week, stateName) {
    var columns = [];
    var _tmp = '';
    var tableSettings = {
      "dom": 'Bfrtip',
      "language": {
        "url": "/static/libs/datatables/i18n/Portuguese-Brasil.json"
      },
      "buttons": [
        'excelHtml5',
        'csvHtml5'
      ],
      "pageLength": 10
    };

    if(week>0) {
      $("#data-table").removeClass('hidden');
    } else {
      $("#data-table").addClass('hidden');
    }

    tableSettings['columnDefs'] = [];

    if (stateName) {
      var _tmp = '/' + stateName;
      tableSettings['columnDefs'].push({
        "targets": [ 0 ],
        "visible": false,
        "searchable": false
      });
    }

    tableSettings['ajax'] = '/data/data-table/' + year + '/' + week + _tmp;
    tableSettings['columns'] = [
      {'data': 'unidade_da_federacao'},
      {'data': 'srag'}
    ];

    // destroy old table
    //this.dataTable.empty(); // empty in case the columns change
    //this.dataTable.destroy();

    // create new table
    $('#divTable').html(this.getDataTableContent());
    this.dataTable = $('#data-table').DataTable(tableSettings);
  }
}