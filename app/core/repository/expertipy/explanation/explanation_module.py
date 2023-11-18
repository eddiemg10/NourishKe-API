from app.core.repository.expertipy.facts.fact import Fact

class Explanation():
    """
    Explanation Module
    """
    def __init__(self, text: str, link: str = None):
        self.text = text,
        self.link = link


class ExplanationModule():
    def __init__(self, fact: Fact):
        self.x_15_15_rule = Explanation(
            text=f"Your Blood sugar is {fact.blood_sugar_history[0]}. Since this is between the 55-69 mg/dL range, it is recommended to raise it by following the 15-15 rule: have 15 grams of carbs and check your blood sugar after 15 minutes. If it’s still below your target range, have another serving. Once it’s in range, eat a nutritious meal or snack to ensure it doesn’t get too low again.",
            link="https://www.cdc.gov/diabetes/basics/low-blood-sugar-treatment.html"),
        
        self.x_sport_induced_hypoglycemia = Explanation(
            text=f"Your activity level is  {fact.pal}. This indicates that you are in danger of 'Sport induced Hpoglycemia. This may be because you did not eat low GI food before physically demanding activity and either ate nothing after the activity or ate low GI foods afterwards. Medium GI foods have been recommended as a result since you're diabetic'",
        link="https://www.gifoundation.com/nutrition/low-blood-sugar/#:~:text=Sport%20induced%20Hypoglycemia,a%20lot%20better."),

        self.x_active_person = Explanation(
            text=f"Your activity level ({fact.pal}) indicates you engage in physically demanding tasks"
        ),
