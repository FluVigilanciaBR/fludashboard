from plotly import tools
from plotly.offline import download_plotlyjs, iplot
from plotly.offline.offline import _plot_html

import numpy as np
import pandas as pd
import plotly.graph_objs as go

# local
from .episem import episem, lastepiday


def ethio_ts(df=pd.DataFrame, scale_id=int, year=int):
    cols = [
        'Testes positivos',
        'Testes negativos',
        'Influenza A',
        'Influenza B',
        'VSR',
        'Adenovirus',
        'Parainfluenza 1',
        'Parainfluenza 2',
        'Parainfluenza 3',
        'Casos sem teste laboratorial',
        'Casos aguardando resultado',
        'Casos sem informação laboratorial'
    ]
    trace = []
    for i, col in enumerate(cols):
        trace.append(
            go.Scatter(
                x=df['epiweek'],
                y=df[col],
                name='',
                mode='lines'
            )
        )

    nrows = len(cols)
    fig = tools.make_subplots(
        rows=nrows,
        cols=1,
        print_grid=False,
        subplot_titles=('Testes positivos',
                        'Testes negativos',
                        'Influenza A',
                        'Influenza B',
                        'VSR',
                        'Adenovirus',
                        'Parainfluenza 1',
                        'Parainfluenza 2',
                        'Parainfluenza 3',
                        'Casos sem teste laboratorial',
                        'Casos aguardando resultado',
                        'Casos sem informação laboratorial'))

    for i in range(1, (nrows + 1)):
        fig.append_trace(trace[i - 1], i, 1)

    # X-axis title and range:
    lastepiweek = int(episem(lastepiday(year), out='W'))
    for i in range(1, (nrows + 1)):
        xaxis = 'xaxis%s' % i
        yaxis = 'yaxis%s' % i
        fig['layout'][xaxis].update(range=[1, lastepiweek])
        ymax = max(5 * np.ceil(df[cols[i - 1]].max() / 5), 5)
        fig['layout'][yaxis].update(range=[0, ymax], rangemode='nonnegative')

    fig['layout']['xaxis%s' % nrows].update(title='Semana epidemiológica',
                                            zeroline=True, showline=True)

    if scale_id == 1:
        ytitle = 'Casos'
    else:
        ytitle = 'Incidência (por 100mil hab.)'
    i = int(nrows / 2)
    fig['layout']['yaxis%s' % i].update(title=ytitle)

    territory_lbl = df['territory_name'].unique()[0]
    fig['layout'].update(
        height=1600,
        width=800,
        title='Exames laboratoriais - %s' % territory_lbl,
        showlegend=False,
        # yaxis='Teste'
    )
    # , , global_requirejs
    html_div, div_id, width, height = _plot_html(
        figure_or_data=fig, config={}, validate=True,
        default_width='100%', default_height=200, global_requirejs=''
    )

    return html_div