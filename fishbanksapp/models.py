from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.serializers.json import DjangoJSONEncoder
from simple_history.models import HistoricalRecords
import time
from datetime import datetime



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    balance = models.FloatField(default=1000.0)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    ships_list = models.JSONField(default=dict, encoder=DjangoJSONEncoder)
    history = HistoricalRecords()
 
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    # Automatically create a profile when a user is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

class Harbor(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(blank=True, null=True, max_length=400)
    carrying_capacity = models.IntegerField(default=100000)
    storage_fee = models.FloatField(default=5000)
    def __str__(self):
        return self.name


class Ship(models.Model):
    history = HistoricalRecords()
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, default='')
    fishing_capacity = models.IntegerField(default=0)
    cost = models.FloatField()
    fishing_rate = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    damage = models.FloatField(default=0)
    harbor = models.ForeignKey(Harbor, on_delete=models.SET_NULL, null=True, blank=True, related_name='ships_temp')  # New ForeignKey

    def __str__(self):
        return self.name
    
class ManufacturerShip(models.Model):
    name = models.CharField(max_length=100)
    fishing_capacity = models.IntegerField(default=0)
    fishing_rate = models.IntegerField()
    base_cost = models.FloatField()
    description = models.TextField(blank=True, null=True)

    def sellShip(self, customer):
        Ship.objects.create(name=self.name, fishing_capacity=self.fishing_capacity, fishing_rate=self.fishing_rate, description=self.description, owner=customer, nickname=self.name, cost=self.base_cost)

    
class FishSpecies(models.Model):
    population = models.IntegerField(default=10000)
    value = models.FloatField(default=1.0)
    name = models.TextField(default=None)
    weight = models.FloatField(default=1.0)
    history = HistoricalRecords()
    harbor = models.ForeignKey(Harbor, on_delete=models.SET_NULL, null=True, blank=True, related_name='fish')  # New ForeignKey
    #growth parameters
    C = models.FloatField(default=100000)
    k = models.FloatField(default=0.01)

    def __str__(self):
        return f"Fish Stock: {self.population}, Value: ${self.value}"


class InGameTime(models.Model):
    start_time = models.FloatField(default=0)
    game_start_time = models.FloatField(default=0)
    time_scale = models.FloatField(default=365.0)
    
        
    def resetTime(self):
        self.start_time = time.time()
        self.save()

    def getTime(self):
        current_time = time.time()
        return self.game_start_time + (current_time - self.start_time)*self.time_scale
    
    def formatTime(self, value):
        return datetime.fromtimestamp(int(value)).strftime('%Y-%m-%d %I:%M%p')

class Invoice(models.Model):
    revenues = models.JSONField(default=dict, encoder=DjangoJSONEncoder)
    costs = models.JSONField(default=dict, encoder=DjangoJSONEncoder)
    date = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    def getProfit(self):
        total_r = 0
        total_c = 0
        for i in self.costs.values():
            total_c += i
        for i in self.revenues.values():
            total_r += i
        return total_r-total_c


class Gas(models.Model):
    price = models.FloatField(default=0.01)

    def __str__(self):
        return f"Gas price is {self.price} per fishing cycle per kg of fishing capacity on ship"
