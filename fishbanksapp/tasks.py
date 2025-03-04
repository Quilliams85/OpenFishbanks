from celery import shared_task
from django.db.models import F
from .models import FishSpecies, Profile, Ship, Invoice, InGameTime
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
    current_fish_pop = FishSpecies.objects.first().population
    t = InGameTime.objects.first()
    current_time = t.formatTime(t.getTime())


    for user in User.objects.all():
        items = {}
        total_fishing_rate = 0
        for ship_id, quantity in user.profile.ships_list.items():
            ship = Ship.objects.get(id=int(ship_id))  # Fetch the Ship object
            revenue = float(ship.fishing_rate) * float(quantity) * FishSpecies.objects.first().value
            items[ship.name] = revenue
    
        invoice = Invoice.objects.create(user=user, revenues=items, costs={}, date=current_time)
        user.profile.balance += invoice.getProfit()
        user.save()
    
