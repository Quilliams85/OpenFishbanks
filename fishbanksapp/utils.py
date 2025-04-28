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
        {"name": "Bluefin Tuna", "value": 15.0, "weight": 60.0, "harbor": ironhook, "C": 800000, "k": 0.00167},
        {"name": "Yellowfin Tuna", "value": 10.5, "weight": 45.0, "harbor": caldera_bay, "C": 1000000, "k": 0.00233},
        {"name": "Halibut", "value": 12.0, "weight": 25.0, "harbor": stormrest, "C": 950000, "k": 0.00267},

        {"name": "Bigeye Tuna", "value": 10.5, "weight": 35.0, "harbor": port_greenwood, "C": 900000, "k": 0.00300},
        {"name": "Atlantic Cod", "value": 9.75, "weight": 3.0, "harbor": eastwind, "C": 600000, "k": 0.00400},
        {"name": "Atlantic Mackerel", "value": 10.5, "weight": 1.8, "harbor": seabright, "C": 700000, "k": 0.00500},
        {"name": "Swordfish", "value": 12.0, "weight": 30.0, "harbor": caldera_bay, "C": 850000, "k": 0.00267},
        {"name": "Snapper", "value": 10.5, "weight": 3.2, "harbor": eastwind, "C": 550000, "k": 0.00400},

        {"name": "Grouper", "value": 12.0, "weight": 4.5, "harbor": moonstone, "C": 400000, "k": 0.00467},
        {"name": "Dogfish", "value": 9.0, "weight": 2.3, "harbor": hollow, "C": 350000, "k": 0.00600},
        {"name": "Eel", "value": 9.0, "weight": 1.5, "harbor": seabright, "C": 420000, "k": 0.00567},
        {"name": "Pangasius", "value": 7.5, "weight": 1.2, "harbor": driftwood, "C": 300000, "k": 0.00600},
        {"name": "Tilapia", "value": 7.5, "weight": 1.0, "harbor": driftwood, "C": 320000, "k": 0.00600},
        {"name": "Mahi Mahi", "value": 10.5, "weight": 6.0, "harbor": stormrest, "C": 600000, "k": 0.00400},

        {"name": "Sardine", "value": 6.0, "weight": 0.15, "harbor": sandbar, "C": 200000, "k": 0.00667},
        {"name": "Atlantic Herring", "value": 6.0, "weight": 0.2, "harbor": sandbar, "C": 250000, "k": 0.00600},
        {"name": "Haddock", "value": 9.75, "weight": 2.5, "harbor": hollow, "C": 300000, "k": 0.00533},

        {"name": "Peruvian Anchoveta", "value": 7.5, "weight": 0.025, "harbor": sandbar, "C": 500000, "k": 0.00667},
        {"name": "Alaska Pollock", "value": 9.0, "weight": 0.7, "harbor": port_greenwood, "C": 400000, "k": 0.00500},
        {"name": "Skipjack Tuna", "value": 9.0, "weight": 2.0, "harbor": moonstone, "C": 600000, "k": 0.00467},
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
        fishing_capacity=2000,
        fishing_rate=1000,
        base_cost=50000,
        description="A versatile and cost-effective trawler, ideal for coastal waters.",
        max_stock=50
    )

    ManufacturerShip.objects.create(
        name="Small Seiner",
        fishing_capacity=3200,
        fishing_rate=1600,
        base_cost=90000,
        description="A compact seiner for efficient small-to-medium scale fishing.",
        max_stock=45
    )

    ManufacturerShip.objects.create(
        name="Seiner",
        fishing_capacity=6000,
        fishing_rate=3000,
        base_cost=200000,
        description="A reliable vessel with advanced netting for larger catches.",
        max_stock=40
    )

    ManufacturerShip.objects.create(
        name="Large Seiner",
        fishing_capacity=9200,
        fishing_rate=4600,
        base_cost=325000,
        description="Enhanced storage and hauling systems for bigger fishing hauls.",
        max_stock=36
    )

    ManufacturerShip.objects.create(
        name="Stern Trawler",
        fishing_capacity=18000,
        fishing_rate=9000,
        base_cost=500000,
        description="A robust deep-sea trawler for high-volume commercial ventures.",
        max_stock=32
    )

    ManufacturerShip.objects.create(
        name="Ocean Stern Trawler",
        fishing_capacity=24000,
        fishing_rate=12000,
        base_cost=750000,
        description="Extended range and reinforced hull for heavier catches.",
        max_stock=28
    )

    ManufacturerShip.objects.create(
        name="Longliner",
        fishing_capacity=30000,
        fishing_rate=15000,
        base_cost=1000000,
        description="A high-capacity longliner suited for open ocean expeditions.",
        max_stock=25
    )

    ManufacturerShip.objects.create(
        name="Industrial Longliner",
        fishing_capacity=50000,
        fishing_rate=25000,
        base_cost=2000000,
        description="Industrial-scale longliner designed for massive sustained catches.",
        max_stock=20
    )

    ManufacturerShip.objects.create(
        name="Factory Longliner",
        fishing_capacity=100000,
        fishing_rate=50000,
        base_cost=10000000,
        description="Combines massive capacity with onboard processing plants.",
        max_stock=10
    )

    ManufacturerShip.objects.create(
        name="Mini Factory Ship",
        fishing_capacity=160000,
        fishing_rate=80000,
        base_cost=20000000,
        description="A smaller factory ship with significant automation and storage.",
        max_stock=8
    )

    ManufacturerShip.objects.create(
        name="Automated Factory Ship",
        fishing_capacity=240000,
        fishing_rate=120000,
        base_cost=35000000,
        description="Fully automated giant trawler with AI-driven harvesting systems.",
        max_stock=6
    )

    ManufacturerShip.objects.create(
        name="Hyper Trawler",
        fishing_capacity=360000,
        fishing_rate=180000,
        base_cost=60000000,
        description="High-efficiency vessel maximizing catch volume and speed.",
        max_stock=5
    )

    ManufacturerShip.objects.create(
        name="Oceanic Megatrawler",
        fishing_capacity=500000,
        fishing_rate=250000,
        base_cost=100000000,
        description="Pinnacle of fishing technology; massive storage and processing.",
        max_stock=4
    )

    ManufacturerShip.objects.create(
        name="Leviathan Dredger",
        fishing_capacity=1200000,
        fishing_rate=600000,
        base_cost=250000000,
        description="The ultimate ultra-massive dredger reshaping marine economies.",
        max_stock=2
    )




    time = InGameTime.objects.create(game_start_time=1893477600)
    time.resetTime()

    if User.objects.all() != None:
        for user in User.objects.all():
            Ship.objects.create(name='Starter Ship', fishing_capacity=1000, fishing_rate=500, description='starting vessel', owner=user, nickname='Starter Ship', cost=50000)




def reset_db():
    for user in User.objects.all():
        user.profile.balance = 20000.0
        user.save()
    FishSpecies.objects.all().delete()
    ManufacturerShip.objects.all().delete()
    Ship.objects.all().delete()
    Gas.objects.all().delete()
    Harbor.objects.all().delete()
    Invoice.objects.all().delete()
    AuctionListing.objects.all().delete()
    Transaction.objects.all().delete()
    Group.objects.all().delete()