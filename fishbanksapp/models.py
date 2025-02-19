from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.serializers.json import DjangoJSONEncoder
from simple_history.models import HistoricalRecords



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

class ToDoList(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Item(models.Model):
    ToDoList = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    complete = models.BooleanField()
        
    def __str__(self):
        return self.text

class Ship(models.Model):
    name = models.CharField(max_length=100)
    cost = models.FloatField()
    stock = models.IntegerField(default=0)
    fishing_rate = models.IntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    
class FishSpecies(models.Model):
    population = models.IntegerField(default=10000)
    value = models.FloatField(default=1.0)
    name = models.TextField(default=None)
    history = HistoricalRecords()

    def __str__(self):
        return f"Fish Stock: {self.population}, Value: ${self.value}"
    
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fish_sold = models.IntegerField()
    revenue = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} sold {self.fish_sold} fish for ${self.revenue}"