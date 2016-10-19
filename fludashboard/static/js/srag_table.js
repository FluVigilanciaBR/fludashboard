/**
 *
 *
 */
function makeTable(year, week, state_name, ui) {
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

    tableSettings['columnDefs'] = [];

    if (stateName) {
        _tmp = '/' + state_name;
        table_settings['columnDefs'].push({
            "targets": [ 0 ],
            "visible": false,
            "searchable": false
        });
    }

    if (week > 0) {
        table_settings['columnDefs'].push({
            "targets": [ 1 ],
            "visible": false,
            "searchable": false
        });
    }

    tableSettings['ajax'] = '/data/data-table/' + year + '/' + week + _tmp;
    tableSettings['columns'] = [
        {'data': 'unidade_da_federacao'},
        {'data': 'isoweek'},
        {'data': 'srag'}
    ];

    // destroy old table
    dataTable.destroy();
    tableUI.empty(); // empty in case the columns change

    delete dataTables;

    // create new table
    tableContainerUI.html(divTableContent);
    dataTable = $('#data-table').DataTable(table_settings);
}