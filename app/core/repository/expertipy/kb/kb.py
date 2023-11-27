from app.core.repository.expertipy.facts.fact import Fact
from app.core.repository.expertipy.rules.rule import *
from ....schemas.HealthMetrics import PALType
from ..explanation.explanation_module import ExplanationModule


class KB():
    def __init__(self, fact: Fact):
        self.Explanations = ExplanationModule(fact)
        self.query = []
        self.rules = []
        self.fact = fact
        

        # Rule 1: (Hypoglycemia) If Hypoglycemia detected
        self.ant_is_hypoglycemic = Antecedent(value=fact.blood_sugar_level, operation=Operation.equals , reference="hypoglycemic")
        # if person if hypoglycemic, check whether it's sports induced
        self.ant_is_very_active = Antecedent(value=fact.pal, operation=Operation.equals, reference=PALType.very_active) # Sports induced Hypoglycemia
        self.ant_is_active = Antecedent(value=fact.pal, operation=Operation.equals, reference=PALType.active) # Sports induced Hypoglycemia

        self.ant_is_active_individual = Antecedent(value=getattr(self.fact, "is_an_active_person", None), operation=Operation.equals, reference=True)
        
        ###############################################################
        
        self.cons_sports_hypoglycemia = Consequent({
            "explanation" : self.Explanations.x_sport_induced_hypoglycemia,
            "fact_updates" : {"has_sports_hypoglycemia": True},
            "filter": {
                "GI" : ("Medium", fact.blood_sugar_history[0])
            }
        })

        self.cons_active_individual = Consequent({
            "explanation" : self.Explanations.x_active_person,
            "fact_updates" : {"is_an_active_person": True},
        })
               
    
    def build(self, fact):
        self.fact = fact

        # Rule 1: Active or not active?
        self.rules.append(ProductionRule(id=1, query=self.query, fact=self.fact, antecedents=[self.ant_is_very_active, self.ant_is_active], consequents=[self.cons_active_individual], logic=Logic.OR))
        # If active and hypoglycemic, then patient is exposed to sports induced hypoglycmia
        self.rules.append(ProductionRule(id=2, query=self.query, fact=self.fact, antecedents=[self.ant_is_hypoglycemic, self.ant_is_active], consequents=[self.cons_sports_hypoglycemia], logic=Logic.AND))
        return self.rules
