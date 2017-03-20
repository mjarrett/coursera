#!/usr/bin/env python3

# Use the following data for this assignment:


import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
import matplotlib

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(33500,150000,3650),
                   np.random.normal(41000,90000,3650),
                   np.random.normal(41000,120000,3650),
                   np.random.normal(48000,55000,3650)],
                  index=[1992,1993,1994,1995])

df['Mean'] = df.mean()
df['STD'] = df.std()


class MyFig:
    def __init__(self,df):


        self.df = df
        self.ndf = self.df.transpose()

        self.f,self.ax = plt.subplots(1)
        self.f.show()
        self.xlabels = [str(x) for x in df.index]
        self.bar = self.ax.bar(self.df.index,df['Mean'],yerr=self.df['STD'],color='lightblue')
        self.ax.xaxis.set_ticks(self.df.index)
        self.ax.xaxis.set_ticklabels(self.xlabels)
        self.ax.set_xlim(1991,1996)


        # tell mpl_connect we want to pass a 'button_press_event' into onclick when the event is detected
        self.f.canvas.mpl_connect('button_press_event', self.onclick)

        self.y1 = None
        self.y2 = None

        self.f.show()

    def onclick(self,event):

        if self.y1 is not None and self.y2 is not None:
            self.y1 = None
            self.y2 = None
            self.ax.lines.remove(self.line1)
            self.ax.lines.remove(self.line2)
            self.ax.collections.remove(self.fill)
        if self.y1 == None:
            self.y1 = event.ydata
            self.line1, = self.ax.plot([1991.5,1995.5],[event.ydata,event.ydata],color='blue')
        elif self.y2 == None:
            self.y2 = event.ydata
            self.line2, = self.ax.plot([1991.5,1995.5],[event.ydata,event.ydata],color='red')
            self.fill = self.ax.fill_between([1991.5,1995.5],[self.y1,self.y1],[self.y2,self.y2],color='red',alpha=0.2)

            prob_list = self.get_prob()
            for i in [0,1,2,3]:
                self.bar[i].set_color(str(prob_list[i]))

        self.f.canvas.draw()




    def get_prob(self):
        results = []
        for ind in self.ndf.columns:
            ys = sorted([self.y1,self.y2])
            self.lower = ys[0]
            self.upper = ys[1]
            results.append(len(self.ndf[(self.ndf[ind]<self.upper) & (self.ndf[ind]>self.lower)])/len(self.ndf))
        print(self.upper,self.lower)
        print(results)
        return results
