from ipd import *
from strategies import *


def run_tournament(bag):
    t = Tournament(g, bag)  # default: length=1000
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
bag = [Periodic("P"), Periodic("D"), Tft(), Periodic("C"), Spiteful()]
t = run_tournament(bag)
plot_eco(t)

"""
Second tournament
"""
bag = [Periodic("CCD"), Periodic("D"), Tft(), Periodic("C"), Spiteful(), SoftMajority()]
t = run_tournament(bag)
plot_eco(t)

"""
Third tournament
"""
bag = [Periodic("D"), Tft(), Spiteful(), HardMajority()]
t = run_tournament(bag)
plot_eco(t)
