'''
Created on Mar 4, 2016

@author: rsong_admin
'''
import numpy as np
import csv
import pandas as pd
import matplotlib.pylab as plt
from matplotlib import style

style.use('ggplot')

class vintage_market:
    '''
    A wrapper class to deal with the situation with multiply market
    '''
    def __init__(self,production_data, market_data_file):
        self.year_and_prod = production_data
        self.tot_prod = production_data[:,1]
        self.years = production_data[:,0]
        ''' split market data '''
        self._market_splitter(market_data_file)
        
    def _market_splitter(self,market_data_file):
        '''
        market data file reader
        
        Input -- market data file, the first column is the name of the sector
                 the second column is the percentage of each sector
        Return -- A dictionary contain sector name and break down
        '''
        with open(market_data_file,'rU') as myfile:
            this_reader = csv.reader(myfile)
            ''' row[0] is the sector name; row[1] percentage; row[2] average_lifetime '''

            self.market_dict = {rows[0]:[rows[1],rows[2]] for rows in this_reader}
            
        self.prod_dict = {}
        for each_mak, each_val in self.market_dict.iteritems():
            ''' create a dictionary that contain the production data flows into each market
                for example : Buildings: 89000*45% tons
                each_val[0] is the percentage
            '''
            this_mark_year_prod = self.year_and_prod
            this_mark_year_prod[:,1] = this_mark_year_prod[:,1]*float(each_val[0])
            self.prod_dict[each_mak] = [this_mark_year_prod]  

          
    def calculate_market_vintage(self):
        '''
        wrapper function to call the vintage class by market share
        '''
        assert self.prod_dict is not None
        self.market_vintage_results = {}

        for each_mak, each_val in self.prod_dict.iteritems():
            this_lifetime = self.market_dict[each_mak][1]
            print this_lifetime
            raw_input()
            this_prod_data = each_val[0]
            this_market = vintage(this_prod_data,this_lifetime)
            this_vintage = this_market.calculate_vintage()
            self.market_vintage_results[each_mak] = this_vintage 
        return self.market_vintage_results
        
class vintage:
    '''
    A vintage model to calculate the cumulative 
    In use and end-of-life release
    for one nano material 
    
    FOR A SINGLE MARKET
    
    The input file must be the annual production data
    The first column is the year and the second column is the production in ton
    '''
    def __init__(self, production_data, average_lifetime):
        self.prod_data = production_data
        self.in_use_rate = 0.1 #assume 10% in use release of this material
        
        self.year = self.prod_data[:,0]
        self.year_production = self.prod_data[:,1]
        
        self.num_year = len(self.year)
        self.x = float(average_lifetime) # The average lifetime for the weibull distribution. Fixed at this time
        self.shape = 5.0 # The shape parameter for weibull distribution, fixed to 5 at this time. Need to know why later
        self.start_year = self.prod_data[0,0]
        self.end_year = self.prod_data[-1,0]
        
    def _inUse(self, stock_last, in_use_release_rate):
        '''
        Calculate the in use release of a year 
        base on the stock size of the year before it.
        '''
        return stock_last * in_use_release_rate
    
    
    def vintage_for_year(self,data_of_year, year):
        '''
        calculate the vintage for a single year through all the year 
        after it
        Input
            data_of_year: the production volunme of the year of this vintage (MT)
            year: what year is this vintage year?
            example: vintage_for_year(382, 1970) 
        
        Return
            A dictionary that contain the Stock size, the In use release and the end of life release 
            of this vintage in each following year.
            Any year before this year are all zeros
        ''' 
        
        number_of_year = year-self.start_year
        left_year = int(self.end_year - year)
        
        year_in_use = np.zeros(self.num_year)
        year_end_of_life = np.zeros(self.num_year)
        year_stock = np.zeros(self.num_year)
        init_stock = data_of_year # This is the initial stock size
        year_stock[number_of_year] = init_stock # initilize
        
        for this_year in range(int(year), int(self.end_year)):
            year_count = this_year - int(year)
            i = this_year - self.start_year
            i = int(i+1) # starting from the next year after the init year

            this_in_use = year_stock[i-1] * self.in_use_rate 
            
            this_weibull = self.weib(year_count, self.x, self.shape) # This is the probability that it goes to end of life at this year (i)
            this_end_of_life = year_stock[i-1] * (1-self.in_use_rate) * this_weibull
            
            this_total_release = this_in_use + this_end_of_life
            
            year_in_use[i] = this_in_use
            year_end_of_life[i] = this_end_of_life
            year_stock[i] = year_stock[i-1] - this_total_release

        year_dict = {'In Use':year_in_use,"End of Life":year_end_of_life,"Stock":year_stock}
        
        return year_dict
    
    def calculate_vintage(self):
        '''
        Aggregate the vintage results (In_use, end_of_life and stock size) of every vintage year
        '''
        self.total_vintage = {} # dictionary to every vintage
        
        acc_stock = np.zeros(self.num_year)
        acc_in_use_release = np.zeros(self.num_year)
        acc_end_of_life_release = np.zeros(self.num_year)
        
        for i in range(int(self.num_year)):
            this_year = int(self.prod_data[i,0])
            print 'Working on Year ', this_year
            this_year_data = self.prod_data[i,1]
            this_year_vintage = self.vintage_for_year(this_year_data, this_year)
            # add this year vintage to the total vintage dictionary, so that we can query each individual vintage later
            self.total_vintage[this_year] = this_year_vintage
            
            # accumulate the stock size
            acc_stock += this_year_vintage['Stock']
            # accumulate the in_use_release
            acc_in_use_release += this_year_vintage['In Use']
            # ...the end_of_life
            acc_end_of_life_release += this_year_vintage['End of Life']
        
        self.acc_vintage ={'Stock':acc_stock, 'In Use':acc_in_use_release,'End of Life':acc_end_of_life_release}
        return self.acc_vintage
            
    def weib(self,x,n,a):
        '''
        A weibull distribution generator
        X: year
        n: average lifetime in this case
        a: shape parameter
        Source: http://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.random.weibull.html
        '''
        return (a / n) * (x / n)**(a - 1) * np.exp(-(x / n)**a)

    def plot_vintage(self):
        '''
        A function that plot the total production, 
        the in use and end-of-life release and the stock size of each year
        '''
        assert self.acc_vintage is not None
        plt.figure()
        plt.plot(self.year,self.year_production,label='Total Production')
        plt.plot(self.year,self.acc_vintage['In Use'],label='In Use Release')
        plt.plot(self.year,self.acc_vintage['End of Life'],label='End of Life Release')
        plt.legend(loc='upper left')
        
        plt.show()
    
if __name__ == '__main__':
    tiO2_data = np.loadtxt('./data/TiO2_market_real.csv',delimiter=',')

#     tiO2 = vintage(tiO2_data,10)
#     test_results = tiO2.calculate_vintage()
#     tiO2.plot_vintage()
    
    tiO2_market = vintage_market(tiO2_data,'./data/TiO2_market_fake.csv')
    test = tiO2_market.calculate_market_vintage()
    print test
