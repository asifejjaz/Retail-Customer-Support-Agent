import os
import json
import sqlite3
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

URLS_TO_SCRAPE = [
    "https://nashadjewellers.com/pages/safety-deposit-boxes",
    "https://nashadjewellers.com/pages/custom-diamond-jewellery",
    "https://nashadjewellers.com/pages/contact",
    "https://nashadjewellers.com/pages/visit-us",
    "https://nashadjewellers.com/policies/refund-policy",
    "https://nashadjewellers.com/policies/shipping-policy",
    "https://nashadjewellers.com/policies/terms-of-service",
    "https://nashadjewellers.com/blogs/news/22ct-gold",
    "https://nashadjewellers.com/blogs/news/4cs-of-diamonds"
]

DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'knowledge_base.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            chunk_text TEXT,
            embedding_json TEXT
        )
    ''')
    # Clear old data if re-running
    cursor.execute('DELETE FROM documents')
    conn.commit()
    return conn

def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def scrape_and_chunk(url):
    print(f"Scraping {url}...")
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try to find the main content area to avoid nav/footers
        main_content = soup.find('main') or soup.find('body')
        if not main_content:
            return []
            
        chunks = []
        current_chunk = f"Source: {url}\n"
        
        # Extract meaningful text tags
        for tag in main_content.find_all(['h1', 'h2', 'h3', 'p', 'li']):
            text = tag.get_text(strip=True)
            if not text or len(text) < 15: # skip very short meaningless strings
                continue
            
            # Very basic chunking: group sentences together until ~1000 characters
            if len(current_chunk) + len(text) > 1000:
                chunks.append(current_chunk)
                current_chunk = f"Source: {url}\n" + text + " "
            else:
                current_chunk += text + "\n"
                
        if current_chunk.strip() and current_chunk != f"Source: {url}\n":
            chunks.append(current_chunk)
            
        return chunks
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return []

def build_kb():
    conn = init_db()
    cursor = conn.cursor()
    
    total_chunks = 0
    for url in URLS_TO_SCRAPE:
        chunks = scrape_and_chunk(url)
        for chunk in chunks:
            print(f"  Generating embedding for chunk ({len(chunk)} chars)...")
            try:
                emb = get_embedding(chunk)
                emb_json = json.dumps(emb)
                cursor.execute('INSERT INTO documents (url, chunk_text, embedding_json) VALUES (?, ?, ?)', (url, chunk, emb_json))
                total_chunks += 1
            except Exception as e:
                print(f"  Failed to embed chunk: {e}")
                
    conn.commit()
    conn.close()
    print(f"\nSuccessfully stored {total_chunks} vectorized chunks in {DB_PATH}!")

if __name__ == "__main__":
    build_kb()
