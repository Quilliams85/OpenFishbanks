from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.serializers.json import DjangoJSONEncoder
from simple_history.models import HistoricalRecords
from django.utils.timezone import now
import time
from datetime import datetime

class Group(models.Model):
    history = HistoricalRecords()
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_organizations', null=True)
    members = models.ManyToManyField(User, related_name='organizations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Invitation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='invitations')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invitation from {self.sender} to {self.recipient} for {self.organization}"

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



class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        PLAYER_TO_PLAYER = "P2P", "Player to Player"
        STORE_TO_PLAYER = "S2P", "Store to Player"
        PLAYER_TO_STORE = "P2S", "Player to Store"
        OTHER = "OTH", "Other"
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='transaction_sender')
    reciever = models.ForeignKey(User, related_name="received_transactions", on_delete=models.CASCADE, null=True, blank=True)
    date = models.CharField(default=None, max_length=100)

    transaction_type = models.CharField(
        max_length=3,
        choices=TransactionType.choices,
        default=TransactionType.PLAYER_TO_PLAYER
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=None, null=True)
    object_id = models.PositiveIntegerField(default=None, null=True)
    object = GenericForeignKey('content_type', 'object_id')
    def __str__(self):
        return f"{self.sender} sent {self.object} to {self.reciever} on {self.date}. This transaction is type {self.transaction_type}"
    
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
    
    def getFormattedTime(self):
        value = self.getTime()
        return self.formatTime(value)

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
        ship = Ship.objects.create(name=self.name, fishing_capacity=self.fishing_capacity, fishing_rate=self.fishing_rate, description=self.description, owner=customer, nickname=self.name, cost=self.base_cost)
        date = InGameTime.objects.first().getFormattedTime()
        Transaction.objects.create(sender=None, reciever=customer,
            transaction_type=Transaction.TransactionType.STORE_TO_PLAYER,
            content_type=ContentType.objects.get_for_model(Ship),
            object_id=ship.id,
            date=date
        )

    
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
    
class AuctionListing(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('expired', 'Expired'),
    ]
    history = HistoricalRecords()
    end_time = models.DateTimeField(null=True, blank=True)
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE, related_name='listing_ship', null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    buy_now_price = models.FloatField(default=0)
    current_bid = models.FloatField(default=0)
    current_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='current_bidder', null=True)
    starting_bid = models.FloatField(default=0)
    details = models.TextField(null=True)
    listing_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_listing', null=True)

    def sellShip(self):
        """Finalize the sale when the auction ends."""
        if self.current_bidder:
            date = InGameTime.objects.first().getFormattedTime()
            self.current_bidder.profile.balance -= self.current_bid
            self.current_bidder.profile.save()
            self.listing_owner.profile.balance += self.current_bid
            self.listing_owner.save()
            
            Transaction.objects.create(
                sender=self.listing_owner,
                reciever=self.current_bidder,
                transaction_type=Transaction.TransactionType.PLAYER_TO_PLAYER,
                content_type=ContentType.objects.get_for_model(Ship),
                object_id=self.ship.id,
                date=date
            )
            
            self.ship.owner = self.current_bidder
            self.ship.save()
            self.status = 'sold'
        else:
            self.status = 'expired'       
        self.save()

    @classmethod
    def check_ended_auctions(cls):
        """Find auctions that have ended and process them."""
        ended_auctions = cls.objects.filter(end_time__lte=now(), status='pending')
        for auction in ended_auctions:
            auction.sellShip()
    
    def enter_bid(self, bid, customer):
        if (self.listing_owner != customer) and (self.end_time < now()):
            self.current_bidder = customer
            self.current_bid = bid

class TradeRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_trades')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_trades')
    
    offered_ships = models.ManyToManyField(Ship, related_name='offered_in_trades', blank=True)
    requested_ships = models.ManyToManyField(Ship, related_name='requested_in_trades', blank=True)
    
    money_offered = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    money_requested = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trade from {self.sender} to {self.recipient} ({self.status})"