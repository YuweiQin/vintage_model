'''
Created on Mar 17, 2016
Sensitive Analysis for the average lifetime of different sectors
in Monte Carlo Style
@author: rsong_admin
'''
import vintage_model
import numpy as np
import csv
import matplotlib.pylab as plt
import vintage_model
from matplotlib import style
style.use('ggplot')

class lifetime_shaker:
    def __init__(self,production_data_csv, market_csv, nano_to_paints = 0.1):
        '''
        The input files are the production data of the Nanomaterial across year
        And the dictionary of the market sectors information
        '''
        self.prod_year_data = np.loadtxt(production_data_csv,delimiter=',')
        self.nano_to_paints = nano_to_paints
        self.prod_year_data[:,1]=self.prod_year_data[:,1]*self.nano_to_paints
        
        self.years=[int(year) for year in self.prod_year_data[:,0]]
        self.market_data_dict = self._csv_to_dict(market_csv)
           
    def _csv_to_dict(self,csv_file):
        with open(csv_file,'rU') as myfile:
            this_reader = csv.reader(myfile)
            ''' row[0] is the sector name; row[1] percentage; row[2] average_lifetime; row[3] is the in use release rate '''
            market_dict = {rows[0]:[rows[1],rows[2],rows[3],rows[4],rows[5],rows[6]] for rows in this_reader}
        return market_dict
    
    def _normal_generator(self,mean,sigma,top,bot):
        '''
        a normal distribution generator and limit the results to a range
        '''
        this_num = np.random.normal(mean,sigma)
        
        if this_num<bot:
            this_num = bot
        elif this_num > top:
            this_num = top
        return this_num
    
    def _shake_lifetime(self):
        '''
        shake this lifetime dictionary based on the 
        std and mean and the top,bot range
        '''
        new_mark_dict={}
        for each_mak, each_val in self.market_data_dict.iteritems():
            this_mean_lifetime = float(each_val[1])
            this_std = float(each_val[3])
            this_bot = float(each_val[4])
            this_top = float(each_val[5])
            new_lifetime = self._normal_generator(this_mean_lifetime, this_std, this_top, this_bot)
            new_mark_dict[each_mak] = [each_val[0],str(new_lifetime),each_val[2]]
        return new_mark_dict
    
    def monte_carlo_analysis(self, round = 100):
        
        results = []
        for i in range(round):
            print 'Working on round', i
            this_market_dict = self._shake_lifetime()
            this_market_vintage = vintage_model.vintage_market(self.prod_year_data,this_market_dict)
            this_vintage_results = this_market_vintage.calculate_market_vintage()
            this_vintage_tot_release = this_market_vintage.tot_releases_year()
            results.append(this_vintage_tot_release)
        
        return results
    
    def plot_error_bar(self,MT_results,average_case):
        '''
        plot the figure of total annual releases
        with error bar
        '''
        year_distribution = []
        round = len(MT_results)
        num_year = len(MT_results[0])
        plt.figure()
        final_results = []
        for each_year in range(num_year):
            this_year_resutls = []
            for each_ana in range(round):
                this_round_year = MT_results[each_ana][each_year]
                this_year_resutls.append(this_round_year)
            final_results.append(this_year_resutls) 
        plt.plot(self.years[40::],average_case[40::],label='Average Release Case')
        plt.boxplot(final_results[40::],positions=self.years[40::],labels=self.years[40::],widths=0.2)
        plt.xlabel('Year')
        plt.ylabel('Total Releases From Coating Products (Ton)')
        plt.legend()
        
        plt.show()

if __name__ == '__main__':
    pass
    