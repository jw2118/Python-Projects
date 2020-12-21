#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 17:14:49 2020

@author: hydrogen
"""

import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#Wavevector and related dispersion factors
k0=1
sk=k0/10
dk=sk/10

#Constants for the dispersion
c=1
d=0.02

#the number for the items in the sum
m0=30

#This lays out all the basic framework for the functions and their values.
def w(k):
    return c*k+d*k**3

def k_m(m):
    return (2*m+1)*k0

def wave_function(x,t):
    P = 0
    for m in range(0,m0+1,1):
        P+=(-1)**m/(2*m+1)*math.cos(k_m(m)*x-w(k_m(m))*t)
    return P

#This part is interested in obtaining the values and plotting them neatly with an animation

def plotfuncx(function,t,x0,xf,dx):
    N=(xf-x0)/dx
    X=[]
    Y=[]
    for i in range(int(N+1)):
        X.append(x0)
        Y.append(function(x0,t))
        x0+=dx
    plt.plot(X,Y)


def animatefunc(function,t0,tf,dt,x0,xf,dx):
    fig = plt.figure()
    k=x0
    plt.axis([x0,xf,-2,2])
    im1, = plt.plot([], [], 'ro')
    N=(xf-x0)/dx
    num_frames=(tf-t0)/dt
    X=[]
    Y=[]
    def func(n):
        x0=k
        X.clear()
        Y.clear()
        for i in range(int(N+1)): 
            X.append(x0)
            Y.append(function(x0,t0+n*dt))
            x0+=dx
        x0=k
        im1.set_xdata(X)
        im1.set_ydata(Y)
        return im1,
    
    animation.FuncAnimation(fig, func,frames=int(num_frames), interval=30, blit=True)
        

#This gives a pretty clear animation: animatefunc(wave_function,0,6,0.001,0,6,0.001)
    