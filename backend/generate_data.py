import mysql.connector
import random

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "business_dashboard"
}

businesses = {
    "restaurants": ["Spice Garden", "The Food Hub", "Biryani Palace", "Pizza Corner", "Cafe Mocha", "Royal Dhaba", "Taste of India", "The Grill House", "Saffron Kitchen", "Urban Bites"],
    "hospitals": ["City Hospital", "Apollo Clinic", "Sunrise Medical", "Care Plus Hospital", "LifeLine Clinic", "Metro Health", "Green Cross Hospital", "Healing Touch", "Prime Care", "Wellness Hub"],
    "hotels": ["Hotel Grand", "The Stay Inn", "Comfort Suites", "Royal Palace Hotel", "City Lodge", "Budget Inn", "The Residency", "Park View Hotel", "Elite Stays", "Home Away Hotel"],
    "gyms": ["Fitness First", "Power Gym", "Iron Paradise", "FitZone", "Gold's Gym", "The Workout Hub", "Flex Fitness", "Body Craft", "Muscle Factory", "Strength Studio"],
    "salons": ["Style Studio", "Hair & Care", "The Beauty Bar", "Glam Zone", "Scissors & Combs", "Urban Cuts", "The Makeover Studio", "Shine Salon", "Elegance Beauty", "Trim & Style"]
}

cities = ["Mumbai", "Pune", "Bangalore", "Delhi", "Hyderabad", "Chennai", "Kolkata", "Ahmedabad", "Jaipur", "Surat"]
sources = ["Sulekha", "Justdial", "Google Maps"]

areas = {
    "Mumbai": ["Andheri", "Bandra", "Dadar", "Kurla", "Borivali"],
    "Pune": ["Koregaon Park", "Viman Nagar", "Hinjewadi", "Kothrud", "Wakad"],
    "Bangalore": ["Indiranagar", "Koramangala", "HSR Layout", "Whitefield", "JP Nagar"],
    "Delhi": ["Connaught Place", "Lajpat Nagar", "Karol Bagh", "Dwarka", "Rohini"],
    "Hyderabad": ["Banjara Hills", "Jubilee Hills", "Hitech City", "Gachibowli", "Secunderabad"],
    "Chennai": ["T Nagar", "Anna Nagar", "Adyar", "Velachery", "Nungambakkam"],
    "Kolkata": ["Park Street", "Salt Lake", "New Town", "Howrah", "Behala"],
    "Ahmedabad": ["Navrangpura", "Satellite", "Bopal", "Vastrapur", "CG Road"],
    "Jaipur": ["MI Road", "Vaishali Nagar", "Malviya Nagar", "C Scheme", "Tonk Road"],
    "Surat": ["Adajan", "Vesu", "Athwa", "Citylight", "Piplod"]
}

def generate_phone():
    return f"+91 {random.randint(7000000000, 9999999999)}"

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

listings = []
for city in cities:
    for category, names in businesses.items():
        for area in areas[city]:
            name = random.choice(names) + f" {area}"
            address = f"{random.randint(1,200)}, {area}, {city}"
            phone = generate_phone()
            source = random.choice(sources)
            listings.append((name, category, city, address, phone, source))

query = """
    INSERT INTO listing_master (business_name, category, city, address, phone, source)
    VALUES (%s, %s, %s, %s, %s, %s)
"""
cursor.executemany(query, listings)
conn.commit()
print(f"Successfully inserted {cursor.rowcount} business listings!")
conn.close()