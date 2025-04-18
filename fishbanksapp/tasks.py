from celery import shared_task
from django.db.models import F
from .models import FishSpecies, Profile, Ship, Invoice, InGameTime, Harbor, Gas, AuctionListing
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

@shared_task
def return_ships():
    t = InGameTime.objects.first()
    current_time = t.getFormattedTime()

    for user in User.objects.all():
        items = {}
        costs = {}
        ships = Ship.objects.all().filter(owner=user)
        none_assigned = True
        for ship in ships:
            if ship.harbor != None:
                none_assigned = False
                fish_type = FishSpecies.objects.get(harbor=ship.harbor)
                total_fish = float(ship.fishing_rate) * float(fish_type.population)

                if (total_fish*fish_type.weight) > ship.fishing_capacity:
                    total_fish = ship.fishing_capacity / fish_type.weight
                fish_type.population -= total_fish
                if fish_type.population < 0:
                    fish_type.population = 0
                fish_type.save()

                revenue = total_fish * float(fish_type.weight) * float(fish_type.value)
                items[f'{fish_type.name} catch from {ship.nickname}'] = revenue
                if Gas.objects.first() != None:
                    costs[f'gas for {ship.nickname}'] = ship.fishing_capacity * Gas.objects.first().price
                costs[f'worker salaries for {ship.nickname}'] = 3 * ship.fishing_capacity
        if not none_assigned:
            invoice = Invoice.objects.create(user=user, revenues=items, costs=costs, date=current_time)
            user.profile.balance += invoice.getProfit()
            user.save()

def update_market_value():
    for species in FishSpecies:
        species.value

@shared_task
def process_ended_auctions():
    AuctionListing.check_ended_auctions()