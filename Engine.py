
import time
from time import gmtime, strftime
import traceback
from collections import deque
from threading import Thread, Lock

import Globales
from Clock import Clock

class Engine:
    def __init__(self, engineName, btcTrader, refreshRate):
        self.engineName = engineName
        self.btcTrader = btcTrader
        self.refreshRate = refreshRate
        self.messages = deque()
        self.messagesMaxNumber = 1000
        self.commands = {}
        self.commands["help"] = Engine.CommandHelp
        self.commandList = deque()
        self.commandMutex = Lock()

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
                self.ExecuteCommands()
                self.Execute(elapsedTime)
                elapsedTime = self.LimitFrameRate(clock)
            except:
                Globales.Log("Error in engine: " + self.engineName + "\n")
                t = traceback.format_exc()
                Globales.Log(t + "\n")
                lines = t.split("\n")
                for l in lines:
                    self.PushMsg(l)
        self.CleanUp()

    def Initialize(self):
        print("Method to redefine!")

    def Execute(self, elapsedTime):
        print("Method to redefine!")

    def CleanUp(self):
        print("Method to redefine!")

    def PushMsg(self, m):
        if len(self.messages) > self.messagesMaxNumber:
            self.messages.popleft()
        s = strftime("[%Y-%m-%d %H:%M:%S] - ", gmtime())
        s += m
        Globales.Log(self.engineName + " " + s + "\n")
        self.messages.append(s)

    def GetDescription(self):
        desc = []
        desc.append("Name : " + self.engineName)
        return desc

    def CommandHelp(self, args):
        for c in self.commands.items():
            self.PushMsg(" - " + c[0])

    def ExecuteCommands(self):
        self.commandMutex.acquire()
        try:
            for c in self.commandList:
                self.ExecuteCommand(c)
        except:
            t = traceback.format_exc()
            Globales.Log(t + "\n")
            lines = t.split("\n")
            for l in lines:
                self.PushMsg(l)
        finally:
            self.commandMutex.release()
        self.commandList = deque()

    def ExecuteCommand(self, c):
        self.PushMsg(">" + c)
        argv = c.split()
        found = 0
        for m in self.commands.items():
            if m[0] == argv[0]:
                found = 1
                m[1](self, argv[1:])
        if found == 0:
            self.PushMsg("Error: Unknown command.")

    def PushCommand(self, c):
        self.commandMutex.acquire()
        self.commandList.append(c)
        self.commandMutex.release()
