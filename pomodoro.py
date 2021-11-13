from globals_ import *
from datetime import datetime
from datetime import timedelta
import time
import math
import threading


class Timer:
 
    def __init__(self):
        self.start = time.time()
        self.fstart = datetime.fromtimestamp(self.start).strftime("%H:%M:%S")
        self.fend = (datetime.strptime(self.fstart, "%H:%M:%S") + timedelta(minutes=25)).strftime("%H:%M:%S")
 
    def start(self):
        self.start = time.time()
 
    def elapsed(self):
        elapsed = time.time() - self.start
        return math.ceil(elapsed)
 
    def milestone(self):
        self.start = time.time()


