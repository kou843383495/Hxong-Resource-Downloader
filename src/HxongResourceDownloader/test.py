import time
from time import sleep

from tqdm import tqdm

total_progress = tqdm(total=10,position=0)
side_progress = tqdm(total= 100,position=1)

for i in range(100):
    side_progress.update(1)
    if i %10 ==0:
        total_progress.update(1)
    time.sleep(1)