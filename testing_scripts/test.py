'''
Created on Mar 4, 2016

@author: rsong_admin
'''
import numpy as np
import matplotlib.pylab as plt
from scipy.special import gammaln, betaln
from matplotlib import style
style.use('ggplot')

def weib(x,n,a):
        '''
        A weibull distribution generator
        X: year
        n: average lifetime in this case
        a: shape parameter
        Source: http://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.random.weibull.html
        '''
        return (a / n) * (x / n)**(a - 1) * np.exp(-(x / n)**a)
    
def lifetime_to_beta(average_lifetime, shape):
        '''
        convert average lifetime to beta in Weibull distribution
        '''
        return average_lifetime/(np.exp(gammaln(1+1/shape)))
    
    
if __name__ == '__main__':
    
    a0 = 0.5
    a1 = 1
    a2 = 2
    a4 = 4
    a8 = 8
    x0 = lifetime_to_beta(a0, 5)
    x1 = lifetime_to_beta(a1, 5)
    x2 = lifetime_to_beta(a2, 5)
    x4 = lifetime_to_beta(a4, 5)
    x8 = lifetime_to_beta(a8, 5)
    year = np.arange(0,10,0.1)

    w0 = weib(year,x0,5)
    w1 = weib(year,x1,5)
    w2 = weib(year,x2,5)
    w4 = weib(year,x4,5)
    w8 = weib(year,x8,5)
    
#     plt.plot(year,w0,label='t=0.5')
    plt.plot(year,w1,label='t = 1')
    plt.plot(year,w2, label='t = 2')
    plt.plot(year,w4,label='t = 4')
    plt.plot(year,w8,label='t = 8')
    plt.legend()
    plt.xlabel('Year')
    plt.ylabel('Probability')
    plt.show()