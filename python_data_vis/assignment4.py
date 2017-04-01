#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import matplotlib.patches as mpatches

sns.set_style('white')


###########################
# Organize and clean data
###########################

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


###########################
# Make initial plot
###########################

f,ax = plt.subplots(2,2)
f.subplots_adjust(left=0.1, bottom=0.1, right=0.97, top=0.93,
                    wspace=0.15, hspace=0.25)
dhdfax = ax[0][0]
rdfax = ax[1][0]
regax = ax[0][1]
regax2 = ax[1][1]


def make_timeseries(ax,df):
    lines = df[-24:].plot(c='grey',alpha=0.15,ax=ax,legend=False,picker=4)
    london_line = df[-24:]['London'].plot(c=sns.color_palette()[1],ax=ax,legend=False,picker=0)
    return lines, london_line


dhdf_lines, dhdf_london_line = make_timeseries(dhdfax,dhdf)
rdf_lines, rdf_london_line = make_timeseries(rdfax,rdf)

dhdfax.set_title('Fractional Change in Housing Starts from 1992 \nfor London and Other Canadian Cities')
rdfax.set_title('Rental Vacancy Rate 1992-2015 \nfor London and Other Canadian Cities')
dhdfax.set_ylabel('Change Housing Starts')
rdfax.set_ylabel('Rental Vacancy Rate')


#sns.regplot(x=rdf[-24:]['London'],y=hdf[-24:]['London'],ax=regax)
#r,p = pearsonr(df.London_housing,df.London_rental)
#sns.regplot(x=rdf[-24:]['London'].shift(-6),y=hdf[-24:]['London'].shift(-6),ax=regdelax)

pal = sns.dark_palette(sns.color_palette()[1],as_cmap=True)
corr_scatter = regax.scatter(rdf[-24:]['London'],hdf[-24:]['London'],c=rdf.index.values,cmap=pal,picker=4)

regax.set_ylabel('Housing Starts')
regax2.set_ylabel('Housing Starts')
regax.set_xlabel('Vacancy Rate')
regax2.set_xlabel('Vacancy Rate')
regax.set_title('Housing Starts vs Vacancy Rate in London')

for ax in regax,regax2,dhdfax,rdfax:
    ax.set_alpha(0.7)

sns.despine()
#plt.tight_layout()

london_patch = mpatches.Patch(color=sns.color_palette()[1], label='London')
dhdfax.legend(handles=[london_patch])
rdfax.legend(handles=[london_patch])



###########################
# Make plot interactive
###########################

def onpick(event):

    # If clicking on a scatter point
    if event.artist.axes in [regax,regax2]:
        ind = event.ind[0]
        rental = float(rdf.iloc[ind]['London'])
        housing = float(hdf.iloc[ind]['London'])
        dhousing = float(dhdf.iloc[ind+2]['London'])
        year = rdf.index.values[ind]
        regax.text
        #print(year,event.mouseevent.x,event.mouseevent.y)
        # print(event.artist.axes.texts)
        for t in event.artist.axes.texts:
            t.remove()
        event.artist.axes.annotate(s=year,
                        xy=(event.mouseevent.xdata,event.mouseevent.ydata),
                        xycoords='data',
                        color=sns.color_palette()[1],
                        xytext=(0.9,0.9),
                        textcoords='axes fraction',
                        arrowprops=dict(arrowstyle='-',facecolor=sns.color_palette()[1]),
                        )


        if len(dhdfax.collections)>0:
            dhdfax.collections[0].remove()
            rdfax.collections[0].remove()

        dhdfax.scatter(year,dhousing,zorder=0,color=sns.color_palette()[1])
        rdfax.scatter(year,rental,zorder=0,color=sns.color_palette()[1])



    elif event.artist.axes in [dhdfax,rdfax]:

        # If clicking an activated (red) line
        if event.artist.get_color() == sns.color_palette()[2]:
            for line in dhdfax.lines + rdfax.lines:
                if line.get_label() != 'London':
                    line.set_color('grey')
                    line.set_alpha(0.15)
                    line.axes.legend(handles=[london_patch])

        # If clicking a grey line
        else:
            for line in dhdfax.lines + rdfax.lines:
                if line.get_label() != 'London':
                    line.set_color('grey')
                    line.set_alpha(0.15)
            if len(regax2.texts)>0:
                regax2.texts[0].remove()

            if event.artist.get_label() != 'London':
                for line in [ x for x in dhdfax.lines + rdfax.lines if x.get_label() == event.artist.get_label()]:
                    line.set_color(sns.color_palette()[2])
                    line.set_alpha(0.8)
                    pick_patch = mpatches.Patch(color=sns.color_palette()[2], label=event.artist.get_label())
                    line.axes.legend(handles=[london_patch,pick_patch])

                for collection in regax2.collections:
                    collection.remove()

                # recompute the ax.dataLim
                regax2.relim()
                # update ax.viewLim using the new dataLim
                regax2.autoscale_view()
                pal = sns.dark_palette(sns.color_palette()[2],as_cmap=True)
                regax2.scatter(rdf[-24:][event.artist.get_label()],hdf[-24:][event.artist.get_label()],c=rdf.index.values,cmap=pal,picker=4)
                regax2.set_title('Housing Starts vs Vacancy Rate in {}'.format(event.artist.get_label()))
    f.canvas.draw_idle()



f.canvas.mpl_connect('pick_event', onpick)




plt.show()
