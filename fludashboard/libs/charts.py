from plotly import tools
from plotly.offline.offline import _plot_html

import cufflinks as cf
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import colorlover as cl

# local
from .episem import episem, lastepiday


cf.set_config_file(theme='white')


def ethio_ts(df=pd.DataFrame, scale_id=int, year=int):
    cols = [
        'Testes positivos',
        'Influenza A',
        'Influenza B',
        'VSR',
        'Adenovirus',
        'Parainfluenza 1',
        'Parainfluenza 2',
        'Parainfluenza 3',
    ]
    trace = []

    if scale_id == 2:
        ytitle = 'Casos'
    else:
        ytitle = 'Incidência'

    trace.append(
        go.Scatter(
            x=df['epiweek'],
            y=df[cols[0]],
            name=cols[0],
            mode='lines',
        )
    )

    for i, col in enumerate(cols[1:]):
        trace.append(
            go.Scatter(
                x=df['epiweek'],
                y=df[col],
                name=ytitle,
                mode='lines',
                showlegend=False
            )
        )

    nrows = len(cols)
    fig = tools.make_subplots(
        rows=nrows,
        cols=1,
        print_grid=False,
        subplot_titles=('Situação dos exames',
                        'Influenza A',
                        'Influenza B',
                        'VSR',
                        'Adenovirus',
                        'Parainfluenza 1',
                        'Parainfluenza 2',
                        'Parainfluenza 3'))

    for i in range(1, (nrows + 1)):
        fig.append_trace(trace[i - 1], i, 1)

    # Add extra lines to first subplot:
    extra_cols = ['Testes negativos',
                  'Casos sem teste laboratorial',
                  'Casos aguardando resultado',
                  'Casos sem informação laboratorial']
    for i, col in enumerate(extra_cols):
        fig.append_trace(
            go.Scatter(
                x=df['epiweek'],
                y=df[col],
                name=col,
                mode='lines',
                line=dict(color=cl.scales['12']['qual']['Paired'][-i])
            ), 1, 1)

    # X-axis title and range:
    lastepiweek = int(episem(lastepiday(year), out='W'))
    extra_cols.extend(['Testes positivos'])
    if scale_id == 2:
        ymax = [
            max(5*np.ceil(df[extra_cols].max().max()/5), 5),
            max(5*np.ceil(df[cols[1:]].max().max()/5), 5)
        ]
    else:
        ymax = [
            df[extra_cols].max().max(),
            df[cols[1:]].max().max()
        ]

    for i in range(1, (nrows + 1)):
        xaxis = 'xaxis%s' % i
        yaxis = 'yaxis%s' % i
        fig['layout'][xaxis].update(range=[1, lastepiweek])
        fig['layout'][yaxis].update(range=[0, ymax[min(1, i-1)]], rangemode='nonnegative')

    fig['layout']['xaxis%s' % nrows].update(title='Semana epidemiológica',
                                            zeroline=True, showline=True)

    i = int(nrows/2)
    fig['layout']['yaxis%s' % i].update(title=ytitle)

    fig['layout'].update(margin={'t': 50, 'l': 50})

    return _plot_html(
        figure_or_data=fig, config={}, validate=True,
        default_width='100%', default_height=1600, global_requirejs=''
    )[0]


def opportunities_boxplot(df: pd.DataFrame, week: int=None):
    """

    :param df:
    :param week:
    :return:

    """
    title_param = {
        'name': df.territory_name.unique()[0],
        'week': ''
    }

    if week not in [0, None]:
        title_param['week'] = 'até a semana epidemiológica %s ' % week

    df_plot = df.iloc[:, :-1].dropna(how='all', axis=1)

    # Set ymax to higher upper fence:
    q1 = df_plot.quantile(.25, axis=0)
    q3 = df_plot.quantile(.75, axis=0)
    ymax = (q3 + 1 * (q3 - q1)).max()

    # Set bottom and right margin to avoid xaxis labels beeing cut off
    figure = df_plot.iplot(
        kind='box',
        boxpoints=False,
        margin={'b': 130,
                't': 50,
                'r': 120,
                'l': 50
        },
        showlegend=False,
        yTitle='Dias',
        asFigure=True
    )

    figure['layout']['yaxis1'].update(range=[0, ymax])
    figure['layout']['xaxis1'].update(tickangle=30)

    return _plot_html(
        figure_or_data=figure, config={}, validate=True,
        default_width='100%', default_height=500, global_requirejs=''
    )[0]
