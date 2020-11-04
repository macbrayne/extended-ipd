from ipd import *
from extended_strategies import *


def run_tournament(bag):
    t = Tournament(g, bag, length=10)  # default: length=1000
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
#bag = [tester, hard]
#t = run_tournament(bag)
#plot_eco(t)

m = Meeting(g, tester, hard, 10)
m.run()