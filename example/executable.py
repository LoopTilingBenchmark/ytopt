#!/usr/bin/env python
from __future__ import print_function
import re
import os
import sys
import time
import json
import math
import os
import argparse
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.dirname(HERE)+ '/plopper')
from plopper import Plopper

from numpy import abs, cos, exp, mean, pi, prod, sin, sqrt, sum
seed = 12345
nparams = 3

def create_parser():
    'command line parser'

    parser = argparse.ArgumentParser(add_help=True)
    group = parser.add_argument_group('required arguments')

    for id in range(0, nparams):
        parser.add_argument('--p%d'%id, action='store', dest='p%d'%id,
                            nargs='?', const=2, type=str, default='a',
                            help='parameter p%d value'%id)
    return(parser)

parser = create_parser()
cmdline_args = parser.parse_args()
param_dict = vars(cmdline_args)

p0 = param_dict['p0']
p1 = param_dict['p1']
p2 = param_dict['p2']

x=[p0,p1,p2]

p0_dict = {'a': "8", 'b': "16",'c': "32"}
p1_dict = {'a': "8", 'b': "16",'c': "32",'d': "64"}
p2_dict = {'a': "16",'b': "32",'c': "64",'d':"128"}

dir_path = os.path.dirname(os.path.realpath(__file__))
kernel_idx = dir_path.rfind('/')
kernel = dir_path[kernel_idx+1:]
obj = Plopper(dir_path+'/heat-3d_pragma.c',dir_path)


def plopper_func(x):
    value = [p0_dict[x[0]],p1_dict[x[1]],p2_dict[x[2]]]
    #print('VALUES:',p0_dict[x[0]])
    params = ["P1","P2","P3"]

    result = obj.findRuntime(value, params)

    return result


pval = plopper_func(x)
print('OUTPUT:%f'%pval)
