"""
Database setup and initialization
"""

import sqlite3
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class DatabaseSetup:
    """Handles database initialization and population"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    def create_schema(self):
        """Create database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT,
                price REAL,
                stock INTEGER DEFAULT 10,
                description TEXT,
                product_url TEXT,
                image_url TEXT
            )
        """
        )

        conn.commit()
        conn.close()
        logger.info("Database schema created successfully")

    def insert_products(self, products: List[Dict]):
        """Insert products into database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for product in products:
            cursor.execute(
                """
                INSERT OR IGNORE INTO products 
                (id, name, category, price, stock, description, product_url, image_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    product.get("id"),
                    product.get("name"),
                    product.get("category"),
                    product.get("price"),
                    product.get("stock", 10),
                    product.get("description"),
                    product.get("product_url"),
                    product.get("image_url"),
                ),
            )

        conn.commit()
        conn.close()
        logger.info(f"Inserted {len(products)} products")
