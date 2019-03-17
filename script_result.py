import os
import sys

for i in range(0,1):
    cmd = '%run results.py {0} {1}'.format(i,i+1)
    os.system(cmd)

