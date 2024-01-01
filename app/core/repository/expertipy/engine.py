from app.core.repository.expertipy.facts.fact import Fact
from app.core.repository.expertipy.rules.rule import *
from app.core.repository.expertipy.kb.kb import KB
from app.core.repository.food import FoodController, FoodGroupController
from app.core.repository.expertipy.explanation.explanation_module import Explanation
from app.core.database import get_database
from fastapi import Depends


def recommend():
    
   

    # Build a fact

    patient =   {
    "height": 180,
    "weight": 65,
    "bmi": 23,
    "age": 0,
    "gender": "male",
    "coords": (39,-3),
    "pal": {"pal":"active", "value": 2.43},
    "eer": 2500.6,
    # "HbA1C": {
    #   "value": 70,
    #   "units": "mg/dL"
    # },
    "HbA1C": None,
    "blood_sugar_history": [
      {
        "value": 69,
        "units": "mg/dL",
        "test": "fasting",
        "date": "2023-11-18T16:27:36.309Z"
      }
    ],
    # "blood_sugar_level": "hypoglycemic",
    "cuisine": [
      "indian"
    ],
    "exclude": [
      "fish", "meat"
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
    
    cals_from_carbs = carb_percentage/100*fact.eer
    cals_from_protein = protein_percentage/100*fact.eer
    cals_from_fat = fat_percentage/100*fact.eer

    
    # return (carb_percentage, protein_percentage, fat_percentage)

    foods = FoodController.index(page=1, size=600 , db=get_database(), groups=None)
    
    # return query_builder
    FG = FoodGroups()
    food_plan = {}
    number_of_meals = 5
    if number_of_meals == 5:
      kcal_distribution = meal_calory_distribution(number_of_meals, fact.eer)
      breakfast_kcal, morning_snack_kcal, lunch_kcal, afternoon_snack, dinner_kcal = kcal_distribution
      breakfast_filter =  {
      "GI": (0, 85), 
      "group": [FG.beverages, FG.cereals, FG.startchy_roots, FG.fruits], 
      "tags": "breakfast", 
      # "exclude": "1234"
      }
      if fact.age < 1:
        breakfast_filter['group'] = [FG.dairy]
        breakfast_filter['tags'] = "infant"
      print(breakfast_filter)
      breakfast_results = FoodController.filter(get_database(), breakfast_filter)
      food_plan.update({"breakfast": breakfast_results})

      ################################
      groups = [FG.mixed, FG.vegetables, FG.legumes, FG.fruits]
      if "meat" in fact.exclude:
        groups.append(FG.fish)
      if "fish" in fact.exclude:
        groups.append(FG.meats_and_poultry)
    
      main_meal_filter = {
      "GI": (0, 85), 
      "group": [FG.mixed, FG.vegetables, FG.legumes, FG.meats_and_poultry, FG.fruits], 
      "tags": "", 
      "exclude": ["meat"]
      }
      main_meal_results = FoodController.filter(get_database(), main_meal_filter)
      food_plan.update({"main_meal": main_meal_results})
      
      snack_filter = {
      "GI": (0, 85), 
      "group": [FG.dairy, FG.nuts_seeds, FG.vegetables, FG.fruits], 
      "tags": "snack", 
      # "exclude": ["meat"]
      }
      snack_results = FoodController.filter(get_database(), snack_filter)
      food_plan.update({"snacks": main_meal_results})
    else:
      kcal_distribution = meal_calory_distribution(number_of_meals, fact.eer)
      breakfast_kcal, lunch_kcal, dinner_kcal = kcal_distribution


    # filter =  {
    #   "GI": (0, 55), 
    #   # "location": "coast",
    #   "group": "653e83acfe351cbe41209807", 
    #   "tags": "breakfast", 
    #   # "exclude": "1234"
    # }
    # results = FoodController.filter(get_database(), filter)
    return food_plan
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
 



def meal_calory_distribution(number_of_meals, eer):
  kcal_distribution = ()
  if number_of_meals == 3:
    breakfast_kcal = 0.2 * eer
    lunch_kcal = 0.41 * eer
    dinner_kcal = 0.39 * eer
    kcal_distribution = (breakfast_kcal, lunch_kcal, dinner_kcal)
  else:
    breakfast_kcal = 0.18 * eer
    morning_snack_kcal = 0.05 * eer
    lunch_kcal = 0.36 * eer
    afternoon_snack = 0.1 * eer
    dinner_kcal = 0.31 * eer
    kcal_distribution = (breakfast_kcal, morning_snack_kcal, lunch_kcal, afternoon_snack, dinner_kcal)
  
  return kcal_distribution

class FoodGroups():
  def __init__(self):
    self.cereals = "653e83a8fe351cbe412097ed"
    self.startchy_roots = "653e83aafe351cbe412097f0"
    self.legumes = "653e83aafe351cbe412097f3"
    self.vegetables = "653e83aafe351cbe412097f6"
    self.fruits="653e83abfe351cbe412097f9"
    self.dairy="653e83abfe351cbe412097fb"
    self.meats_and_poultry="653e83abfe351cbe412097fd"
    self.fish="653e83abfe351cbe412097ff"
    self.oils_fats="653e83acfe351cbe41209801"
    self.nuts_seeds="653e83acfe351cbe41209803"
    self.sweeteners="653e83acfe351cbe41209805"
    self.beverages="653e83acfe351cbe41209807"
    self.condiments="653e83adfe351cbe41209809"
    self.insects="653e83adfe351cbe4120980b"
    self.mixed = "653e83adfe351cbe4120980d"