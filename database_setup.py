import sqlite3
import os
import requests
from bs4 import BeautifulSoup
import re

DB_PATH = os.path.join(os.path.dirname(__file__), 'jewelry_store.db')

def scrape_products():
    url = "https://nashadjewellers.com/collections/all"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    products = []
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # On shopify sites, products are usually in grid items.
        # We can look for product titles or prices based on common classes or just grab all a tags with href containing '/products/'
        # Let's use a simpler heuristic for the scraped text structure if HTML is tricky, or just extract from HTML.
        
        # Look for product cards
        for item in soup.find_all('a', href=re.compile(r'/products/')):
            title_el = item.find(['h3', 'span', 'div'], string=re.compile(r'[A-Za-z]'))
            price_el = item.find(['span', 'div'], string=re.compile(r'£'))
            
            if title_el and price_el:
                title = title_el.text.strip()
                price_str = price_el.text.strip().replace('£', '').replace(',', '')
                try:
                    price = float(re.findall(r"[-+]?\d*\.\d+|\d+", price_str)[0])
                except (ValueError, IndexError):
                    continue
                
                # Determine category based on title
                title_lower = title.lower()
                if 'ring' in title_lower: category = 'Ring'
                elif 'necklace' in title_lower or 'pendant' in title_lower: category = 'Necklace'
                elif 'bracelet' in title_lower or 'bangle' in title_lower or 'kareh' in title_lower: category = 'Bracelet'
                elif 'earring' in title_lower or 'hoop' in title_lower or 'stud' in title_lower: category = 'Earring'
                elif 'anklet' in title_lower: category = 'Anklet'
                else: category = 'Other'
                
                # Avoid duplicates
                if not any(p[0] == title for p in products):
                    products.append((title, category, price, 10, f"Beautiful {category.lower()} from Nashad Jewellers."))
                    
    # Fallback mock data if scraping fails or returns empty
    if not products:
        print("Scraping failed or no products found. Using mock data.")
        products = [
            ("Diamond Elegance Ring", "Ring", 1250.00, 5, "18k Gold ring with a beautiful 1-carat diamond."),
            ("Silver Infinity Necklace", "Necklace", 120.50, 15, "Sterling silver necklace with an infinity pendant."),
            ("Rose Gold Charm Bracelet", "Bracelet", 350.00, 8, "Rose gold bracelet with customizable charms."),
            ("Pearl Drop Earrings", "Earring", 250.00, 12, "Classic pearl drop earrings set in white gold."),
            ("0.75ct Round Solitaire Pendant", "Necklace", 860.00, 3, "Beautiful round solitaire pendant."),
            ("Aamina bracelet 11.9g", "Bracelet", 2025.00, 2, "Elegant 11.9g bracelet."),
            ("Alia Bangle Set 73g", "Bracelet", 11315.00, 1, "Luxurious bangle set.")
        ]
    else:
        print(f"Successfully scraped {len(products)} products from the website.")
        
    return products

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            description TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            customer_name TEXT,
            customer_address TEXT,
            status TEXT,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')

    cursor.execute('DELETE FROM products')
    cursor.execute('DELETE FROM orders')

    products = scrape_products()

    cursor.executemany('''
        INSERT INTO products (name, category, price, stock, description)
        VALUES (?, ?, ?, ?, ?)
    ''', products)

    conn.commit()
    conn.close()
    print(f"Database initialized with {len(products)} products at {DB_PATH}")

if __name__ == "__main__":
    setup_database()
