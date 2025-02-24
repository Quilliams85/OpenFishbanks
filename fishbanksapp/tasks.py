from celery import shared_task
from django.db.models import F
from .models import FishSpecies, Profile, Ship
from fishbanks.settings import POPULATION_UPDATE_INTERVAL
from django.contrib.auth.models import User


@shared_task
def update_population():
    # Get the population object (assuming there's only one)
    species = FishSpecies.objects.all()

    for fish in species:
        new_pop = float(fish.population) * float(fish.k) * (1 - (float(fish.population) / float(fish.C))) * float(POPULATION_UPDATE_INTERVAL)
        fish.population += int(new_pop)
        fish.save()
""" for fish in species:
        fish.population += 100
        fish.save() """

@shared_task
def return_ships():
    total_fishing_rate = 0
    for user in User.objects.all():
        for ship_id, quantity in user.profile.ships_list.items():
            ship = Ship.objects.get(id=int(ship_id))  # Fetch the Ship object
            total_fishing_rate+= ship.fishing_rate * quantity
        
    print(total_fishing_rate)
    
    
    
