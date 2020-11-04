from strategies import Strategy


class First(Strategy):
    def __init__(self, game):
        super().__init__()
        self.name = "first"
        self.hisPast = ""
        self.myPast = ""
        self.gaveUp = False
        self.game = game
        self.score = 0

        self.period_of_retaliation = 0
        self.retaliation_counter = 0

    def getAction(self, tick):
        # First round
        if tick == 0:
            return "C"

        # Every 20th round
        if tick % 20 == 0:
            # Calculate if average payoff is less than 1.5
            match_length = len(self.myPast)
            average_payoff = self.score / match_length
            if average_payoff < 1.5:  # 1.5 = threshold
                self.gaveUp = True

        if self.gaveUp:
            return "P"

        if self.hisPast[-1] == "D" and self.retaliation_counter == 0:
            # Start retaliation
            self.period_of_retaliation += 1
            self.retaliation_counter = self.period_of_retaliation * (self.period_of_retaliation + 1) / 2 + 2
            print(self.retaliation_counter)

        if self.retaliation_counter > 2:
            self.retaliation_counter -= 1
            return "D"
        if self.retaliation_counter > 0:
            self.retaliation_counter -= 1
            return "C"

        # Normal Tft behaviour
        return "C"

    def clone(self):
        return First(self.game)

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
