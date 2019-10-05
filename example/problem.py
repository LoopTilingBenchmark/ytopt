from collections import OrderedDict
import numpy as np
import os

np.random.seed(0)

HERE = os.path.dirname(os.path.abspath(__file__))

from ytopt.problem import Problem

cmd_frmt = "python " +HERE+"/executable.py"
nparam = 3

for i in range(0, nparam):
    cmd_frmt += f" --p{i} {'{}'}"
problem = Problem(cmd_frmt)
problem.spec_dim(p_id=0, p_space=['a', 'b','c'], default='a')
problem.spec_dim(p_id=1, p_space=['a', 'b','c','d'], default='a')
problem.spec_dim(p_id=2, p_space=['a', 'b','c','d'], default='a')

problem.checkcfg()
if __name__ == '__main__':
    print(problem)
