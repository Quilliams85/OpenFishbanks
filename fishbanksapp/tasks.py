from celery import shared_task
from django.db.models import F
from .models import FishSpecies

@shared_task
def update_population():
    # Get the population object (assuming there's only one)
    species = FishSpecies.objects.all()

    for fish in species:
        fish.population += 100
        fish.save()