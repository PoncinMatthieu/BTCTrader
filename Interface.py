
from Engine import Engine
from Market import Market

class Interface(Engine):
    def __init__(self):
        Engine.__init__(self, 0.0333333) # 1/30 --> 30 frame per seconds

    def Execute(self, elapsedTime):
        # do nothing
        p = 1

