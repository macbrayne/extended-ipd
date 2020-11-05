# IPD : the Extended Iterated Prisoner's Dilemma
For more information about the original project visit https://github.com/cristal-smac/ipd

[In their paper[1]](#Reference) the authors proposed an interesting extended version of the iterated prisoner's dilemma.
Unfortunately today no existing project for simulating the prisoner's dilemma has implemented such a variation.
So I adapted the work from the SMAC team and created a version of their library specifically for simulating the extended version the team proposed 26 years earlier.

As a result of using a existing project all classic strategies should remain usable
and are cross-compatible (untested).

## Running the experiments
Running experiments with the extended prisoner's dilemma:
```bash
python ./extended_tests.py
```

Running experiments with the iterated prisoner's dilemma
```bash
python ./classic_tests.py
```

## Strategies

I've implemented the following six strategies from [[1]](#Reference):
* Hard,
* Tester-4,
* Tit-for-Tat-with-Threshold,
* First,
* Second and
* Third

The latter three were the winners of a tournament held in cooperation with Pour La Science, the french version of the monthly Scientific American.

## Using the new strategies
```python
from ipd import *
from extended_strategies import *
from pour_la_science import *

bag=[First(g), Second(g), Third(), Hard(), Tester4(), TftWithThreshold(g)]
t= Tournament(g,bag)        # default: length=1000
e= Ecological(t)            # default: pop=100
e.run()
e.tournament.matrix
e.historic
e.drawPlot()
```

# Reference
[1] Delahaye, J. & Mathieu, P., 1994. ‘Complex Strategies in the Iterated Prisoner's Dilemma’, Proceedings of the 1994 Chaos and Society conference, Hull, Canada, 1st–2nd Juli 1994. pp 283–292.
