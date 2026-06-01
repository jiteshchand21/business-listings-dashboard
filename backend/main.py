from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from typing import List
import pandas as pd
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "business_dashboard"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.get("/")
def root():
    return {"message": "Business Dashboard API is running"}

@app.get("/city-wise")
def city_wise():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT city, COUNT(*) as count FROM listing_master GROUP BY city ORDER BY count DESC")
    result = cursor.fetchall()
    conn.close()
    return result

@app.get("/category-wise")
def category_wise():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT category, COUNT(*) as count FROM listing_master GROUP BY category ORDER BY count DESC")
    result = cursor.fetchall()
    conn.close()
    return result

@app.get("/source-wise")
def source_wise():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT source, COUNT(*) as count FROM listing_master GROUP BY source ORDER BY count DESC")
    result = cursor.fetchall()
    conn.close()
    return result

class Listing(BaseModel):
    business_name: str
    category: str
    city: str
    address: str
    phone: str
    source: str

@app.post("/insert-listings")
def insert_listings(listings: List[Listing]):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO listing_master (business_name, category, city, address, phone, source)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    data = [(l.business_name, l.category, l.city, l.address, l.phone, l.source) for l in listings]
    cursor.executemany(query, data)
    conn.commit()
    count = cursor.rowcount
    conn.close()
    return {"message": f"Successfully inserted {count} listings"}


