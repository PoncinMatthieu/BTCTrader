
import time

import Globales
from Clock import Clock

class Engine:
    def __init__(self, refreshRate):
        self.refreshRate = refreshRate

    def LimitFrameRate(self, clock):
        elapsedTime = clock.ElapsedTime()
        clock.Reset()
        if self.refreshRate > 0:
            sleepingTime = self.refreshRate - elapsedTime
            if sleepingTime > 0:
                time.sleep(sleepingTime)
            return self.refreshRate
        return elapsedTime

    def Run(self):
        clock = Clock()
        elapsedTime = 0
        self.Initialize()
        while Globales.stopBot == 0:
            try:
                self.Execute(elapsedTime)
                elapsedTime = self.LimitFrameRate(clock)
            except:
                print("Error in market: " + self.apiName)
                print(traceback.format_exc())
        self.CleanUp()

    def Initialize(self):
        print("Method to redefine!")

    def Execute(self, elapsedTime):
        print("Method to redefine!")

    def CleanUp(self):
        print("Method to redefine!")

