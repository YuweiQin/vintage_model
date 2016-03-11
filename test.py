'''
Created on Mar 4, 2016

@author: rsong_admin
'''
import numpy as np
import matplotlib.pylab as plt
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

print weib(10,10,5.0)
raw_input()   
x = np.arange(0,70,0.1)
weibull = weib(x, 10.0, 5.0)
    

plt.plot(x, weibull)
plt.show()