
import curses

from Engine import Engine
from Market import Market

class Interface(Engine):
    def __init__(self):
        Engine.__init__(self, 0.0333333) # 1/30 --> 30 frame per seconds

    def Initialize(self):
        #self.stdscr = curses.initscr()
        i = 0

    def Execute(self, elapsedTime):
        i = 0 # do nothing

    def CleanUp(self):
        #curses.endwin()
        i = 0
