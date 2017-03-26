#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

hdf = pd.read_excel('housing_data.xlsx',header=2,skiprows=[3,5,6,17,18],skipfooter=6)

rdf = pd.read_excel('rental_data.xlsx',header=2,skiprows=[3,5,6,17,18],skipfooter=6)

# #print(hdf.head())
# print(rdf)

def process_data(df):

    for col in df.columns:
        df[str(col)+' scaled'] = df[col]/hdf[1990]

    df['Type'] = 'City'
    df[1]['Type'] = 'Country'
    df[1:11]['Type'] = 'Province'
    df[11:]['Type'] = 'City'

    print(df)

    return df



hdf = process_data(hdf)
rdf = process_data(rdf)




# for col in df.columns:
#     df[col] = df[col]/df[1990]
#
#
#
# df.transpose().plot()
# plt.show()
