from collections import OrderedDict
import numpy as np
import os

np.random.seed(0)

HERE = os.path.dirname(os.path.abspath(__file__))

from ytopt.problem import Problem

cmd_frmt = "python " +HERE+"/executable.py"
nparam = 14

for i in range(0, nparam):
    cmd_frmt += f" --p{i} {'{}'}"
problem = Problem(cmd_frmt)

problem.spec_dim(p_id=0, p_space=['a', 'b', 'c'], default='b') #p0_dict
problem.spec_dim(p_id=1, p_space=['a', 'b', 'c'], default='b') #p1_dict
problem.spec_dim(p_id=2, p_space=['a', 'b'], default='b') #P2_dict
problem.spec_dim(p_id=3, p_space=['a', 'b'], default='b') #PF_dict
problem.spec_dim(p_id=4, p_space=['a', 'b'], default='b') #SI_dict
problem.spec_dim(p_id=5, p_space=['a', 'b'], default='b') #SC_dict
problem.spec_dim(p_id=6, p_space=['a', 'b'], default='b') #NT_dict
problem.spec_dim(p_id=7, p_space=['a', 'b'], default='b') #CO_dict
problem.spec_dim(p_id=8, p_space=['a', 'b'], default='b') #TL_dict
problem.spec_dim(p_id=9, p_space=['static', 'dynamic'], default='static') #stat or dyn
problem.spec_dim(p_id=10, p_space=['1', '8', '16'], default='8') #chunk size?
problem.spec_dim(p_id=11, p_space=['1', '2', '4', '8', '14', '16', '28'], default='2') #NT param?
problem.spec_dim(p_id=12, p_space=['1', '2', '3'], default='1') #collapse param
problem.spec_dim(p_id=13, p_space=['32', '64', '128', '256'], default ='128') # tl param?


problem.checkcfg()

if __name__ == '__main__':
    print(problem)
