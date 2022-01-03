from lib.strategies import Strategy


class BetterFirst(Strategy):
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
            # print(self.retaliation_counter)

        if self.retaliation_counter > 2:
            self.retaliation_counter -= 1
            return "D"
        if self.retaliation_counter > 0:
            self.retaliation_counter -= 1
            return "C"

        # Normal Tft behaviour
        return "C"

    def clone(self):
        return BetterFirst(self.game)

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


class BetterSecond(Strategy):
    def __init__(self, game):
        super().__init__()
        self.name = "better-second"
        self.hisPast = ""
        self.myPast = ""

        self.tickBetrayal = -1

        self.start_value = 5
        self.possible_states = ["tft", "all-c", "spiteful", "periodic-ccd"]
        self.state = 0
        self.state_counter = self.start_value
        self.state_memory = "C"

        self.gaveUp = False
        self.game = game
        self.scores = {"tft": [], "all-c": [], "spiteful": [], "periodic-ccd": []}

    def getAction(self, tick):
        if self.gaveUp:
            return "P"

        result = ""
        # Strategies:
        if self.possible_states[self.state] == "tft":
            # Normal Tft behaviour
            result = "C" if (tick == 0) else self.hisPast[-1]
        elif self.possible_states[self.state] == "all-c":
            # ALL-C behaviour
            result = "C"
        elif self.possible_states[self.state] == "spiteful":
            # Spiteful behaviour
            if self.hisPast[-1] == "D":
                self.state_memory = "D"
            result = self.state_memory
        elif self.possible_states[self.state] == "periodic-ccd":
            # Periodic CCD behaviour
            sequence = "CCD"
            result = sequence[tick % len(sequence)]


        if self.tickBetrayal != -1:
            print(self.tickBetrayal + " " + self.possible_states[self.state])
            self.tickBetrayal += 1
        if tick > 0 and self.hisPast[-1] == "D":
            self.tickBetrayal = 0


        # Try out states
        if self.tickBetrayal != -1 and self.tickBetrayal < 20 and self.state_counter == 0:
            self.state += 1
            self.state_counter = self.start_value
        # Best state or pass
        elif self.tickBetrayal >= 20 and self.state_counter == 0:
            # Average payoff by state
            average_payoff = {}
            for possible_state in enumerate(self.possible_states):
                # print("State:", possible_state[0])
                # print("Score: ", (self.scores[self.possible_states[possible_state[0]]]))
                average_payoff[possible_state] = (sum(self.scores[self.possible_states[possible_state[0]]]) / 4)
            # Passing
            # Calculate if average payoff is less than 1.5
            if max(average_payoff.values()) < 1.5:  # 1.5 = threshold
                self.gaveUp = True
            else:
                # Choose best strategy
                self.state = max(average_payoff, key=average_payoff.get)[0]
                # print("State: ", self.state)
                self.state_counter = 12

        self.state_counter -= 1
        assert result != ""
        return result

    def clone(self):
        return BetterSecond(self.game)

    def update(self, my, his):
        my_payoff = [[payoff[0] for payoff in self.game.scores[0]], [payoff[0] for payoff in self.game.scores[1]],
                     [payoff[0] for payoff in self.game.scores[2]]]
        score_list = self.scores[self.possible_states[self.state]]
        if len(score_list) > 3:
            # print(self.possible_states[self.state], score_list)
            score_list.pop(0)
        if his == "C" and my == "C":
            score_list.append(my_payoff[0][0])
        elif his == "D" and my == "D":
            score_list.append(my_payoff[1][1])
        elif his == "C" and my == "D":
            score_list.append(my_payoff[1][0])
        elif his == "P" or my == "P":
            score_list.append(my_payoff[2][2])
        self.myPast += my
        self.hisPast += his


class BetterThird(Strategy):
    def __init__(self):
        super().__init__()
        self.name = "better-third"
        self.hisPast = ""
        self.myPast = ""
        self.gaveUp = False
        self.score = 0

        self.possible_states = ["calm", "irritated", "furious"]
        self.state = 0
        self.defection_counter = 0
        self.defections_in_a_row = 0
        self.cooperation_counter = 0

    def getAction(self, tick):
        if self.gaveUp:
            return "P"
        # First round
        if tick == 0:
            return "C"

        # Get irritated or furious if not furious
        if self.hisPast[-1:-2].count("D") == 2 and self.possible_states[self.state] != "furious":
            self.state += 1
        elif self.hisPast[-1] == "C" and self.possible_states[self.state] == "irritated":
            self.state -= 1
            return "C"

        if self.possible_states[self.state] == "calm" or self.possible_states[self.state] == "irritated":
            return self.hisPast[-1]
        elif self.possible_states[self.state] == "furious":
            if self.hisPast[-1] == "D":
                self.defections_in_a_row += 1
            elif self.hisPast[-1] == "C":
                self.defections_in_a_row = 0
            if self.defections_in_a_row == 12:
                self.defections_in_a_row = 0
                if self.cooperation_counter < self.defection_counter:
                    self.gaveUp = True
                else:
                    self.state -= 1
                    return "C"
            return "D"
        # Tit for Tat

        if self.gaveUp:
            return "P"
        # Normal Tft behaviour

    def clone(self):
        return BetterThird()

    def update(self, my, his):
        self.myPast += my
        self.hisPast += his
        if his[-1] == "D":
            self.defection_counter += 1
        elif his[-1] == "C":
            self.cooperation_counter += 1
