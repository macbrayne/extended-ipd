from ipd import *
from extended_strategies import *
from pour_la_science import First, Second, Third
from strategies import Tft, Periodic, Spiteful, HardMajority


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

tester = Tester4()
hard = Hard()
tft = TftWithThreshold(g)
first = First(g)
second = Second(g)
third = Third()
"""
First tournament
"""
bag = [first, second, hard, tft, tester, third]
t = run_tournament(bag)
plot_eco(t)

"""
Second tournament

Note that Tft, a good strategy from the iterated prisoner's dilemma, does quite well and reaches a stable population
"""
# bag = [first, second, Tft(), Periodic("C"), third]
bag = [first, second, tft, third, Tft(), Periodic("D")]
t = run_tournament(bag)
plot_eco(t)


"""
Third tournament
"""
bag = [first, second, hard, tft, third]
t = run_tournament(bag)
plot_eco(t)