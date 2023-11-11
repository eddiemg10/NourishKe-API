
class Fact():
    name: str
    bmi: float
    pal: str
    eer: float

    def __init__(self, patient):
        self.name = patient['name']
        self.bmi = patient['bmi']
        self.pal = patient['pal']
        self.eer = patient['eer']
        
