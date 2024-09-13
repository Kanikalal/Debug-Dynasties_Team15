from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import pandas as pd
from .models import Workout

class DashboardDataView(View):
    @method_decorator(login_required)
    def get(self, request):
        # Query user's workout data
        workouts = Workout.objects.filter(user=request.user)

        # Convert data to DataFrame
        df = pd.DataFrame(list(workouts.values('date', 'exercise_type', 'duration_minutes', 'calories_burned')))

        # Process data
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        progress = {
            'total_workouts': df.shape[0],
            'total_calories_burned': df['calories_burned'].sum(),
            'workout_frequency': df.resample('W').size().to_list(),  # Weekly frequency
            'calories_burned_over_time': df.resample('W').sum()['calories_burned'].to_list(),  # Weekly calories burned
        }

        return JsonResponse(progress)

# Define the URL pattern for the API endpoint
from django.urls import path
urlpatterns = [
    path('api/dashboard/', DashboardDataView.as_view(), name='dashboard_data'),
]
