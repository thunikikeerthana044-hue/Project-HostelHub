# seed_data.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostelhub.settings')
django.setup()

from django.contrib.auth.models import User
from hostels.models import UserProfile, Amenity, Hostel, Room, Review, HostelImage

def seed():
    print("Starting database seed with expanded Hyderabad and surroundings dataset...")

    # 1. Create or get Owner user
    owner_user, created = User.objects.get_or_create(username='owner', defaults={
        'email': 'owner@hostelhub.com',
        'first_name': 'Arun',
        'last_name': 'Sharma',
        'is_staff': False,
        'is_superuser': False
    })
    if created:
        owner_user.set_password('password123')
        owner_user.save()
        print("Created owner user.")
    
    # Ensure profile role is 'owner'
    profile, p_created = UserProfile.objects.get_or_create(user=owner_user)
    profile.role = 'owner'
    profile.phone = '9876543210'
    profile.city = 'Bangalore'
    profile.save()

    # Create or get Seeker user for testing reviews
    seeker_user, created = User.objects.get_or_create(username='seeker', defaults={
        'email': 'seeker@hostelhub.com',
        'first_name': 'Rohan',
        'last_name': 'Das',
    })
    if created:
        seeker_user.set_password('password123')
        seeker_user.save()
        print("Created seeker user.")
    
    seeker_profile, p_created = UserProfile.objects.get_or_create(user=seeker_user)
    seeker_profile.role = 'student'
    seeker_profile.phone = '9123456789'
    seeker_profile.city = 'Hyderabad'
    seeker_profile.save()

    # 2. Seed Amenities
    amenity_data = [
        ("High-Speed WiFi", "bi bi-wifi"),
        ("Air Conditioning", "bi bi-wind"),
        ("Laundry Services", "bi bi-droplet-half"),
        ("24/7 CCTV & Security", "bi bi-shield-lock"),
        ("Fitness Gym", "bi bi-activity"),
        ("Power Backup", "bi bi-lightning-charge"),
        ("Hygienic Meals", "bi bi-egg-fried"),
        ("Daily Housekeeping", "bi bi-stars"),
    ]
    
    amenities = []
    for name, icon in amenity_data:
        amenity, created = Amenity.objects.get_or_create(name=name, defaults={'icon': icon})
        amenities.append(amenity)
        if created:
            print(f"Created amenity: {name}")

    # 3. Seed Hostels (Hyderabad, Surrounding suburbs, Bangalore, Mumbai)
    hostels_data = [
        # Hyderabad & Surroundings
        {
            "name": "Elite Women's PG & Hostel",
            "description": "Premium security, single and sharing AC rooms with high-speed internet, delicious home-cooked meals, security CCTV, and regular housekeeping. Conveniently located near Gachibowli IT hub.",
            "address": "Lane 4, Gachibowli Near DLF Cyber City",
            "city": "Hyderabad",
            "state": "Telangana",
            "pincode": "500032",
            "phone": "9554433221",
            "email": "elitehyderabad@hostelhub.com",
            "gender_type": "female",
            "latitude": 17.4483,
            "longitude": 78.3741,
            "is_verified": True,
            "amenities_indices": [0, 1, 3, 5, 6, 7]
        },
        {
            "name": "Cyber Co-living Hub",
            "description": "State-of-the-art mixed co-living space. Features study lounges, indoor sports recreation, shared laundry, high-speed fiber internet, and premium AC room setups. Best suited for working professionals and students.",
            "address": "Hitech City Main Rd, Madhapur",
            "city": "Hyderabad",
            "state": "Telangana",
            "pincode": "500081",
            "phone": "9443322110",
            "email": "cyberhub@hostelhub.com",
            "gender_type": "mixed",
            "latitude": 17.4435,
            "longitude": 78.3822,
            "is_verified": True,
            "amenities_indices": [0, 1, 2, 3, 5, 7]
        },
        {
            "name": "Kukatpally Boys Executive PG",
            "description": "Highly affordable executive PG for male students and job seekers. Offers three home-cooked Telugu style meals, daily room cleaning, locker facilities, and heavy-duty backup power systems. Situated close to JNTU metro station.",
            "address": "Ph-3, Near JNTU Metro Station, Kukatpally",
            "city": "Hyderabad",
            "state": "Telangana",
            "pincode": "500072",
            "phone": "9000112233",
            "email": "kukatpallypg@hostelhub.com",
            "gender_type": "male",
            "latitude": 17.4948,
            "longitude": 78.3996,
            "is_verified": True,
            "amenities_indices": [0, 2, 3, 5, 6, 7]
        },
        {
            "name": "Secunderabad Transit PG",
            "description": "Convenient transit co-living accommodation located right behind Secunderabad railway station. Perfect for travelers, weekend visitors, and temporary workers looking for budget-friendly dorms or private double rooms.",
            "address": "Regimental Bazaar, Secunderabad",
            "city": "Secunderabad",
            "state": "Telangana",
            "pincode": "500003",
            "phone": "9111223344",
            "email": "secunderabadpg@hostelhub.com",
            "gender_type": "mixed",
            "latitude": 17.4344,
            "longitude": 78.5011,
            "is_verified": True,
            "amenities_indices": [0, 3, 5, 7]
        },
        {
            "name": "Begumpet Girls Luxury Residency",
            "description": "Exclusive, luxury boutique residency for women. Biometric access, premium mattress beds, reading lamps, indoor gym space, organic custom meals, and top-tier safety patrols. Walkable distance to major metro links.",
            "address": "Prakash Nagar, Begumpet",
            "city": "Hyderabad",
            "state": "Telangana",
            "pincode": "500016",
            "phone": "9222334455",
            "email": "begumpetresidency@hostelhub.com",
            "gender_type": "female",
            "latitude": 17.4421,
            "longitude": 78.4712,
            "is_verified": True,
            "amenities_indices": [0, 1, 2, 3, 4, 5, 6, 7]
        },
        {
            "name": "Kondapur IT Professional Stay",
            "description": "Modern boys PG curated specifically for software engineers and tech sector workers. Features premium study desks, ergonomic chairs, super-fast 300 Mbps WiFi, power backups, and late curfew accommodations.",
            "address": "Hanuman Nagar, Kondapur",
            "city": "Hyderabad",
            "state": "Telangana",
            "pincode": "500084",
            "phone": "9333445566",
            "email": "kondapurstay@hostelhub.com",
            "gender_type": "male",
            "latitude": 17.4612,
            "longitude": 78.3688,
            "is_verified": True,
            "amenities_indices": [0, 1, 2, 3, 5, 6, 7]
        },
        {
            "name": "Ramanthapur Student Co-living",
            "description": "Dynamic co-living environment tailored for students of Aurora Group and surrounding colleges. Features high speed internet, clean dining options, daily cleaning, and recreation rooms.",
            "address": "Opposite Aurora College, Ramanthapur, Hyderabad",
            "city": "Hyderabad",
            "state": "Telangana",
            "pincode": "500013",
            "phone": "9444556677",
            "email": "ramanthapurcoliving@hostelhub.com",
            "gender_type": "mixed",
            "latitude": 17.3986,
            "longitude": 78.5321,
            "is_verified": True,
            "amenities_indices": [0, 2, 3, 5, 6, 7]
        },
        {
            "name": "Sri Sai Girls PG Ramanthapur",
            "description": "Safe and peaceful ladies PG in Ramanthapur. Features secure main entrance with biometric check, organic home-style meals, dynamic housekeeping, and power backup.",
            "address": "Narayana High School Lane, Ramanthapur, Hyderabad",
            "city": "Hyderabad",
            "state": "Telangana",
            "pincode": "500013",
            "phone": "9555667788",
            "email": "srisaigirlspg@hostelhub.com",
            "gender_type": "female",
            "latitude": 17.3995,
            "longitude": 78.5315,
            "is_verified": True,
            "amenities_indices": [0, 3, 5, 6, 7]
        },
        {
            "name": "Pragathi Boys PG Ramanthapur",
            "description": "Comfortable stay for boys near Ramanthapur lake. Home-like meals, daily cleaning, individual cupboards, high speed internet, and friendly caretakers.",
            "address": "Laxmi Nagar, Near Lake Road, Ramanthapur, Hyderabad",
            "city": "Hyderabad",
            "state": "Telangana",
            "pincode": "500013",
            "phone": "9666778899",
            "email": "pragathiboyspg@hostelhub.com",
            "gender_type": "male",
            "latitude": 17.3972,
            "longitude": 78.5342,
            "is_verified": True,
            "amenities_indices": [0, 2, 3, 5, 6, 7]
        },
        
        # Bangalore & Mumbai backups
        {
            "name": "Starlight Luxury Boys Hostel",
            "description": "Premium accommodation for boys, located near major IT parks and colleges. Includes air-conditioned rooms, individual study tables, high-speed internet, and three delicious meals daily.",
            "address": "45, 80 Feet Rd, Koramangala 4th Block",
            "city": "Bangalore",
            "state": "Karnataka",
            "pincode": "560034",
            "phone": "9887766554",
            "email": "starlight@hostelhub.com",
            "gender_type": "male",
            "latitude": 12.9344,
            "longitude": 77.6244,
            "is_verified": True,
            "amenities_indices": [0, 1, 2, 3, 5, 6, 7]
        },
        {
            "name": "Sunrise Premium Girls PG",
            "description": "Safe, secure, and modern PG exclusively for girls. Offers bi-monthly cleaning, organic home-style meals, dynamic community events, and a secure biometric entry system.",
            "address": "12/A, Lane 3, Sector 5, HSR Layout",
            "city": "Bangalore",
            "state": "Karnataka",
            "pincode": "560102",
            "phone": "9776655443",
            "email": "sunrisepg@hostelhub.com",
            "gender_type": "female",
            "latitude": 12.9128,
            "longitude": 77.6388,
            "is_verified": True,
            "amenities_indices": [0, 2, 3, 5, 6, 7]
        },
        {
            "name": "Metro Hub Co-ed Co-living",
            "description": "Vibrant co-living spaces for boys and girls. Experience community living at its best with shared gaming rooms, gym access, community kitchen, and weekend social events.",
            "address": "88, Andheri Kurla Road, near Andheri Metro",
            "city": "Mumbai",
            "state": "Maharashtra",
            "pincode": "400059",
            "phone": "9665544332",
            "email": "metrohub@hostelhub.com",
            "gender_type": "mixed",
            "latitude": 19.1136,
            "longitude": 72.8697,
            "is_verified": True,
            "amenities_indices": [0, 1, 2, 3, 4, 5, 7]
        }
    ]

    for h_data in hostels_data:
        hostel, created = Hostel.objects.get_or_create(
            name=h_data["name"],
            defaults={
                "owner": owner_user,
                "description": h_data["description"],
                "address": h_data["address"],
                "city": h_data["city"],
                "state": h_data["state"],
                "pincode": h_data["pincode"],
                "phone": h_data["phone"],
                "email": h_data["email"],
                "gender_type": h_data["gender_type"],
                "latitude": h_data["latitude"],
                "longitude": h_data["longitude"],
                "is_verified": h_data["is_verified"],
                "is_active": True
            }
        )
        if created:
            print(f"Created hostel: {hostel.name} in {hostel.city}")
            # Add selected amenities
            for idx in h_data["amenities_indices"]:
                hostel.amenities.add(amenities[idx])
            
            # Seed Rooms for this hostel
            seed_rooms(hostel)
            
            # Seed reviews for this hostel
            seed_reviews(hostel, seeker_user)
        else:
            # If already exists, make sure rooms are seeded
            if hostel.rooms.count() == 0:
                seed_rooms(hostel)

