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
    "blood_sugar_level": "hypoglycemic",
    "cuisine": [
      "indian"
    ],
    "exclude": [
      "meat"
    ],
    "_id": "string",
  }
    fact = Fact(patient)

    # test -> If bmi is between 20 and 30 and eer is less greater than 2650 then recommend foods high in energy
    # ant1 = Antecedent(value=fact.bmi, operation=Operation.between , reference=[20, 30])
    # ant2 = Antecedent(value=fact.eer, operation=Operation.greater , reference=2650)

    # cons1 = Consequent({"energy": "high"})

    # rule = ProductionRule(antecedents=[ant1, ant2], consequents=[cons1], logic="OR")
    query = []
    knowledge_base = KB(fact)
    rules = knowledge_base.build(fact)
    visited_rules = set()
    # for rule in rules:
    #     query.append(rule.execute())
    # return query

    ctr = 0
    while ctr < 3:
      rule_triggered = False
      knowledge_base = KB(fact)
      # print(vars(fact), "\n\n")
      rules = knowledge_base.build(fact)
      # print(vars(knowledge_base.fact), "\n\n")
      for rule in rules:
        if rule.evaluate() and rule.id not in visited_rules:
          query_builder, fact = rule.execute()  # Pass the fact to execute method
          visited_rules.add(rule.id)
          print(visited_rules)
          rule_triggered = True
      ctr += 1

      if not rule_triggered:
        print("No match found")
        break
    return query_builder
      