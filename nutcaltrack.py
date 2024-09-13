from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import DailyFoodIntake, FoodItem, FoodIntakeDetail, MealRecommendation
from .nutrition import get_nutrition_info
import pandas as pd

class LogFoodIntakeView(View):
    @method_decorator(login_required)
    @csrf_exempt
    def post(self, request):
        food_name = request.POST.get('food_name')
        quantity = int(request.POST.get('quantity'))

        # Get nutrition info from Nutritionix API
        nutrition_info = get_nutrition_info(food_name)
        if not nutrition_info:
            return JsonResponse({'error': 'Food item not found'}, status=404)

        # Create or get food item
        food_item, created = FoodItem.objects.get_or_create(
            name=nutrition_info['name'],
            defaults={
                'calories': nutrition_info['calories'],
                'protein': nutrition_info['protein'],
                'carbohydrates': nutrition_info['carbohydrates'],
                'fat': nutrition_info['fat']
            }
        )

        # Log food intake
        daily_intake, created = DailyFoodIntake.objects.get_or_create(user=request.user)
        FoodIntakeDetail.objects.create(
            daily_food_intake=daily_intake,
            food_item=food_item,
            quantity=quantity
        )

        return JsonResponse({'message': 'Food intake logged successfully'})

class NutritionRecommendationView(View):
    @method_decorator(login_required)
    def get(self, request):
        # Example recommendation logic (can be extended)
        recommendations = "Based on your current intake, consider adding more vegetables to your diet."
        MealRecommendation.objects.create(user=request.user, recommended_meal=recommendations)
        
        return JsonResponse({'recommendations': recommendations})

class CalorieTrackingView(View):
    @method_decorator(login_required)
    def get(self, request):
        today = pd.Timestamp.now().normalize()
        daily_intake = DailyFoodIntake.objects.filter(user=request.user, date=today).first()
        if not daily_intake:
            return JsonResponse({'calories': 0})

        total_calories = sum(
            food_item.quantity * food_item.food_item.calories / 100
            for food_item in FoodIntakeDetail.objects.filter(daily_food_intake=daily_intake)
        )

        return JsonResponse({'total_calories': total_calories})
