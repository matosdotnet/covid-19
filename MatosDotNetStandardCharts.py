# -*- coding: utf-8 -*-
"""
Created on Sun May 24 11:14:48 2020

@author: rmatos
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import datetime

def line_plot_df_tindex(y,data,title,ylabel,ycolor,window_span=7,bollinger_type='EMA',evends_data = pd.DataFrame()):
    '''
    bollinger_type:
                    'EMA' Exponential moving average
                    'MA' Moving average
    '''
    #Mean ans Standard Deviations
    v_mean = data[y].mean()
    v_std =  data[y].std()

    v_df_averages    = pd.Series([], dtype= 'float64')
    v_df_upper_stds  = pd.Series([], dtype= 'float64')
    v_df_lower_stds  = pd.Series([], dtype= 'float64')

    if bollinger_type == 'MA':
        v_df_averages = data[y].rolling(window=window_span).mean()
        v_df_upper_stds = v_df_averages + 2*data[y].rolling(window=window_span).std()
        v_df_lower_stds = v_df_averages - 2*data[y].rolling(window=window_span).std()
    elif bollinger_type == 'EMA':
        v_df_averages = data[y].ewm(span=window_span).mean()
        v_df_upper_stds = v_df_averages + 2*data[y].ewm(span=window_span).std()
        v_df_lower_stds = v_df_averages - 2*data[y].ewm(span=window_span).std()
    else :
        return 0

    #Set Style
    sns.set_style('darkgrid',
              {
                  'axes.facecolor': '#646666',
                  'figure.facecolor': '#646666',
                  'grid.color': 'lightgrey',
                  'grid.linestyle': 'dotted',
                  'xtick.color': 'white',
                  'xtick.top': False,
                  'xtick.bottom': True,
                  'ytick.color': 'white',
                  'ytick.left': True,
                  'ytick.right': False,
                  'axes.labelcolor': 'white',
                  'axes.spines.top': False,
                  'axes.spines.right': False,
                  'text.color': 'white'

              })

    #Set Fig Size
    fig = plt.figure(figsize=(12,5))

    #Plot events
    for d in evends_data.index :
        plt.axvline(d,color='#000000',linestyle='dotted',alpha=0.2)

    #Line Plots for Mean and Standard Deviation
    ax = sns.lineplot(x=data.index,y=v_df_averages
                      ,color = '#5CFE00'
                      ,alpha = 0.2
                      ,dashes=True
                     # ,estimator = 'mean'
                     )

    ax = sns.lineplot(x=data.index,y=v_df_upper_stds
                      ,color = '#5CFE00'
                      ,alpha = 0.2
                      ,dashes=True
                     # ,estimator = 'mean'
                     )

    ax.lines[1].set_linestyle('dotted')
    ax = sns.lineplot(x=data.index,y=v_df_lower_stds
                      ,color = '#5CFE00'
                      ,alpha = 0.2
                      ,dashes=True
                     # ,estimator = 'mean'
                     )
    ax.lines[2].set_linestyle('dotted')

    #Line Plot with data

    ax = sns.lineplot(x=data.index,y=data[y]
                      ,marker=True
                      ,markers=["o", "o"]
                      ,alpha = 0.5
                      ,dashes=False
                      ,style=True
                      ,hue = 1
                      ,palette = [ycolor]
                     # ,estimator = 'mean'
                     )

    # Rerieve Max, Min and Latest
    y_max = data[y].max()
    x_max = data[[y]].idxmax()[0]
    y_min = data[y].min()
    x_min = data[[y]].idxmin()[0]
    y_mean = y_max+y_max*0.10
    x_mean = data[[y]].index[0]
    x_latest =  data.index.max()
    y_latest = data[x_latest:x_latest][y][0]

    # Slice the chart canvas
    ax.set_xlim(data.index.min(), data.index.max()+datetime.timedelta(days=1))

    if y_min >= 0 :
        ax.set_ylim(0, y_max+y_max*0.10)
    else :
        ax.set_ylim(y_min+y_min*0.10, y_max+y_max*0.10)

    #Set Date Format
    str_date_format = '%d/%m'

    #Anotattions for Max, Min and Latest
    lbl_y_offset = 0.02*y_max
    lbl_y_max_offset = 0.02*y_max
    lbl_y_min_offset = 0.02*y_min

    ax.annotate('  MAX: {0:.0f} \n {1}'.format(y_max,x_max.strftime(str_date_format))
                ,xy=(x_max,y_max)
                ,xytext=(x_max,y_max+lbl_y_max_offset)
                ,ha='center')

    if (x_min != x_max) :
        ax.annotate('  MIN: {0:.0f} \n {1}'.format(y_min,x_min.strftime(str_date_format))
                ,xy=(x_min,y_min)
                ,xytext=(x_min,y_min+lbl_y_min_offset)
                ,ha='center')

    if (x_latest != x_max) and (x_latest!= x_min) :
        ax.annotate('  {0:.0f} \n {1}'.format(y_latest,x_latest.strftime(str_date_format))
                ,xy=(x_latest,y_latest)
                ,xytext=(x_latest,y_latest+lbl_y_offset)
                ,ha='center')

    plt.figtext(0.1, 0.05,'x̄: {0:.1f} σ: {1:.1f} : {2}[x̄ +- 2σ] N={3:.0f}'.format(v_mean,v_std,bollinger_type,window_span)
               #,ha='right'
               ,color='#5CFE00')

    #Axis and Labels formating
    ax.set_title(title)

    #Make sure the dataset has continuous dates in the DataFrame
    ax.set_xlabel('Last {0} days'.format(len(data.index)))
    ax.set_ylabel(ylabel)

    myFmt = mdates.DateFormatter(str_date_format)
    ax.xaxis.set_major_formatter(myFmt)
    ax.legend().remove()

    # Fill Area
    plt.fill_between( data.index, data[y], color=ycolor, alpha=0.2)

    #fig.savefig("{}.png".format(title),bbox_inches = 'tight', dpi=plt.gcf().dpi,facecolor='#646666')
    fig.savefig("img/{}.png".format(title),bbox_inches = 'tight', dpi=300,facecolor='#646666')

    plt.show()
