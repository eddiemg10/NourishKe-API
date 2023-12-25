from app.core.repository.expertipy.facts.fact import Fact
from app.core.repository.expertipy.rules.rule import *
from app.core.repository.expertipy.kb.kb import KB
from app.core.repository.food import FoodController, FoodGroupController
from app.core.repository.expertipy.explanation.explanation_module import Explanation

def recommend():
    # Build a fact

    patient =   {
    "height": 180,
    "weight": 65,
    "bmi": 23,
    "age": 19,
    "gender": "male",
    "coords": (39,-3),
    "pal": {"pal":"active", "value": 2.43},
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
    # "blood_sugar_level": "hypoglycemic",
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
    query_builder=[]
    ctr = 0
    while ctr < 4:
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


    sugar_level = getattr(fact, "blood_sugar_level", None)['level']
    carb_percentage, protein_percentage, fat_percentage = getAMDR(query_builder, sugar_level)
    
    carbs_from_calories = carb_percentage/100*fact.eer
    carbs_from_protein = protein_percentage/100*fact.eer
    carbs_from_fat = fat_percentage/100*fact.eer
    
    # return (carb_percentage, protein_percentage, fat_percentage)
    
    return fact
      

def getAMDR(query, sugar_level):
  PROTEIN_AMDR = (10, 35)
  CARBOHYDRATES_AMDR = (45, 65)
  FAT_AMDR = (20, 35)

  if sugar_level == "hypoglycemic":
    CARBOHYDRATES_AMDR = (55, 65)
    PROTEIN_AMDR = (10, 20)

  elif sugar_level == "prediabetic":
    CARBOHYDRATES_AMDR = (50, 55)
    PROTEIN_AMDR = (15, 25)

  elif sugar_level == "diabetic":
    CARBOHYDRATES_AMDR = (45, 50)
    PROTEIN_AMDR = (25, 35)
  else:
    CARBOHYDRATES_AMDR = (50, 65)

  # Adjust individual AMDRs proportionally to ensure they add up to 100%
  carb_percentage = sum(CARBOHYDRATES_AMDR) / 2
  protein_percentage = sum(PROTEIN_AMDR) /2
  fat_percentage = sum(FAT_AMDR) / 2

  return (carb_percentage, protein_percentage, fat_percentage)