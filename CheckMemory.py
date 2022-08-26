import numpy as np
import os
import psutil
import gc
from memory_profiler import profile
 
@profile
def test():
    a=np.full(shape=(600, 700), fill_value=99.0)
    return a
 
if __name__ == '__main__':
 
    a=test()
 
    print('A：%.2f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
    del a
    gc.collect()
    print('B：%.2f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))