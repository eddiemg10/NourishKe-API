from locust import HttpUser, task, between

class AppUser(HttpUser):
    wait_time = between(2,5)

    @task
    def index(self):
        self.client.get("/")

    @task
    def get_foods(self):
        self.client.get("/api/v1/foods")

    @task
    def get_users(self):
        self.client.get("/api/v1/users")

    @task
    def get_single_food(self):
        self.client.get("/api/v1/foods/653e871bfe351cbe4120a207")
   
    @task
    def get_single_food_nutrition(self):
        self.client.get("/api/v1/foods/653e871bfe351cbe4120a207/nutrition")

    @task
    def get_food_groups(self):
        self.client.get("/api/v1/foodgroups")

    @task
    def post_eer(self):
        data = {
            "age": 18,
            "height": 180.4,
            "weight": 70,
            "gender": "male",
            "pal": "very active"
        }
        self.client.post("/api/v1/healthmetrics/eer", json=data, headers={"Content-Type": "application/json", "x-api-key": "cqj57WvRcOMHTHiMJIs7JoC2ABJ0RosE"})
    
    @task
    def post_bmi(self):
        data = {
            "height": 180.4,
            "weight": 70
        }
        self.client.post("/api/v1/healthmetrics/bmi", json=data, headers={"Content-Type": "application/json", "x-api-key": "cqj57WvRcOMHTHiMJIs7JoC2ABJ0RosE"})
    
    @task
    def post_blood_sugar(self):
        data = {
            "value": 120,
            "units": "mg/dL",
            "test": "random"
        }
        self.client.post("/api/v1/healthmetrics/bloodsugar", json=data, headers={"Content-Type": "application/json", "x-api-key": "cqj57WvRcOMHTHiMJIs7JoC2ABJ0RosE"})
    
    @task
    def get_food_groups(self):
        self.client.get("/api/v1/locations?lat=0.4&long=39")
    
    @task
    def get_food_groups(self):
        self.client.get("/api/v1/locations")
   
    @task
    def get_profiles(self):
        self.client.get("/api/v1/profiles")