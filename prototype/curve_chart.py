import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.font_manager as fm
import numpy as np


def get_curve_data():
    # data
    dfincidence = pd.read_csv('../data/clean_data_filtro_sintomas_dtsin4mem-incidence-2013.csv')
    dftypical = pd.read_csv('../data/mem-typical-2016-uf.csv')
    dfthresholds = pd.read_csv('../data/mem-report-2016-uf.csv')
    dfpop = pd.read_csv('../data/populacao_uf_regional_atual.csv')
    df = pd.merge(
        dfincidence, dftypical, on=['UF', 'isoweek'], how='right'
    ).merge(dfthresholds.drop(['Unidade da Federação', 'População'], axis=1), on='UF')

    '''
    season = 'SRAG2013'
    uf = 'Rio Grande do Sul'
    week = 32
    dftmp = df[df['Unidade da Federação'] == uf]

    # Set font properties
    fontproplgd = fm.FontProperties('Oswald')
    fontproplgd.set_size(28)
    fontproplbl = fm.FontProperties('Oswald')
    fontproplbl.set_size(42)
    fontpropticks = fm.FontProperties('Oswald')
    fontpropticks.set_size(24)

    # Set figure size
    fig, ax = plt.subplots(1, 1, figsize = [20, 20])

    # Set ymax at least = 1:
    maxval1 = max(dftmp[[season, 'corredor alto', 'intensidade muito alta']].max().max(), 1)
    ax.set_ylim([0,maxval1])

    # Plot lines and regions:
    ax.fill_between(dftmp['isoweek'], 0, dftmp['corredor baixo'], color='green', alpha=0.5)
    ax.fill_between(dftmp['isoweek'], dftmp['corredor baixo'], dftmp['corredor mediano'], color='yellow', alpha=0.5)
    ax.fill_between(dftmp['isoweek'], dftmp['corredor mediano'], dftmp['corredor alto'], color='orange', alpha=0.5)
    dftmp.plot(ax=ax, x='isoweek', y=season, color='k', lw=3)
    dftmp.plot(ax=ax, x='isoweek', y='limiar pré-epidêmico', style='--', lw=3)
    dftmp.plot(ax=ax, x='isoweek', y='intensidade alta', style='--', lw=3)
    dftmp.plot(ax=ax, x='isoweek', y='intensidade muito alta', style='--', lw=3)
    dftmp.plot(ax=ax, x='isoweek', y='corredor alto', legend=False, alpha=0)

    # Grab ylim in order to set the range for the red zone:
    miny, maxy = ax.get_ylim()
    del(ax.lines[-1])
    ax.fill_between(dftmp['isoweek'], dftmp['corredor alto'], maxy, color='red', alpha=0.5)
    ax.set_ylim([miny, maxy])

    # Draw vertical line indicating user selected week:
    plt.axvline(axes=ax, x=week, color='silver', lw=8, alpha=0.5)

    # Use defined font properties for axis tick labels
    for label in ax.get_xticklabels() :
        label.set_fontproperties(fontpropticks)    
    for label in ax.get_yticklabels() :
        label.set_fontproperties(fontpropticks)

    ax.set_title(uf, fontproperties=fontproplbl)
    ax.set_xlabel('SE', fontproperties=fontproplbl)
    ax.set_ylabel('Incidência (por 100mil habitantes)', fontproperties=fontproplbl)
    xticks = np.arange(4,53,4)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks)

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(prop=fontproplgd, loc='center left', bbox_to_anchor=(1,0.5))
    '''

    return df.to_json(orient='records')

