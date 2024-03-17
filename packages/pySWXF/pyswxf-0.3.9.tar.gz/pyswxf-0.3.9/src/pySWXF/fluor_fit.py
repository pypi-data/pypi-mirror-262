# -*- coding: utf-8 -*-
"""
multilayer_fluor_fit

file to fit fluorescence from bilayer on top of multilayer

Created on Tue Mar 14 13:50:10 2023
Code to generate multilayer sample simulation


@author: lluri
"""
import scipy.constants as scc
from pySWXF.refl_funs import reflection_matrix, standing_wave 
from pySWXF.xray_utils import eden_to_rho
from lmfit import Model
from scipy.special import erf
import numpy as np
import time
import xraydb as xdb
import scipy.constants as scc
#%% Imports and configuration section
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 12:40:26 2023

@author: th0lxl1
"""
#%%
def make_bilayer_model():
    Head = 'CH2'
    Tail = 'CH2'
    Methyl = 'CH2'
    rho_head = eden_to_rho(Head, 486/scc.nano**3)
    rho_tail = eden_to_rho(Tail, 323/scc.nano**3)
    bilayer_layers = [(Head,rho_head,7,3.17),            # Water                                                                          
              (Tail,rho_tail,17.23,3.17),       # Distal Acyl Chain
              (Methyl,0,2,3.17),                # Methyl Overlap Region
              (Tail,rho_tail,17.63,2.6),         # Proximal Acyl Chain
              (Head,rho_head,7,2.6)]           # Proximal Head Group
    return bilayer_layers
#%%

def sample_sim(G,D,sig_Mo,sig_Si,overlay,
               sig_Si_top,water,bilayer,
               D_Ti=108.2,sig_Ti=3.0,D_SiO2=10,sig_SiO2=3,D_SiO2_Bot=30,
               sig_SiO2_Bot=3,sig_Si_Bot=3, **kwargs):
    if water:
        layers = [('H2O',1.0,0,0)]  
        if bilayer:
            layers += make_bilayer_model()
    else:
        layers = [('N2',1.225e-3,0,0)]
    layers += [('SiO2',eden_to_rho('SiO',692e27),D_SiO2,sig_SiO2),
    ('SiO',eden_to_rho('SiO',560e27),1.5,1.5,),
    ('Si',xdb.atomic_density('Si'),overlay,sig_Si_top)]
    nstack = 20
    rMo = xdb.atomic_density('Mo')
    rSi = xdb.atomic_density('Si')
    for i in range(nstack):
        layers += [('Mo',rMo,D*G,sig_Mo),
                       ('Si',rSi,D*(1-G),sig_Si)]
    layers += [('Ti',xdb.atomic_density('Ti'),D_Ti,sig_Ti), 
                   ('SiO2',2.2,D_SiO2_Bot,sig_SiO2_Bot),
                   ('Si',xdb.atomic_density('Si'),0,sig_Si_Bot)]
    return layers

def multilayer_ref_Ti(theta,I0,thoff,
                   bg,foot,G,D,sig_Mo,sig_Si,overlay,
                   sig_Si_top,water,
                   Energy,bilayer,res,D_Ti,sig_Ti,D_SiO2,sig_SiO2,
                   D_SiO2_Bot,sig_SiO2_Bot,sig_Si_Bot):
    if res == 0:
        norm = 1
        nspan = 1
        dth_span = [0]
        mul = [1]
        # print('multilayer_ref_Ti: bypassing resolution')
    else:
        nspan = 8
        dth_span = np.linspace(-2*res,2*res,nspan)
        mul = np.exp(-dth_span**2/2/res**2)
        norm = np.sum(mul)
        # print('resolution = {0:7.2f} nspan = {1:d}'.format(res,nspan))
    vals = locals()
    tic = time.time()
    result_list = []
    for i in range(nspan):
        dth = vals['dth_span'][i]
        alpha = (vals['theta'] - vals['thoff'] + dth)*scc.degree
        layers = sample_sim(G,D,sig_Mo,
                sig_Si,overlay,
                sig_Si_top,water,bilayer,
                D_Ti = D_Ti, sig_Ti = sig_Ti,
                D_SiO2 = D_SiO2,sig_SiO2=sig_SiO2,
                D_SiO2_Bot = D_SiO2_Bot, sig_SiO2_Bot = sig_SiO2_Bot,
                sig_Si_Bot = sig_Si_Bot)
        t,r,kz,_,_,_,zm = reflection_matrix(
            alpha,Energy,layers)
        Intensity = np.abs(r[:,0])**2
        frange = theta<foot
        Intensity[frange] *= theta[frange]/foot
        tres = Intensity*mul[i]/norm
        result_list.append(tres)       
    toc = time.time()
    #print(f'{toc-tic:2.1f} ',end='')
    return(I0*np.sum(np.array(result_list),0)+bg)


def multilayer_fluor(theta,I0,thoff,
                   bg,foot,G,D,sig_Mo,sig_Si,overlay,
                   sig_Si_top,sep,hoff,res,
                   Energy):
    water = True
    bilayer = True 
    D_bilayer = 50.86
    if res == 0:
        norm = 1
        nspan = 1
        dth_span = [0]
        mul = [1]
    else:
        nspan = 4
        dth_span = np.linspace(-1.5*res,1.5*res,nspan)
        mul = np.exp(-dth_span**2/2/res**2)
        norm = np.sum(mul)
    for i in range(nspan): 
        dth = dth_span[i]
        alpha = (theta-thoff+dth)*scc.degree 
        layers = sample_sim(G,D,sig_Mo,sig_Si,overlay,
                sig_Si_top,water,bilayer)
        t,r,kz,_,_,_,zm = reflection_matrix(alpha,Energy,layers)
        heights = np.array([sep/2,-sep/2])+hoff - D_bilayer/2
        I,E = standing_wave(heights*scc.angstrom,t,r,kz,zm)
        I = np.average(I,0)
        I /= (theta-thoff)
        I *= np.mean(theta)*I0
        if i==0:
            Itot = I*mul[i]/norm
        else:
            Itot += I*mul[i]/norm 
    Itot[(theta-thoff)<foot] *= (theta-thoff)[(theta-thoff)<foot]/foot
    Itot += bg
    print('.',end='')
    return Itot

def get_prof(amp, zcen, sig):
    '''
    get_prof(zcen, amp, sig)
    function to return real space profile from
    arrays of zcenters, amplitudes and widths
    '''
    zspan = max(zcen) - min(zcen)
    zmin = min(zcen)-2*zspan
    zmax = max(zcen) +2*zspan
    zrange = linspace(zmin, zmax, 2**10)
    prof = zrange*0
    for thisz, thisa, thiss in zip(zcen, amp, sig):
        prof += thisa*exp(-(zrange-thisz)**2/2/thiss**2)
    return zrange, prof

def get_dprof(amp, zcen, sig):
    '''
    get_prof(zcen, amp, sig)
    function to return real space profile from
    arrays of zcenters, amplitudes and widths
    '''
    zspan = max(zcen) - min(zcen)
    zmin = min(zcen)-2*zspan
    zmax = max(zcen) +2*zspan
    zrange = linspace(zmin, zmax, 2**10)
    prof = zrange*0
    lasta = amp[0]
    prof = np.abs(prof) + lasta
    for  thisz, thisa, thiss  in zip(zcen, amp[1:], sig):
        prof += (thisa-lasta)*(erf((thisz-zrange)/thiss)+1)/2
        lasta = thisa
    return zrange, prof

def get_realspace(params,E0):
    D_H = params['D_H'].value
    D_B = params['D_B'].value
    D_M = params['D_M'].value
    D_A = (D_B -2*D_H-D_M)/2
    rho_H = params['rho_H'].value
    rho_A = params['rho_A'].value
    sig = params['sig'].value
    sig_SiO2 = params['sig_SiO2'].value
    zcen, sig_i, layers = get_layers(sig_SiO2,rho_H,rho_A,D_A,D_H,D_M,sig)
    amp = []
    for lay in layers:
        amp = np.append(amp,rho_to_rhoe(lay[0],lay[1],E0)*scc.angstrom**3)
    zrange, prof = get_dprof(amp, zcen, sig_i)
    return zrange, prof,amp,zcen,sig_i,layers



multilayer_model_Ti = Model(multilayer_ref_Ti, independent_vars=['theta','Energy','water','bilayer'])
fluor_model = Model(multilayer_fluor, independent_vars=['theta','Energy'])


  

    