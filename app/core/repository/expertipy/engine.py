from app.core.repository.expertipy.facts.fact import Fact
from app.core.repository.expertipy.rules.rule import *
from app.core.repository.expertipy.kb.kb import KB

def recommend():
    # Build a fact

    patient =   {
    "height": 180,
    "weight": 65,
    "bmi": 23,
    "age": 19,
    "location": "coast",
    "pal": "active",
    "eer": 2500.6,
    "HbA1C": {
      "value": 120,
      "units": "mg/dL"
    },
    "blood_sugar_history": [
      {
        "value": 120,
        "units": "mg/dL",
        "test": "random",
        "date": "2023-11-18T16:27:36.309Z"
      }
    ],
    "blood_sugar_level": "normal",
    "cuisine": [
      "indian"
    ],
    "exclude": [
      "meat"
    ],
    "_id": "string"
  }
    fact = Fact(patient)

    # test -> If bmi is between 20 and 30 and eer is less greater than 2650 then recommend foods high in energy
    # ant1 = Antecedent(value=fact.bmi, operation=Operation.between , reference=[20, 30])
    # ant2 = Antecedent(value=fact.eer, operation=Operation.greater , reference=2650)

    # cons1 = Consequent({"energy": "high"})

    # rule = ProductionRule(antecedents=[ant1, ant2], consequents=[cons1], logic="OR")
    query = []
    knowledge_base = KB(fact)
    rules = knowledge_base.build()
    for rule in rules:
        
        query.append(rule.execute())
    return query