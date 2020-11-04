import itertools
import numpy as np
import collections


class Strategy:
    def setMemory(self, mem):
        pass

    def getAction(self, tick):
        pass

    def __copy__(self):
        pass

    def update(self, x, y):
        pass


"""
I defect if the other player cooperates. If he defects once, I give up.
"""


class Hard(Strategy):
    def __init__(self):
        super().__init__()
        self.name = "hard"
        self.hisPast = ""
        self.myPast = ""
        self.gaveUp = False

    def getAction(self, tick):
        print("Hard gave up: ", self.gaveUp, " Tester history: ", self.hisPast, " Hard history ", self.myPast)
        if tick == 0:
            return "D"

        if self.gaveUp or self.hisPast[-1] != "C":
            self.gaveUp = True
            return "P"
        else:
            return "D"

    def clone(self):
        return Hard()

    def update(self, my, his):
        self.myPast += my
        self.hisPast += his


class Tester4(Strategy):
    def __init__(self):
        super().__init__()
        self.name = "tester-4"
        self.hisPast = ""
        self.myPast = ""
        self.gaveUp = False

    def getAction(self, tick):
        print("Tester gave up: ", self.gaveUp)
        if tick == 0 or tick == 1:
            return "C"
        if tick == 2 or tick == 3:
            return "D"
        if tick == 4:
            defection_rate = (self.hisPast[0] + self.hisPast[1] + self.hisPast[2] + self.hisPast[3]).count("D")
            if defection_rate >= 3:
                self.gaveUp = True

        if self.hisPast[-1] == "P":
            self.gaveUp = True

        if self.gaveUp:
            return "P"
        return "C"

    def clone(self):
        return Tester4()

    def update(self, my, his):
        self.myPast += my
        self.hisPast += his


class TftWithThreshold(Strategy):
    def __init__(self):
        super().__init__()
        self.name = "tft+threshold"
        self.hisPast = ""
        self.myPast = ""
        self.gaveUp = False

    def getAction(self, tick):
        print("Hard gave up: ", self.gaveUp, " Tester history: ", self.hisPast, " Hard history ", self.myPast)
        if tick == 0:
            return "D"

        if self.gaveUp or self.hisPast[-1] != "C":
            self.gaveUp = True
            return "P"
        else:
            return "D"

    def clone(self):
        return Hard()

    def update(self, my, his):
        self.myPast += my
        self.hisPast += his