def seed_rooms(hostel):
    # Determine base pricing to vary properties
    price_factor = 1.0
    if "Transit" in hostel.name:
        price_factor = 0.6
    elif "Luxury" in hostel.name:
        price_factor = 1.3
    
    if hostel.gender_type == 'male' or hostel.gender_type == 'mixed':
        # Single room
        Room.objects.create(
            hostel=hostel,
            room_type='single',
            capacity=1,
            price_per_month=float(12000.00 * price_factor),
            deposit_amount=float(20000.00 * price_factor),
            total_rooms=4,
            available_rooms=4,
            is_available=True,
            description="Private single AC room with study table, wardrobe, and attached washroom."
        )
        # Double room
        Room.objects.create(
            hostel=hostel,
            room_type='double',
            capacity=2,
            price_per_month=float(7500.00 * price_factor),
            deposit_amount=float(12000.00 * price_factor),
            total_rooms=10,
            available_rooms=7,
            is_available=True,
            description="Premium double sharing room with individual workspaces and high-speed WiFi."
        )
        # Dormitory
        Room.objects.create(
            hostel=hostel,
            room_type='dormitory',
            capacity=4,
            price_per_month=float(5000.00 * price_factor),
            deposit_amount=float(8000.00 * price_factor),
            total_rooms=4,
            available_rooms=3,
            is_available=True,
            description="Comfortable dormitory bed setup with personal safety lockers."
        )
    else:
        # Female-only rooms
        Room.objects.create(
            hostel=hostel,
            room_type='single',
            capacity=1,
            price_per_month=float(13000.00 * price_factor),
            deposit_amount=float(25000.00 * price_factor),
            total_rooms=5,
            available_rooms=4,
            is_available=True,
            description="Private executive suite room with dressers, full mirror, and balcony."
        )
        Room.objects.create(
            hostel=hostel,
            room_type='double',
            capacity=2,
            price_per_month=float(8000.00 * price_factor),
            deposit_amount=float(15000.00 * price_factor),
            total_rooms=12,
            available_rooms=10,
            is_available=True,
            description="Spacious sharing room with writing desks, personal locks, and custom storage."
        )
        Room.objects.create(
            hostel=hostel,
            room_type='triple',
            capacity=3,
            price_per_month=float(6000.00 * price_factor),
            deposit_amount=float(10000.00 * price_factor),
            total_rooms=6,
            available_rooms=5,
            is_available=True,
            description="Cozy three sharing room setup, with access to common dining and geyser."
        )
    print(f"Rooms seeded for {hostel.name}")

def seed_reviews(hostel, user):
    Review.objects.create(
        hostel=hostel,
        reviewer=user,
        rating=5,
        comment="Absolutely wonderful stay! The food is hygienic, internet is super fast, and the staff is extremely helpful. Strongly recommended!"
    )
    admin_user = User.objects.filter(is_superuser=True).first()
    if admin_user:
        Review.objects.create(
            hostel=hostel,
            reviewer=admin_user,
            rating=4,
            comment="Very clean facilities and convenient location. Security is top-notch."
        )
    print(f"Reviews seeded for {hostel.name}")

if __name__ == '__main__':
    seed()
    print("Database seeding completed successfully!")
