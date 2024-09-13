from django.db import models
from django.contrib.auth.models import User

class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    calories = models.PositiveIntegerField()
    protein = models.FloatField()
    carbohydrates = models.FloatField()
    fat = models.FloatField()

    def __str__(self):
        return self.name

class DailyFoodIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    food_items = models.ManyToManyField(FoodItem, through='FoodIntakeDetail')

class FoodIntakeDetail(models.Model):
    daily_food_intake = models.ForeignKey(DailyFoodIntake, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()  # Quantity in grams

    def __str__(self):
        return f'{self.food_item.name} - {self.quantity}g'

class MealRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    recommended_meal = models.TextField()  # JSON or a formatted string for meal suggestions

    def __str__(self):
        return f'{self.user.username} - {self.date}'
