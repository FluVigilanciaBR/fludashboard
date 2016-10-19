/** */
class SRAGChart{
    /**
     * Plot incidence chart using
     * @param {number} year - year to filter the data
     * @param {string} state_name - state_name to filter the data
     * @param {number} week- week to filter the data
     */
    static plot(bindto, year, state_name, week) {
        return = c3.generate({
            bindto: bindto,
            data: {
              url: './data/weekly-incidence-curve/' + year + '/' + state_name,
              x: 'isoweek',
              names: {
                  corredor_baixo: null,
                  corredor_mediano: null,
                  corredor_alto: null,
                  srag: 'SRAG',
                  limiar_pre_epidemico: 'Limiar Pré epidêmico',
                  intensidade_alta: 'Intensidade Alta',
                  intensidade_muito_alta: 'Intensidade Muito Alta'
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
                intensidade_muito_alta: '#ff0000'
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
              y: {show: false}
            },/*
            zoom: {
              enabled: true
            },*/ /*
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
    }
}