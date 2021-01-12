#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 13:21:10 2021

@author: hydrogen
"""

from numpy.random import choice
import matplotlib.pyplot as plt
import numpy as np

''''First we'll create a class which is a market event. This will make this programme much more modular 
since you can append more events later and then the normalization for the probability will adjust accordingly'''

class marketEvent:
    def __init__(self, weight, jump):
        self.weight = weight
        self.jump = jump
     
    
    def props(self):
        print("Jump:", self.jump, " Weight:", self.weight)

'''Now here's a collation of some simple events, just growth and decline, big growth and big decline'''

g=marketEvent(10,1)
d=marketEvent(10,-1)
c=marketEvent(1,-100)
b=marketEvent(2,50)

marketevents = [g,d,c,b]

'''Some useful auxiliary functions for calculations later that select and do an averaging. Average for recentAvg was 4 originally'''
def normConst(events):
    return sum([event.weight for event in events])
        
def randomSelect(events):
    total=normConst(events)
    return choice([event.jump for event in events], 1,
              p=[event.weight/total for event in events])

def recentAvg(listVals,n):
    return sum([i for i in listVals[-n:]])/n

def plotMarket(N,events):
    i=1
    value=0
    T=[i]
    V=[value]
    while(i < N):
        value+=randomSelect(marketevents)
        #Iterator
        i+=1
        #Lists of the interval and the values for each part of the interval
        T.append(i)
        V.append(value[0])
    plt.plot(T,V)
    
def investMarket(N,events):
    principal=10000
    quantity=0
    i=0
    value=5000
    C=[]
    T=[i]
    V=[value]
    while(i < N):
        value+=randomSelect(marketevents)
        
        #Iterator
        i+=1
        #Lists of the interval and the values for each part of the interval and the changes, C
        T.append(i)
        V.append(value[0])
        C.append(V[i]-V[i-1])
        
        #Define the if statements for buying and selling. Only kicks in after fifth to give some sampling
        if i>5:
            #Buying
            if recentAvg(C) < 0 and principal - V[-1] > 0:
                principal+=-V[-1]
                quantity+=1
            #Selling
            if recentAvg(C) > 0 and quantity > 0:
                principal+=V[-1]
                quantity-=1
    plt.plot(T,V)
    print("Final balance", principal/10000, ", Quantity of stock", quantity)
    print("Total liquidated assets", (principal + quantity*V[-1])/10000)
'''Future idea, make it so there is a fixed supply of the stock and when its purchased more 
its price will rise accordingly. Also add more "investors" if you can'''

'''This next part is running statistics on several iterations of the basic ifvestor to see what the behaviour is like
statistically. Generally, the histogram is peaked around 1 with an upper limit of just over 1.05 and a lower limit of bigger than 0.85 
when the market runs for 50 iterations. However, of the iterations run so far, the average still appears 
to be greater than 1 (but by such a small amount it is most likely 1.)
'''
def investMarketStats(N,events,averagen):
    principal=10000
    quantity=0
    i=0
    value=5000
    C=[]
    T=[i]
    V=[value]
    while(i < N):
        value+=randomSelect(marketevents)
        
        #Iterator
        i+=1
        #Lists of the interval and the values for each part of the interval and the changes, C
        T.append(i)
        V.append(value[0])
        C.append(V[i]-V[i-1])
        
        #Define the if statements for buying and selling. Only kicks in after fifth to give some sampling
        if i>averagen+1:
            #Buying
            if recentAvg(C,averagen) < 0 and principal - V[-1] > 0:
                principal+=-V[-1]
                quantity+=1
            #Selling
            if recentAvg(C,averagen) > 0 and quantity > 0:
                principal+=V[-1]
                quantity-=1
    return (principal + quantity*V[-1])/10000

def histogramPerformance(total, length, events,spacing,averagen):
    stats=[]
    for i in range(total):
        stats.append(investMarketStats(length,events,averagen))
    plt.hist(stats, bins = np.arange(0.8,1.2,spacing))
    plt.show()
    print("The mean is:", np.average(stats), ", The standard deviation is", np.std(stats))
    





