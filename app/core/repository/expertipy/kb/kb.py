from app.core.repository.expertipy.facts.fact import Fact
from app.core.repository.expertipy.rules.rule import *
from ....schemas.HealthMetrics import PALType
from ..explanation.explanation_module import ExplanationModule


class KB():
    def __init__(self, fact: Fact):
        self.Explanations = ExplanationModule(fact)
        self.query = []
        self.rules = []
        # Rule 1: (Hypoglycemia) If Hypoglycemia detected
        self.ant1 = Antecedent(value=fact.blood_sugar_level, operation=Operation.equals , reference="hypoglycemic")
        # if person if hypoglycemic, check whether it's sports induced
        self.ant2 = Antecedent(value=fact.pal, operation=Operation.equals, reference=PALType.very_active) # Sports induced Hypoglycemia
        self.ant3 = Antecedent(value=fact.pal, operation=Operation.equals, reference=PALType.active) # Sports induced Hypoglycemia

        self.cons1 = Consequent({
            "explanation" : self.Explanations.x_sport_induced_hypoglycemia,
            "filter": {
                "GI" : ("Medium", fact.blood_sugar_history[0])
            }
        })

        self.cons2 = Consequent({
            "explanation" : self.Explanations.x_active_person,
        })
               
    
    def build(self):
        # Rule 2: Active or not active?
        self.rules.append(ProductionRule(query=self.query, antecedents=[self.ant2, self.ant3], consequents=[self.cons2], logic=Logic.OR))
        return self.rules
