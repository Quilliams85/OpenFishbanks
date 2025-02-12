from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    balance = models.FloatField(default=1000.0)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

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

# Create your models here.
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
    fish_capacity = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

""" class FishStock(models.Model):
    total_fish = models.IntegerField(default=10000)  # Total fish in the ecosystem
    fish_value = models.FloatField(default=1.0)      # Value of each fish

    def __str__(self):
        return f"Fish Stock: {self.total_fish}, Value: ${self.fish_value}" """
    
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fish_sold = models.IntegerField()
    revenue = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} sold {self.fish_sold} fish for ${self.revenue}"