from celery import shared_task
from django.db.models import F
from .models import FishSpecies, Profile, Ship, Invoice, InGameTime, Harbor, Gas, AuctionListing, ManufacturerShip, Transaction
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
                    species_fished[f'{fish_type.name}'] = species_fished.get(f'{fish_type.name}', 0) + total_fish


                    revenue = total_fish * float(fish_type.weight) * float(fish_type.value)
                    items[f'{fish_type.name} catch from {ship.nickname}[{ship.id}]'] = revenue

                if Gas.objects.first() != None:
                    costs[f'gas for {ship.nickname} [{ship.id}]'] = ship.fishing_capacity * Gas.objects.first().price
                costs[f'worker salaries for {ship.nickname} [{ship.id}]'] = 1 * ship.fishing_capacity
                costs[f'harbor fee for {ship.nickname} @ {ship.harbor.name} [{ship.id}]'] = ship.harbor.storage_fee
        if not none_assigned:
            invoice = Invoice.objects.create(user=user, revenues=items, costs=costs, date=current_time)
            user.profile.balance += invoice.getProfit()
            user.save()

    update_market_value(species_fished)

def update_market_value(dict):
    base_change = 0.98
    total_fish = 0
    fluctuation_constant = 0.1
    if dict != None:
        for fish in dict:
            total_fish += dict[fish]
    
    for species in FishSpecies.objects.all():
        prop = dict[f'{species.name}'] / total_fish
        species.value /= ((base_change + prop*fluctuation_constant) * random.uniform(0.9,1.112))
        species.save()

@shared_task
def process_ended_auctions():
    AuctionListing.check_ended_auctions()

@shared_task
def update_ship_stock_and_price():
    restock_constant = 1.5
    for ship in ManufacturerShip.objects.all():
        if ship.stock < ship.max_stock:
            ship.stock += int(restock_constant * (ship.max_stock/(ship.stock + 1)))
            if ship.stock > ship.max_stock:
                ship.stock = ship.max_stock
            ship.save()


""" def calculate_demand(ship):
    purchases = {}
    for purchase in Transaction.objects.filter(type='S2P'):
        ship = Ship.objects.get(id = purchase.object_id)
        purchases[f'ship.name'] += 1 """
    

