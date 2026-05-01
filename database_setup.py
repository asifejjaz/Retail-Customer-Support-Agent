import sqlite3
import os
import requests
from bs4 import BeautifulSoup
import re
import time

DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'jewelry_store.db')
BASE_URL = "https://nashadjewellers.com"

def scrape_products():
    print("Gathering products from all collection pages...")
    products = []
    
    for page_num in range(1, 16):
        url = f"{BASE_URL}/collections/all?page={page_num}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
        print(f"Scraping {url}...")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            blocks = soup.find_all(class_='product-block')
            for block in blocks:
                # URL
                link_el = block.find('a', class_='product-link')
                if not link_el: continue
                product_url = BASE_URL + link_el['href']
                
                # Image
                img_el = block.find('img')
                image_url = ""
                if img_el and img_el.has_attr('src'):
                    image_url = img_el['src']
                    if image_url.startswith('//'):
                        image_url = 'https:' + image_url
                        
                # Title
                title_el = block.find(class_='product-block__title')
                title = title_el.text.strip() if title_el else "Unknown Product"
                
                # Price
                price_el = block.find(class_='price__current')
                price = 0.0
                if price_el:
                    price_str = price_el.text.strip().replace('£', '').replace(',', '')
                    found_prices = re.findall(r"[-+]?\d*\.\d+|\d+", price_str)
                    if found_prices:
                        price = float(found_prices[0])
                        
                # Category
                title_lower = title.lower()
                if 'ring' in title_lower: category = 'Ring'
                elif 'necklace' in title_lower or 'pendant' in title_lower: category = 'Necklace'
                elif 'bracelet' in title_lower or 'bangle' in title_lower or 'kareh' in title_lower: category = 'Bracelet'
                elif 'earring' in title_lower or 'hoop' in title_lower or 'stud' in title_lower: category = 'Earring'
                elif 'anklet' in title_lower: category = 'Anklet'
                else: category = 'Other'
                
                desc = f"Beautiful {category.lower()} from Nashad Jewellers."
                
                if not any(p[5] == product_url for p in products):
                    products.append((title, category, price, 10, desc, product_url, image_url))
                    
            time.sleep(3) # Be polite and bypass Cloudflare
        except Exception as e:
            print(f"Error on page {page_num}: {e}")
            
    if not products:
        print("Scraping blocked by Cloudflare anti-bot protection. Using rich mock data for demonstration.")
        products = [
            ("Amina Bangle Pair", "Bracelet", 6140.00, 5, "The Amina Bangle Pair is a delicate set, crafted from 22-carat gold and weighing approximately 39.6 grams. Features intricate Kareh detailing.", "https://nashadjewellers.com/products/amina-kareh-bangles-39-6g", "https://nashadjewellers.com/cdn/shop/files/Kareh7_3525914e-a3e8-46da-8118-a960062b2abe.jpg?v=1724772462&width=500"),
            ("Amena Hoops 6.2g", "Earring", 950.00, 8, "22ct Gold Hoop Earrings, meticulously handcrafted to embody timeless luxury.", "https://nashadjewellers.com/products/amena-hoops-6-2g", "https://nashadjewellers.com/cdn/shop/files/FBEF44AB-5AAD-4A60-A354-4C2D18D17FA6.jpg?width=500"),
            ("0.75ct Round Solitaire Pendant", "Necklace", 860.00, 3, "Beautiful round solitaire pendant.", "https://nashadjewellers.com/products/0-75ct-round-solitaire-pendant", "https://nashadjewellers.com/cdn/shop/files/FBEF44AB-5AAD-4A60-A354-4C2D18D17FA6.jpg?width=500"),
            ("Diamond Elegance Ring", "Ring", 1250.00, 5, "18k Gold ring with a beautiful 1-carat diamond.", "https://nashadjewellers.com/products/diamond-elegance-ring", "https://nashadjewellers.com/cdn/shop/files/FBEF44AB-5AAD-4A60-A354-4C2D18D17FA6.jpg?width=500"),
            ("Alia Bangle Set 73g", "Bracelet", 11315.00, 1, "Luxurious 22ct gold bangle set.", "https://nashadjewellers.com/products/alia-bangle-set", "https://nashadjewellers.com/cdn/shop/files/Kareh7_3525914e-a3e8-46da-8118-a960062b2abe.jpg?v=1724772462&width=500")
        ]
    else:
        print(f"Successfully scraped {len(products)} products with basic details and images.")
        
    return products

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS orders')
    cursor.execute('DROP TABLE IF EXISTS products')

    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            description TEXT,
            product_url TEXT,
            image_url TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            customer_name TEXT,
            customer_address TEXT,
            status TEXT,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')

    products = scrape_products()

    cursor.executemany('''
        INSERT INTO products (name, category, price, stock, description, product_url, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', products)

    conn.commit()
    conn.close()
    print(f"Database initialized with {len(products)} products at {DB_PATH}")

if __name__ == "__main__":
    setup_database()
