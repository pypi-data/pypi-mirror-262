'''
Wrappers for BAYWATCH in Matlab
@author: Feng Zhu (fengzhu@ucar.edu)
'''

import os
import numpy as np
import oct2py
dirpath = os.path.dirname(__file__)

def TEX_forward_M(lat, lon, temp, seed=2333, type='SST', mode='standard', tolerance=None):
    ''' Wrapper for TEX_forward in Matlab

    args:
        lat (float): latitude
        lon (float): longitude
        temp (float): temperature
        seed (int): random seed
        type (str): temperature type, must be 'SST' or 'subT'
        mode (str): calibration mode, must be 'standard' or 'analog'
        tolerance (float): search tolerance, must be provided when mode is 'analog'
    '''
    oc = oct2py.Oct2Py(temp_dir=dirpath)
    oc.addpath(dirpath)
    oc.eval(f"rng({seed})")
    texPosterior = oc.feval('TEX_forward', lat, lon, temp, type, mode, tolerance)
    oc.exit()
    return texPosterior
