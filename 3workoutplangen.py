from django.http import JsonResponse
from django.views import View
from .models import Exercise, WorkoutPlan

class GenerateWorkoutPlanView(View):
    def post(self, request):
        # Extract user preferences from the request
        fitness_level = request.POST.get('fitness_level')
        equipment = request.POST.get('equipment')
        goals = request.POST.get('goals')  # Add additional logic based on goals if needed

        # Query exercises based on the user's preferences
        exercises = Exercise.objects.filter(
            fitness_level=fitness_level,
            equipment__icontains=equipment
        )

        # Create a workout plan (optional)
        workout_plan = WorkoutPlan.objects.create(user=request.user)
        workout_plan.exercises.set(exercises)

        # Prepare data for response
        exercise_data = [
            {
                'name': exercise.name,
                'description': exercise.description,
                'muscle_group': exercise.muscle_group,
                'image_url': exercise.image_url
            }
            for exercise in exercises
        ]

        return JsonResponse({'exercises': exercise_data})
