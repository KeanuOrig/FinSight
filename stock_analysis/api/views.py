from django.shortcuts import render
from django.http import JsonResponse
from django.core.management import call_command
from django.http import HttpResponseServerError
from django.core.management import CommandError

# Create your views here.
def create_superuser_and_load_fixtures(request):
    try:
        # Run the custom management command
        call_command('create_superuser_and_load_fixtures')
        return JsonResponse({"status": "success", "message": "Superuser created and fixtures loaded successfully."})
    except CommandError as e:
        return HttpResponseServerError(f"Error: {e}")