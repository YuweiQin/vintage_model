'''
Created on Mar 15, 2016
A caller to calculate the SiO2 vintage release 

Year 1970 - Year 2020
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

def calculate_defult_SiO2():
    '''
    Do a single vintage calculation
    default market share  = 0.1
    '''
    # read data now
    SiO2_data = np.loadtxt('./data/SiO2_production_real.csv',delimiter=',')
    SiO2_to_paints = 0.1 # what portion of SiO2 are used in coating, paints and pigment market
    SiO2_data[:,1] = SiO2_data[:,1] * SiO2_to_paints
    market_data_dict = csv_to_dict('./data/coating_market_fake.csv')
    
    SiO2_market = vintage_model.vintage_market(SiO2_data,market_data_dict)
    test = SiO2_market.calculate_market_vintage()
    df = SiO2_market.to_dataframe(test)
    SiO2_market.plot_market_vintage()
    df.to_csv('./results/SiO2_vintage_results.csv')

def do_shake_lifetime():
    data = './data/SiO2_production_real.csv'
    market = './data/coating_market_fake.csv'
    SiO2_to_coating = 0.1
    this_shaker = lifetime_shaker(data,market,SiO2_to_coating)
    MT_results = this_shaker.monte_carlo_analysis(round=500)
    average_tot = calculate_defult_SiO2()
    this_shaker.plot_error_bar(MT_results,average_tot)

def do_release_market():
    SiO2_data = np.loadtxt('./data/SiO2_production_real.csv',delimiter=',')
    market_data_dict = csv_to_dict('./data/coating_market_fake.csv')
    SiO2_to_coating = 0.1
    SiO2_data[:,1] = SiO2_data[:,1] * SiO2_to_coating
    SiO2_market = vintage_model.vintage_market(SiO2_data,market_data_dict)
    test = SiO2_market.calculate_market_vintage()
    print SiO2_market.tot_releases_year()
    SiO2_market.plot_market_vintage('')
    
    
if __name__ == '__main__':
    calculate_defult_SiO2()
    