import time

import numpy as np
from numba import njit

#@njit('(float32[:], float64, )')
def mad_median_rule(data: np.ndarray, k: int = 2.0):
    median = np.median(data)
    mad = np.median(np.abs(data - median))
    threshold = k * mad
    #outliers = np.abs(data - median) > threshold
    #return outliers * 1

data = np.random.randint(0, 600, (9000000,)).astype(np.float32)
start = time.time()
mad_median_rule(data=data, k=1.0)
print(time.time() - start)
