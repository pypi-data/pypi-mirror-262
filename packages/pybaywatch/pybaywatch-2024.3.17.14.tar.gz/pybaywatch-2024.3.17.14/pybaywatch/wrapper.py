'''
Wrappers for BAYWATCH in Matlab
@author: Feng Zhu (fengzhu@ucar.edu)
'''

import os
import numpy as np
import oct2py
from . import utils
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
    params_path = os.path.join(dirpath, f'ModelOutput/Output_SpatAg_{type}/params_{mode}.mat')
    os.makedirs(os.path.dirname(params_path), exist_ok=True)
    if not os.path.exists(params_path):
        utils.download(utils.data_url_dict[f'TEX_forward_{type}_params_{mode}'], params_path)
        utils.p_success(f'>>> Downloaded file saved at: {params_path}')

    if mode == 'analog':
        if tolerance is None:
            raise ValueError('`tolerance` should be specified when `mode=analog`.')

        params_path = os.path.join(dirpath, f'ModelOutput/Data_Input_SpatAg_{type}.mat')
        if not os.path.exists(params_path):
            utils.download(utils.data_url_dict[f'TEX_forward_{type}_Data_Input'], params_path)
            utils.p_success(f'>>> Downloaded file saved at: {params_path}')

    oc = oct2py.Oct2Py(temp_dir=dirpath)
    oc.addpath(dirpath)
    oc.eval(f"rng({seed})")
    texPosterior = oc.feval('TEX_forward', lat, lon, temp, type, mode, tolerance)
    oc.exit()
    return texPosterior

