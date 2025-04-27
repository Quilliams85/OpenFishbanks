from celery import shared_task
from django.db.models import F
from .models import FishSpecies, Profile, Ship, Invoice, InGameTime, Harbor, Gas, AuctionListing
from fishbanks.settings import POPULATION_UPDATE_INTERVAL
from django.contrib.auth.models import User
import numpy as np
import random


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

    species_fished = {}

    for user in User.objects.all():
        items = {}
        costs = {}
        ships = Ship.objects.all().filter(owner=user)
        none_assigned = True
        for ship in ships:
            if ship.harbor != None:
                none_assigned = False
                fish_types = FishSpecies.objects.filter(harbor=ship.harbor)
                for fish_type in fish_types:


                    total_fish = (float(ship.fishing_rate) / float(fish_type.weight)) * ((float(fish_type.population) / float(fish_type.C)) ** 2)

                    if (total_fish*fish_type.weight) > ship.fishing_capacity:
                        total_fish = ship.fishing_capacity / fish_type.weight
                    fish_type.population -= total_fish
                    if fish_type.population < 0:
                        fish_type.population = 0
                    fish_type.save()

                    if species_fished[f'{fish_type.name}'] == None:
                        species_fished[f'{fish_type.name}'] = total_fish
                    else:
                        species_fished[f'{fish_type.name}'] += total_fish

                    revenue = total_fish * float(fish_type.weight) * float(fish_type.value)
                    items[f'{fish_type.name} catch from {ship.nickname}[{ship.id}]'] = revenue

                if Gas.objects.first() != None:
                    costs[f'gas for {ship.nickname}'] = ship.fishing_capacity * Gas.objects.first().price
                costs[f'worker salaries for {ship.nickname}'] = 1 * ship.fishing_capacity
                costs[f'harbor fee for {ship.nickname} @ {ship.harbor.name}'] = ship.harbor.storage_fee
        if not none_assigned:
            invoice = Invoice.objects.create(user=user, revenues=items, costs=costs, date=current_time)
            user.profile.balance += invoice.getProfit()
            user.save()

    update_market_value(species_fished)

def update_market_value(dict):
    total_fish = 0
    fluctuation_constant = 0.1
    if dict != None:
        for fish in dict:
            total_fish += dict[fish]
    
    for species in FishSpecies:
        prop = dict[f'{species.name}'] / total_fish
        species.value /= ((1 + prop*fluctuation_constant) * random.uniform(0.9,1.112))
        species.save()

@shared_task
def process_ended_auctions():
    AuctionListing.check_ended_auctions()

