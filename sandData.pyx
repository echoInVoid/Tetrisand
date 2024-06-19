# cython: boundscheck=False, wraparound=False, initializedcheck=False

from sand import *
from settings import setting

import numpy as np

# cdef class SandsData:
#     data : np.ndarray
#     cdef int w, h

#     def __cinit__(self):
#         self.w, self.h = setting.sandListSize
#         self.data = np.zeros(setting.sandListSize, dtype=np.int8)
#         self.reset()
    
#     cpdef reset(self):
#         cdef int i, j
#         for i in range(self.w):
#             for j in range(self.h):
#                 self.data[i, j] = 0
    
#     def __getitem__(self, row: int) -> Sand:
#         class Proxy:
#             def __init__(self, parent: SandsData, index):
#                 self.parent = parent
#                 self.index = index
#             def __getitem__(self, index) -> Sand:
#                 return SANDS[self.parent.data[self.index, index]]
#             def __setitem__(self, index, s: Sand) -> None:
#                 self.parent.data[self.index, index] = s.id
        
#         return Proxy(self, row)

# cdef sand_t = np.dtype(
#     [
#         ("type", np.int8),
#         ("color", "S8")
#     ]
# )

sands = np.empty(setting.sandListSize, dtype=object)

def resetSand():
    global sands
    cdef int i, j
    for i in range(setting.sandListSize[0]):
        for j in range(setting.sandListSize[1]):
            sands[i][j] = VOID

resetSand()