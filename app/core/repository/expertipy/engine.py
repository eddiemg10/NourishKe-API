from app.core.repository.expertipy.facts.fact import Fact
from app.core.repository.expertipy.rules.rule import *

def recommend():
    # Build a fact
    patient = {
        "name": "Eddie",
        "bmi" : 23,
        "pal" : "very active",
        "eer" : 2700
    }
    fact = Fact(patient)

    # test -> If bmi is between 20 and 30 and eer is less greater than 2650 then recommend foods high in energy
    ant1 = Antecedent(value=fact.bmi, operation=Operation.between , reference=[20, 30])
    ant2 = Antecedent(value=fact.eer, operation=Operation.greater , reference=2650)
    cons1 = Consequent({"energy": "high"})

    rule = ProductionRule(antecedents=[ant1, ant2], consequents=[cons1])
    return rule.execute()