'''
Created on Mar 15, 2016
Vintage model calculation for nano Fe + FeOxides
@author: rsong_admin
'''
import vintage_model
import numpy as np
import csv
import matplotlib.pylab as plt
from monte_carlo_lifetime import *
from matplotlib import style
style.use('ggplot')

'''
Calculate the average case
'''
def csv_to_dict(csv_file):
    with open(csv_file,'rU') as myfile:
        this_reader = csv.reader(myfile)
        ''' row[0] is the sector name; row[1] percentage; row[2] average_lifetime; row[3] is the in use release rate '''
        market_dict = {rows[0]:[rows[1],rows[2],rows[3],rows[4],rows[5],rows[6]] for rows in this_reader}
    return market_dict

def calculate_defult_Fe():
    '''
    Do a single vintage calculation
    default in use Rate = 0.33
    '''
    # read data now
    Fe_data = np.loadtxt('./data/Fe_production_real.csv',delimiter=',')
    Fe_to_paints = 0.33 # what portion of SiO2 are used in coating, paints and pigment market
    Fe_data[:,1] = Fe_data[:,1] * Fe_to_paints
    market_data_dict = csv_to_dict('./data/coating_market_fake.csv')
    
    FeO2_market = vintage_model.vintage_market(Fe_data,market_data_dict)
    test = FeO2_market.calculate_market_vintage()
    df = FeO2_market.to_dataframe(test)
    FeO2_market.plot_market_vintage()
    df.to_csv('./results/Fe_vintage_results.csv')
#     total = FeO2_market.tot_releases_year()
#     plt.figure()
#     plt.plot(total)
#     plt.show()
#     return total

def do_shake_lifetime():
    data = './data/Fe_production_real.csv'
    market = './data/coating_market_fake.csv'
    Fe_to_coating = 0.33
    this_shaker = lifetime_shaker(data,market,Fe_to_coating)
    MT_results = this_shaker.monte_carlo_analysis(round=500)
    average_tot = calculate_defult_Fe()
    this_shaker.plot_error_bar(MT_results,average_tot)

def do_release_market():
    Fe_data = np.loadtxt('./data/Fe_production_real.csv',delimiter=',')
    market_data_dict = csv_to_dict('./data/coating_market_fake.csv')
    SiO2_to_coating = 0.1
    Fe_data[:,1] = Fe_data[:,1] * SiO2_to_coating
    Fe_market = vintage_model.vintage_market(Fe_data,market_data_dict)
    test = Fe_market.calculate_market_vintage()
    print Fe_market.tot_releases_year()
    Fe_market.plot_market_vintage('In Use')
    
if __name__ == '__main__':
    calculate_defult_Fe()
        