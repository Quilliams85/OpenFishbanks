from django.core.mail import send_mail
from .models import Harbor, FishSpecies, ManufacturerShip, Gas, InGameTime

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
        # Large harbors (high capacity, high fee)
        {"name": "Bluefin Tuna", "value": 40.0, "weight": 60.0, "harbor": ironhook, "C": 80000, "k": 0.005},
        {"name": "Yellowfin Tuna", "value": 2.3, "weight": 45.0, "harbor": caldera_bay, "C": 100000, "k": 0.007},
        {"name": "Halibut", "value": 13.5, "weight": 25.0, "harbor": stormrest, "C": 95000, "k": 0.008},

        # Medium to large harbors
        {"name": "Bigeye Tuna", "value": 6.5, "weight": 35.0, "harbor": port_greenwood, "C": 90000, "k": 0.009},
        {"name": "Atlantic Cod", "value": 9.0, "weight": 3.0, "harbor": eastwind, "C": 60000, "k": 0.012},
        {"name": "Atlantic Mackerel", "value": 11.87, "weight": 1.8, "harbor": seabright, "C": 70000, "k": 0.015},
        {"name": "Swordfish", "value": 10.0, "weight": 30.0, "harbor": caldera_bay, "C": 85000, "k": 0.008},
        {"name": "Snapper", "value": 8.4, "weight": 3.2, "harbor": eastwind, "C": 55000, "k": 0.012},

        # Mid-tier harbors
        {"name": "Grouper", "value": 12.0, "weight": 4.5, "harbor": moonstone, "C": 40000, "k": 0.014},
        {"name": "Dogfish", "value": 3.8, "weight": 2.3, "harbor": hollow, "C": 35000, "k": 0.018},
        {"name": "Eel", "value": 6.0, "weight": 1.5, "harbor": seabright, "C": 42000, "k": 0.017},
        {"name": "Pangasius", "value": 1.8, "weight": 1.2, "harbor": driftwood, "C": 30000, "k": 0.018},
        {"name": "Tilapia", "value": 2.0, "weight": 1.0, "harbor": driftwood, "C": 32000, "k": 0.018},
        {"name": "Mahi Mahi", "value": 9.7, "weight": 6.0, "harbor": stormrest, "C": 60000, "k": 0.012},

        # Small harbors
        {"name": "Sardine", "value": 1.5, "weight": 0.15, "harbor": sandbar, "C": 20000, "k": 0.02},
        {"name": "Atlantic Herring", "value": 3.0, "weight": 0.2, "harbor": sandbar, "C": 25000, "k": 0.018},
        {"name": "Haddock", "value": 7.2, "weight": 2.5, "harbor": hollow, "C": 30000, "k": 0.016},

        # Anchoveta-like species for low-fee ports
        {"name": "Peruvian Anchoveta", "value": 15.0, "weight": 0.025, "harbor": sandbar, "C": 50000, "k": 0.02},
        {"name": "Alaska Pollock", "value": 5.81, "weight": 0.7, "harbor": port_greenwood, "C": 40000, "k": 0.015},
        {"name": "Skipjack Tuna", "value": 4.1, "weight": 2.0, "harbor": moonstone, "C": 60000, "k": 0.014},
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
        fishing_rate=1000,
        base_cost=50000,
        description="A versatile and cost-effective trawler, perfect for small-scale fishing operations. Ideal for coastal waters with a capacity of 5,000 kg and a steady catch rate."
    )

    ManufacturerShip.objects.create(
        name="Seiner",
        fishing_capacity=15000,
        fishing_rate=3000,
        base_cost=200000,
        description="A reliable vessel designed for medium-scale fishing. Equipped with advanced netting systems, it can handle larger catches of up to 15,000 kg with improved efficiency."
    )

    ManufacturerShip.objects.create(
        name="Stern Trawler",
        fishing_capacity=30000,
        fishing_rate=7000,
        base_cost=500000,
        description="A robust trawler built for deep-sea fishing. With a massive 30,000 kg capacity and high-speed hauling, it's perfect for commercial fishing ventures."
    )

    ManufacturerShip.objects.create(
        name="Longliner",
        fishing_capacity=50000,
        fishing_rate=10000,
        base_cost=1000000,
        description="A high-capacity vessel designed for longline fishing. Capable of handling 50,000 kg of catch, it's suited for large-scale operations in open waters."
    )

    ManufacturerShip.objects.create(
        name="Factory Longliner",
        fishing_capacity=250000,
        fishing_rate=50000,
        base_cost=10000000,
        description="The ultimate fishing vessel, combining massive capacity (250,000 kg) with industrial-grade processing capabilities. Designed for the largest and most demanding fishing operations."
    )

    time =InGameTime.objects.create(game_start_time=1893477600)
    time.resetTime()