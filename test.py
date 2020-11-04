from ipd import *
from extended_strategies import *


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

bag = [tester, hard, tft]
t = run_tournament(bag)
plot_eco(t)
