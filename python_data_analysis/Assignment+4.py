
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.0** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[1]:

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import re


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[2]:

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[3]:

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan","Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State","RegionName"]  )'''
    
 
    f = open('university_towns.txt')
    data = []
    for line in f:
        #print(line)
        m = re.search('(.+)\[edit\]',line) #get state
        if m:
            state=m.group(1)
        else:
            town = line.split('(')[0].strip()
            data.append([state,town])
    
    unitowns = pd.DataFrame(data,columns=["State","RegionName"])

    return unitowns

#get_list_of_university_towns()


# In[4]:

def load_gdp_data():
    gdp = pd.read_excel('gdplev.xls')
    gdp = gdp.drop(gdp.columns[list(range(4))+[5,7]],axis=1).drop(range(7))
    gdp.columns = ['quarter','GDP']
    gdp = gdp.reset_index(drop=True)
    gdp = gdp.drop(range(gdp[gdp['quarter'] == '2000q1'].index.tolist()[0])).reset_index(drop=True)
    return gdp

gdp = load_gdp_data()
    
    
def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    
    
    recessionflag = False
    onenegative = False
    for index,row in gdp.iterrows():
        if index > 0:
            change = gdp.loc[index]['GDP'] - gdp.loc[index-1]['GDP']
            #print(row['quarter'],int(change),onenegative,recessionflag)
            if change < 0 and recessionflag == False and onenegative == False:
                onenegative = True
            elif change < 0 and recessionflag == False and onenegative == True:
                recessionflag = True
                return gdp.loc[index-1]['quarter']
            elif change > 0:
                onenegative = False
                   
    return gdp

get_recession_start()


# In[5]:

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    
    starti = gdp[gdp['quarter'] == get_recession_start()].index.tolist()[0]
    
    recessionflag = True
    onepositive = False
    for index,row in gdp.iterrows():
        if index > starti:
            change = gdp.loc[index]['GDP'] - gdp.loc[index-1]['GDP']
            #print(row['quarter'],int(change),onepositive,recessionflag)
            if change > 0 and recessionflag == True and onepositive == False:
                onepositive = True
            elif change > 0 and recessionflag == True and onepositive == True:
                recessionflag = False
                return gdp.loc[index]['quarter']
            elif change < 0:
                onepositive = False
                   
    return gdp

get_recession_end()


# In[6]:

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    
    starti = gdp[gdp['quarter'] == get_recession_start()].index.tolist()[0]
    gdps = []
    recessionflag = True
    onepositive = False
    for index,row in gdp.iterrows():
        if index > starti:
            change = gdp.loc[index]['GDP'] - gdp.loc[index-1]['GDP']
            gdps.append((gdp.loc[index]['quarter'],gdp.loc[index]['GDP']))
            #print(gdps)
            #print(row['quarter'],int(change),onepositive,recessionflag)
            if change > 0 and recessionflag == True and onepositive == False:
                onepositive = True
            elif change > 0 and recessionflag == True and onepositive == True:
                recessionflag = False
                mingdp = min(gdps, key = lambda t: t[1])
                return mingdp[0]
                return gdps[gdps[0] == '2009q2']
            elif change < 0:
                onepositive = False
                   
    return gdp

get_recession_bottom()
    
   


# In[7]:

def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    hdata = pd.read_csv('City_Zhvi_AllHomes.csv')
    hdata = hdata.drop(hdata.columns[[0]+list(range(3,51))],axis=1)
    hdata2 = pd.DataFrame(hdata[['State','RegionName']])
    for year in range(2000,2016):
        #q1list = [str(year)+'-01',str(year)+'-02',str(year)+'-03']
        hdata2[str(year)+'q1'] = hdata[[str(year)+'-01',str(year)+'-02',str(year)+'-03']].mean(axis=1)
        hdata2[str(year)+'q2'] = hdata[[str(year)+'-04',str(year)+'-05',str(year)+'-06']].mean(axis=1)
        hdata2[str(year)+'q3'] = hdata[[str(year)+'-07',str(year)+'-08',str(year)+'-09']].mean(axis=1)
        hdata2[str(year)+'q4'] = hdata[[str(year)+'-10',str(year)+'-11',str(year)+'-12']].mean(axis=1)
    year = 2016    
    hdata2[str(year)+'q1'] = hdata[[str(year)+'-01',str(year)+'-02',str(year)+'-03']].mean(axis=1)
    hdata2[str(year)+'q2'] = hdata[[str(year)+'-04',str(year)+'-05',str(year)+'-06']].mean(axis=1)
    hdata2[str(year)+'q3'] = hdata[[str(year)+'-07',str(year)+'-08']].mean(axis=1)
    hdata2 = hdata2.replace({'State':states})
    hdata2 = hdata2.set_index(['State','RegionName'])
    return hdata2

#convert_housing_data_to_quarters().loc["Texas"].loc["Austin"].loc["2010q3"]
convert_housing_data_to_quarters()


# In[40]:

def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    unitowns = get_list_of_university_towns()
    bottom = get_recession_bottom()
    start = get_recession_start()
    hdata = convert_housing_data_to_quarters()
    #price_ratio=quarter_before_recession/recession_bottom
    bstart = hdata.columns[hdata.columns.get_loc(start) -1]
    
    hdata['ratio'] = hdata[bottom] - hdata[bstart]
    hdata = hdata[[bottom,bstart,'ratio']]
    hdata = hdata.reset_index()
    #print(hdata.sort('RegionName'))
    unitowns_hdata = pd.merge(hdata,unitowns,how='inner',on=['State','RegionName'])
    unitowns_hdata['uni'] = True
    hdata2 = pd.merge(hdata,unitowns_hdata,how='outer',on=['State','RegionName',bottom,bstart,'ratio'])
    hdata2['uni'] = hdata2['uni'].fillna(False)
    
    #print(hdata.iloc[10700])
#     print(len(hdata2[hdata2['uni'] == True]))
#     print(len(hdata2[hdata2['uni'] == False]))
#     print(len(hdata2))

    ut = hdata2[hdata2['uni'] == True]
    nut = hdata2[hdata2['uni'] == False]
    
    #print(ut)
    

    
    t,p = ttest_ind(ut['ratio'].dropna(),nut['ratio'].dropna())
    
    if p < 0.01: different = True
    else: different = False
    
    if ut['ratio'].mean() < nut['ratio'].mean(): better = "non-university town"
    else: better = "university town"

    return (different, p, better)

run_ttest()


# In[ ]:




# In[ ]:



