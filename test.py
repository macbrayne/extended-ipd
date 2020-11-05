from ipd import *
from extended_strategies import *
from pour_la_science import First, Second, Third


def run_tournament(bag):
    t = Tournament(g, bag, length=1000)  # default: length=1000
    t.run()
    print(t.matrix)
    return t


def plot_eco(t):
    e = Ecological(t)  # default: pop=100
    e.run()
    e.drawPlot()


# bag=[Periodic("D"), HardMajority(), Tft(), Spiteful(),  Gradual()]
# bag=[Periodic("C"), Periodic("D"), Tft(), Periodic("CCD")]
"""
First tournament
"""
tester = Tester4()
hard = Hard()
tft = TftWithThreshold(g)
first = First(g)
second = Second(g)
third = Third()

bag = [first, second, hard, tft, tester, third]
t = run_tournament(bag)
plot_eco(t)

# m = Meeting(g, second, tft, 1000)
# m.run()
# print("Scores: [", m.s1_score, ",", m.s2_score, "]")
