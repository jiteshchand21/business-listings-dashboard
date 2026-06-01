import requests
from bs4 import BeautifulSoup
import mysql.connector
import time
import random

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "business_dashboard"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def insert_listings(listings):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO listing_master (business_name, category, city, address, phone, source)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(query, listings)
    conn.commit()
    print(f"Inserted {cursor.rowcount} records")
    conn.close()

def scrape_sulekha(city, category):
    listings = []
    for page in range(1, 6):
        url = f"https://www.sulekha.com/{category}/{city}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            businesses = soup.find_all('div', class_='compny-detail-info')
            for biz in businesses:
                name = biz.find('h2')
                address = biz.find('p', class_='address')
                phone = biz.find('span', class_='phone')
                listings.append((
                    name.text.strip() if name else 'N/A',
                    category,
                    city,
                    address.text.strip() if address else 'N/A',
                    phone.text.strip() if phone else 'N/A',
                    'Sulekha'
                ))
            time.sleep(random.uniform(1, 2))
        except Exception as e:
            print(f"Error scraping {city} {category}: {e}")
    return listings

cities = ['mumbai', 'pune', 'bangalore', 'delhi', 'hyderabad']
categories = ['restaurants', 'hospitals', 'hotels', 'gyms', 'salons']

all_listings = []
for city in cities:
    for category in categories:
        print(f"Scraping {category} in {city}...")
        data = scrape_sulekha(city, category)
        all_listings.extend(data)
        print(f"Got {len(data)} listings")

print(f"Total listings scraped: {len(all_listings)}")
if all_listings:
    insert_listings(all_listings)
else:
    print("No listings scraped. Inserting sample data instead.")