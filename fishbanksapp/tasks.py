from celery import shared_task
from django.db.models import F
from .models import FishSpecies, Profile, Ship, Invoice, InGameTime, Harbor
from fishbanks.settings import POPULATION_UPDATE_INTERVAL
from django.contrib.auth.models import User
import numpy as np


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
    t = InGameTime.objects.first()
    current_time = t.formatTime(t.getTime())


    for user in User.objects.all():
        items = {}
        costs = {}
        ships = Ship.objects.all().filter(owner=user)
        for ship in ships:
            if ship.harbor == None:
                break
            fish_type = FishSpecies.objects.get(harbor=ship.harbor)
            total_fish = float(ship.fishing_rate) * float(fish_type.population)

            if total_fish > ship.fishing_capacity:
                total_fish = ship.fishing_capacity
            fish_type.population -= total_fish
            fish_type.save()

            revenue = total_fish * float(fish_type.weight) * float(fish_type.value)
            items[f'{fish_type.name} catch from {ship.nickname}'] = revenue
            costs[f'gas for {ship.nickname}'] = 0
            costs[f'worker salaries for {ship.nicknam}'] = 3 * ship.fishing_capacity

        invoice = Invoice.objects.create(user=user, revenues=items, costs=costs, date=current_time)
        user.profile.balance += invoice.getProfit()
        user.save()
    
