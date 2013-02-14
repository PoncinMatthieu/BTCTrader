
import time

class Clock:
    def __init__(self):
        self.Reset()

    def Reset(self):
        self.startTime = time.time()

    def ElapsedTime(self):
        return time.time() - self.startTime
