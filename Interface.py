
import string
import curses
import curses.textpad

import Globales
from Engine import Engine
from Market import Market

class Interface(Engine):
    def __init__(self, btcTrader):
        Engine.__init__(self, "Interface", btcTrader, 0.0333333) # 1/30 --> 30 frame per seconds
        self.currentConsole = 0
        self.commandLine = ""
        self.cursorPosition = 0
        self.printset = set(string.printable)
        self.PushMsg("Hola !")
        self.PushMsg("PageUp / PageDown to change of market.")
        self.PushMsg("Type help to see the list of available commands.")

    # create 3 different windows to display:
    # - market list
    # - console
    # - command line
    def Initialize(self):
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.CreateWindows()

    def CreateWindows(self):
        screenSize = self.screen.getmaxyx()
        self.marketList = curses.newwin(int(screenSize[0] / 2), 30, 0, 0)
        self.description = curses.newwin(int(screenSize[0] / 2) + 1, 30, int(screenSize[0] / 2), 0)
        self.console = curses.newwin(screenSize[0] - 3, screenSize[1] - 30, 0, 30)
        self.command = curses.newwin(3, screenSize[1] - 30, screenSize[0] - 3, 30)
        self.command.nodelay(1)
        self.command.keypad(1)
        self.RefreshMarketList()
        self.RefreshCommandLine()
        self.RefreshDescription()

    def Execute(self, elapsedTime):
        currentEngine = self.GetCurrentEngine()
        if currentEngine.newMessages == 1:
            self.RefreshConsoleEngine(currentEngine)
            currentEngine.newMessages = 0
        self.RefreshCommandLine()

    def CleanUp(self):
        curses.endwin()

    def GetCurrentEngine(self):
        if self.currentConsole == 0:
            return self
        else:
            return self.btcTrader.markets[self.currentConsole - 1]

    def RefreshMarketList(self):
        self.marketList.border()
        att = curses.A_NORMAL
        if self.currentConsole == 0:
            att = curses.A_UNDERLINE
        self.marketList.addstr(1, 1, "Interface", att)
        line = 2
        for m in self.btcTrader.markets:
            att = curses.A_NORMAL
            if (self.currentConsole + 1) == line:
                att = curses.A_UNDERLINE
            self.marketList.addstr(line, 1, m.engineName, att)
            line = line + 1
        self.marketList.refresh()

    def RefreshDescription(self):
        self.description.erase()
        self.description.border()
        currentEngine = self.GetCurrentEngine()
        line = 1
        for d in currentEngine.GetDescription():
            self.description.addstr(line, 1, d)
            line += 1
        self.description.refresh()

    def RefreshConsoleEngine(self, e):
        self.console.erase()
        self.console.border()
        size = len(e.messages)
        winsize = self.console.getmaxyx()
        line = winsize[0] - size - 1
        for msg in e.messages:
            if line > 0:
                self.console.addstr(line, 1, msg)
                line += 1
        self.console.refresh()

    def RefreshCommandLine(self):
        self.command.border()
        c = self.command.getch()
        if c != curses.ERR:
            car = chr(c)
            if car == "\n":
                self.GetCurrentEngine().PushCommand(self.commandLine)
                self.commandLine = ""
                self.command.erase()
                self.cursorPosition = 0
            elif c == curses.KEY_NPAGE:
                self.currentConsole = (self.currentConsole + 1) % (len(self.btcTrader.markets) + 1)
                self.RefreshMarketList()
                self.RefreshDescription()
            elif c == curses.KEY_PPAGE:
                self.currentConsole = (self.currentConsole - 1) % (len(self.btcTrader.markets) + 1)
                self.RefreshMarketList()
                self.RefreshDescription()
            elif c == curses.KEY_BACKSPACE:
                if self.cursorPosition > 0:
                    self.cursorPosition -= 1
                    self.commandLine = self.commandLine[:self.cursorPosition] + self.commandLine[self.cursorPosition+1:]
                    self.command.erase()
            elif c == curses.KEY_LEFT:
                if self.cursorPosition > 0:
                    self.cursorPosition -= 1
            elif c == curses.KEY_RIGHT:
                if self.cursorPosition < len(self.commandLine):
                    self.cursorPosition += 1
            elif c == curses.KEY_RESIZE:
                self.CreateWindows()
            elif self.IsPrintable(car):
                self.commandLine = self.commandLine[:self.cursorPosition] + car + self.commandLine[self.cursorPosition:]
                self.cursorPosition += 1
        self.command.addstr(1, 1, self.commandLine)
        self.command.move(1, self.cursorPosition + 1)
        self.command.refresh()

    def IsPrintable(self, c):
        return set(c).issubset(self.printset)
