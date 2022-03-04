import time
from collections import deque

T = int(1e5)

st = time.time()
for i in range(T):
    x = []
print(time.time() - st)

st = time.time()
for i in range(T):
    x = deque()
print(time.time()-st)