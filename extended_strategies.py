"""
I defect if the other player cooperates. If he defects once, I give up.
"""
from strategies import Strategy


class Hard(Strategy):
    def __init__(self):
        super().__init__()
        self.name = "hard"
        self.hisPast = ""
        self.myPast = ""
        self.gaveUp = False

    def getAction(self, tick):
        # print("Hard gave up: ", self.gaveUp, " Tester history: ", self.hisPast, " Hard history ", self.myPast)
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
        # print("Tester gave up: ", self.gaveUp)
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
    def __init__(self, game):
        super().__init__()
        self.name = "tft+threshold"
        self.hisPast = ""
        self.myPast = ""
        self.gaveUp = False
        self.game = game
        self.score = 0

    def getAction(self, tick):
        # First round
        if tick == 0:
            return "C"

        # Every 5th round
        if tick % 5 == 0:
            # Calculate if average payoff is above or equals 2
            match_length = len(self.myPast)
            average_payoff = self.score / match_length
            # print("Round: ", match_length, " Payoff: ", average_payoff)
            if average_payoff < 2:  # 2 = threshold
                self.gaveUp = True

        if self.gaveUp:
            return "P"

        # Normal Tft behaviour
        return self.hisPast[-1]

    def clone(self):
        return TftWithThreshold(self.game)

    def update(self, my, his):
        my_payoff = [[payoff[0] for payoff in self.game.scores[0]], [payoff[0] for payoff in self.game.scores[1]],
                     [payoff[0] for payoff in self.game.scores[2]]]
        if his == "C" and my == "C":
            self.score += my_payoff[0][0]
        elif his == "D" and my == "D":
            self.score += my_payoff[1][1]
        elif his == "C" and my == "D":
            self.score += my_payoff[1][0]
        elif his == "P" or my == "P":
            self.score += my_payoff[2][2]
        self.myPast += my
        self.hisPast += his