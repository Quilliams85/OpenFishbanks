from django.core.mail import send_mail
from .models import Harbor, FishSpecies, ManufacturerShip, Gas, InGameTime, Ship, Invoice, AuctionListing, Transaction, Group
import random
from django.contrib.auth.models import User

def send_invitation_email(invitation):
    subject = f"Invitation to join {invitation.group.name}"
    message = f"Hi {invitation.recipient.username},\n\nYou have been invited to join {invitation.group.name} by {invitation.sender.username}.\n\nPlease visit the site to accept or decline the invitation."
    send_mail(subject, message, 'noreply@example.com', [invitation.recipient.email])

def setup_sim():
    #create harbors
    harbor_data = [
        {"name": "Port Greenwood", "description": "A bustling harbor nestled between forested cliffs.", "carrying_capacity": 120000, "storage_fee": 4500},
        {"name": "Eastwind Dockyard", "description": "Known for strong easterly winds and merchant traffic.", "carrying_capacity": 95000, "storage_fee": 5200},
        {"name": "Caldera Bay", "description": "Volcanic bay with deep waters for large vessels.", "carrying_capacity": 140000, "storage_fee": 6000},
        {"name": "Sandbar Point", "description": "Quiet inlet with artisanal fishing.", "carrying_capacity": 75000, "storage_fee": 3000},
        {"name": "Ironhook Wharf", "description": "Industrial fishing hub with massive storage.", "carrying_capacity": 160000, "storage_fee": 7000},
        {"name": "Moonstone Harbor", "description": "Picturesque and tourist-friendly.", "carrying_capacity": 85000, "storage_fee": 4800},
        {"name": "Seabright Port", "description": "Sun-drenched harbor for mid-sized fleets.", "carrying_capacity": 110000, "storage_fee": 5100},
        {"name": "Hollow Shore Harbor", "description": "Protected bay for small boats.", "carrying_capacity": 90000, "storage_fee": 4700},
        {"name": "Stormrest Landing", "description": "Harsh-weather port with strong infrastructure.", "carrying_capacity": 130000, "storage_fee": 5500},
        {"name": "Driftwood Quay", "description": "Scenic harbor with calm tides.", "carrying_capacity": 100000, "storage_fee": 4300},
    ]

    harbors = [Harbor.objects.create(**data) for data in harbor_data]

    #create fishspecies instances
    port_greenwood, eastwind, caldera_bay, sandbar, ironhook, moonstone, seabright, hollow, stormrest, driftwood = harbors


    fish_species_data = [
        {"name": "Bluefin Tuna", "value": 20.0, "weight": 60.0, "harbor": ironhook, "C": int(80000 * random.uniform(9, 13)), "k": 0.005},
        {"name": "Yellowfin Tuna", "value": 2.3, "weight": 45.0, "harbor": caldera_bay, "C": int(100000 * random.uniform(9, 13)), "k": 0.007},
        {"name": "Halibut", "value": 13.5, "weight": 25.0, "harbor": stormrest, "C": int(95000 * random.uniform(9, 13)), "k": 0.008},

        {"name": "Bigeye Tuna", "value": 6.5, "weight": 35.0, "harbor": port_greenwood, "C": int(90000 * random.uniform(9, 13)), "k": 0.009},
        {"name": "Atlantic Cod", "value": 9.0, "weight": 3.0, "harbor": eastwind, "C": int(60000 * random.uniform(9, 13)), "k": 0.012},
        {"name": "Atlantic Mackerel", "value": 11.87, "weight": 1.8, "harbor": seabright, "C": int(70000 * random.uniform(9, 13)), "k": 0.015},
        {"name": "Swordfish", "value": 10.0, "weight": 30.0, "harbor": caldera_bay, "C": int(85000 * random.uniform(9, 13)), "k": 0.008},
        {"name": "Snapper", "value": 8.4, "weight": 3.2, "harbor": eastwind, "C": int(55000 * random.uniform(9, 13)), "k": 0.012},

        {"name": "Grouper", "value": 12.0, "weight": 4.5, "harbor": moonstone, "C": int(40000 * random.uniform(9, 13)), "k": 0.014},
        {"name": "Dogfish", "value": 3.8, "weight": 2.3, "harbor": hollow, "C": int(35000 * random.uniform(9, 13)), "k": 0.018},
        {"name": "Eel", "value": 6.0, "weight": 1.5, "harbor": seabright, "C": int(42000 * random.uniform(9, 13)), "k": 0.017},
        {"name": "Pangasius", "value": 1.8, "weight": 1.2, "harbor": driftwood, "C": int(30000 * random.uniform(9, 13)), "k": 0.018},
        {"name": "Tilapia", "value": 2.0, "weight": 1.0, "harbor": driftwood, "C": int(32000 * random.uniform(9, 13)), "k": 0.018},
        {"name": "Mahi Mahi", "value": 9.7, "weight": 6.0, "harbor": stormrest, "C": int(60000 * random.uniform(9, 13)), "k": 0.012},

        {"name": "Sardine", "value": 1.5, "weight": 0.15, "harbor": sandbar, "C": int(20000 * random.uniform(9, 13)), "k": 0.02},
        {"name": "Atlantic Herring", "value": 3.0, "weight": 0.2, "harbor": sandbar, "C": int(25000 * random.uniform(9, 13)), "k": 0.018},
        {"name": "Haddock", "value": 7.2, "weight": 2.5, "harbor": hollow, "C": int(30000 * random.uniform(9, 13)), "k": 0.016},

        {"name": "Peruvian Anchoveta", "value": 15.0, "weight": 0.025, "harbor": sandbar, "C": int(50000 * random.uniform(9, 13)), "k": 0.02},
        {"name": "Alaska Pollock", "value": 5.81, "weight": 0.7, "harbor": port_greenwood, "C": int(40000 * random.uniform(9, 13)), "k": 0.015},
        {"name": "Skipjack Tuna", "value": 4.1, "weight": 2.0, "harbor": moonstone, "C": int(60000 * random.uniform(9, 13)), "k": 0.014},
    ]


    for data in fish_species_data:
        FishSpecies.objects.create(
            name=data["name"],
            value=data["value"],
            weight=data["weight"],
            population=data["C"],
            C=data["C"],
            k=data["k"],
            harbor=data["harbor"]
        )
    
    Gas.objects.create(price=1.0)

    ManufacturerShip.objects.create(
        name="Outrigger Trawler",
        fishing_capacity=5000,
        fishing_rate=500,
        base_cost=50000,
        description="A versatile and cost-effective trawler, perfect for small-scale fishing operations. Ideal for coastal waters with a capacity of 5,000 kg and a steady catch rate."
    )

    ManufacturerShip.objects.create(
        name="Seiner",
        fishing_capacity=15000,
        fishing_rate=1500,
        base_cost=200000,
        description="A reliable vessel designed for medium-scale fishing. Equipped with advanced netting systems, it can handle larger catches of up to 15,000 kg with improved efficiency."
    )

    ManufacturerShip.objects.create(
        name="Stern Trawler",
        fishing_capacity=30000,
        fishing_rate=4500,
        base_cost=500000,
        description="A robust trawler built for deep-sea fishing. With a massive 30,000 kg capacity and high-speed hauling, it's perfect for commercial fishing ventures."
    )

    ManufacturerShip.objects.create(
        name="Longliner",
        fishing_capacity=50000,
        fishing_rate=5000,
        base_cost=1000000,
        description="A high-capacity vessel designed for longline fishing. Capable of handling 50,000 kg of catch, it's suited for large-scale operations in open waters."
    )

    ManufacturerShip.objects.create(
        name="Factory Longliner",
        fishing_capacity=250000,
        fishing_rate=25000,
        base_cost=10000000,
        description="The ultimate fishing vessel, combining massive capacity (250,000 kg) with industrial-grade processing capabilities. Designed for the largest and most demanding fishing operations."
    )
    ManufacturerShip.objects.create(
        name="Automated Factory Ship",
        fishing_capacity=750000,
        fishing_rate=60000,
        base_cost=35000000,
        description="A behemoth of the sea, this fully automated factory ship integrates AI-driven trawling systems and onboard processing. With a staggering 750,000 kg capacity, it's designed for relentless, efficient harvesting on a global scale."
    )

    ManufacturerShip.objects.create(
        name="Oceanic Megatrawler",
        fishing_capacity=1500000,
        fishing_rate=125000,
        base_cost=100000000,
        description="The Oceanic Megatrawler is the pinnacle of fishing technology—capable of processing multiple species simultaneously and storing up to 1.5 million kg. Operates continuously for weeks with onboard freezing and logistics facilities."
    )

    ManufacturerShip.objects.create(
        name="Leviathan Dredger",
        fishing_capacity=3000000,
        fishing_rate=300000,
        base_cost=250000000,
        description="An ultra-massive, world-spanning dredger capable of reshaping marine economies. With a 3 million kg capacity and unmatched rate, the Leviathan Dredger is reserved for industrial-scale operations and legendary captains."
    )


    time = InGameTime.objects.create(game_start_time=1893477600)
    time.resetTime()


def reset_db():
    User.objects.all().delete()
    FishSpecies.objects.all().delete()
    ManufacturerShip.objects.all().delete()
    Ship.objects.all().delete()
    Gas.objects.all().delete()
    Harbor.objects.all().delete()
    Invoice.objects.all().delete()
    AuctionListing.objects.all().delete()
    Transaction.objects.all().delete()
    Group.objects.all().delete()
