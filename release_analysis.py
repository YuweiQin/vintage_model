'''
Created on Mar 15, 2016
Release Data Analysis

@author: rsong_admin
'''
import numpy as np
import pandas as pd
import vintage_model
import matplotlib.pylab as plt
from matplotlib import style
style.use('ggplot')

def pie_chart(vintage_results, year=40):
    '''
    plot a pie chart show the release break down (by market) for the specific year
    '''
    labels = vintage_results.keys()
    size = []
    explode = (0,0.1,0,0,0,0,0) # only explode the second one
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    for each_key, each_val in vintage_results.iteritems():
        this_tot_rel_year = each_val['In Use'][40] + each_val['End of Life'][40]
        size.append(this_tot_rel_year)
    
    plt.pie(size,explode=explode,labels=labels,autopct='%1.1f%%',colors=colors,shadow=True)
    plt.show()
    
if __name__ == '__main__':
    ''' Read production data and multiply it with the market share data to coating and paints market'''
    tiO2_production_data = np.loadtxt('./data/TiO2_production_real.csv',delimiter=',')
    tiO2_to_coating = 0.3 # what portion of SiO2 are used in coating, paints and pigment market
    tiO2_production_data[:,1] = tiO2_production_data[:,1] * tiO2_to_coating
    
    ''' Set up and calcuate vintage''' 
    tiO2_market_data = './data/coating_market_fake.csv'
    tiO2 = vintage_model.vintage_market(tiO2_production_data,tiO2_market_data)
    tiO2_vintage_results_market = tiO2.calculate_market_vintage()
    total_release = tiO2.tot_releases_year()
    
    ax = plt.subplot(111)
    ax.plot(tiO2_production_data[30::,0],total_release[30::])
    plt.show()
    
