# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 12:16:10 2024

@author: vreugdjd
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy.interpolate import griddata
import streamlit as st

def PlotContour(x,y,z,title,xi,yi):
    fig, ax = plt.subplots()
    p1 = ax.tripcolor(x,y,z,cmap=plt.cm.jet, shading='gouraud')
    ax.plot(xi,yi,'--w')
    
    PV = (np.max(z) - np.min(z)) * 1E9
    SFE = np.std(z) * 1E9
    
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.title(title + f'\n PV = {PV:.1f} [nm] \n SFE = {SFE:.1f} [nm RMS]')
    ax.set_aspect('equal', 'box')
    fig.colorbar(p1)
    plt.tight_layout()
    
    
    
    return fig

with st.sidebar:
    st.write('Influence Functions Keck')
    IF_set = st.radio('select IF set:',['2262 actuators','3774 actuators'])
    
    n_max = int(IF_set[0:4])
    
    n = st.slider('# IF function set',1 , n_max)

if n_max == 2262:
    file = 'Keck_2262actuators.fits'
else:
    file = 'Keck_3774actuators.fits'
    
hdul = fits.open(file)

data = hdul[0].data

x = data[:,0]
y = data[:,1]

IFfunction = data[:,n+1]

maxF = np.max(IFfunction)
pos = np.where(IFfunction==maxF)
print(f'max value = {maxF}')
print(f'pos = {pos}')

locx = x[pos[0][0]]
locy = y[pos[0][0]]

angle = np.arctan2(locy,locx)
np.arctan2(-4,4)
print(f'angle = {angle/np.pi*180} [deg]')

R = np.linspace(0,723.19E-3,1000)
xi = R*np.cos(angle)
yi = R*np.sin(angle)

fig = PlotContour(x,y,IFfunction,file + '\n' + f'IF# = {n}',xi,yi)
st.pyplot(fig)

dzi = griddata((x,y),IFfunction,(xi,yi))

fig2,ax = plt.subplots()
ax.plot(R,dzi)
ax.set_xlabel('mirror Radius [m]')
ax.set_ylabel('Influence Function [m]')
ax.grid(True)
st.pyplot(fig2)