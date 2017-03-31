#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import matplotlib.patches as mpatches

sns.set_style('white')


hdf = pd.read_excel('housing_data.xlsx',header=2,skiprows=[3,5,6,17,18],skipfooter=6)[11:].transpose()
rdf = pd.read_excel('rental_data.xlsx',header=2,skiprows=[3,5,6,17,18],skipfooter=6)[11:].transpose()


dhdf = hdf.copy()
dhdf = dhdf.transpose()
for col in range(1993,2016):
    dhdf[col] = dhdf[col] / dhdf[1992]

dhdf[1992] = 1
dhdf = dhdf.transpose()

drdf = rdf.copy()
drdf = drdf.transpose()
for col in range(1993,2016):
    drdf[col] = drdf[col] / drdf[1992]

drdf[1992] = 1
drdf = drdf.transpose()

#df = hdf.join(rdf,how='outer',lsuffix='_housing',rsuffix='_rental')




#citydf=df[df['Type']=='City']
f,ax = plt.subplots(2,2)

# def make_timeseries(ax,df):
#     for col in df.columns:
#         line, = ax.plot(range(1992,2016),df[-24:][col],c='grey',alpha=0.15)
#         if 'London' in col:
#             line[0].set_color(sns.color_palette()[1])
#             line[0].set_alpha(1)
#         # if 'Vancouver' in col:
#         #     line[0].set_color(sns.color_palette()[1])
#         #     line[0].set_alpha(1)

def make_timeseries(ax,df):
    lines = df[-24:].plot(c='grey',alpha=0.15,ax=ax,legend=False,picker=4)
    london_line = df[-24:]['London'].plot(c=sns.color_palette()[1],ax=ax,legend=False,picker=0)
    return lines, london_line


dhdf_lines, dhdf_london_line = make_timeseries(ax[0][0],dhdf)
rdf_lines, rdf_london_line = make_timeseries(ax[1][0],rdf)
#ax[0].set_yscale("log")

ax[0][0].set_title('Fractional Change in Housing Starts from 1992 for London and Other Canadian Cities')
ax[1][0].set_title('Rental Vacancy Rate 1992-2015 for London and Other Canadian Cities')
ax[0][0].set_ylabel('Change Housing Starts')
ax[1][0].set_ylabel('Rental Vacancy Raimport matplotlib.patches as mpatcheste')


sns.regplot(x=rdf[-24:]['London'],y=hdf[-24:]['London'],ax=ax[0][1])
#r,p = pearsonr(df.London_housing,df.London_rental)
sns.regplot(x=rdf[-24:]['London'].shift(-6),y=hdf[-24:]['London'].shift(-6),ax=ax[1][1])

sns.despine()
plt.tight_layout()



london_patch = mpatches.Patch(color=sns.color_palette()[1], label='London')
ax[0][0].legend(handles=[london_patch])
ax[1][0].legend(handles=[london_patch])

def onpick(event):

    if event.artist.get_color() == sns.color_palette()[2]:
        event.artist.set_color('grey')
        event.artist.set_alpha(0.15)
        event.artist.axes.legend(handles=[london_patch])
    else:
        for line in ax[0][0].lines + ax[1][0].lines:
            if line.get_label() != 'London':
                line.set_color('grey')
                line.set_alpha(0.15)

        if event.artist.get_label() != 'London':
            event.artist.set_color(sns.color_palette()[2])
            event.artist.set_alpha(0.8)
            pick_patch = mpatches.Patch(color=sns.color_palette()[2], label=event.artist.get_label())
            event.artist.axes.legend(handles=[london_patch,pick_patch])
    f.canvas.draw_idle()

f.canvas.mpl_connect('pick_event', onpick)




plt.show()
