from app.core.repository.expertipy.facts.fact import Fact
from app.core.repository.expertipy.rules.rule import *

def recommend():
    # Build a fact
    patient = {
        "name": "Eddie",
        "bmi" : 23,
        "pal" : "very active",
        "eer" : 2600
    }
    fact = Fact(patient)

    # test -> If bmi is between 1 and 10 and eer is less greater than 2650 then recommend food X
    ant1 = Antecedent(value=8, operation=Operation.between , reference=[1, 10])
    ant2 = Antecedent(value=12500, operation=Operation.greater , reference=2650)
    cons1 = Consequent("Recommend Food X")

    rule = ProductionRule(antecedents=[ant1, ant2], consequents=[cons1])
    return rule.execute()