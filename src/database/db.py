"""
Database connection and operations
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Optional


class DatabaseManager:
    """Manages database connections and queries"""

    def __init__(self, db_path: str):
        """Initialize database manager"""
        self.db_path = db_path
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        """Ensure database directory exists"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    def connect(self):
        """Create database connection"""
        return sqlite3.connect(self.db_path)

    def search_products(
        self, query: str, max_price: Optional[float] = None, limit: int = 9
    ) -> List[Dict]:
        """Search for products matching query"""
        conn = self.connect()
        cursor = conn.cursor()

        try:
            # Normalize query
            query = query.lower().strip()
            if query.endswith("s") and not query.endswith("ss"):
                query = query[:-1]

            words = query.split()

            # Build WHERE clause
            conditions = []
            params = []
            for word in words:
                conditions.append(
                    "(LOWER(name) LIKE ? OR LOWER(category) LIKE ? OR LOWER(description) LIKE ?)"
                )
                params.extend([f"%{word}%", f"%{word}%", f"%{word}%"])

            sql = f"SELECT id, name, category, price, stock, description, product_url, image_url FROM products WHERE {' AND '.join(conditions)}"

            if max_price:
                sql += " AND price <= ?"
                params.append(max_price)

            sql += f" LIMIT {limit}"

            cursor.execute(sql, params)
            results = cursor.fetchall()

            unique_products = []
            seen = set()
            for r in results:
                product_key = (
                    r[1].strip().lower(),
                    r[2].strip().lower(),
                    r[3],
                    r[4],
                    r[5].strip().lower(),
                )
                if product_key in seen:
                    continue
                seen.add(product_key)
                unique_products.append(
                    {
                        "id": r[0],
                        "name": r[1],
                        "category": r[2],
                        "price": r[3],
                        "stock": r[4],
                        "description": r[5],
                        "product_url": r[6],
                        "image_url": r[7],
                    }
                )

            return unique_products
        finally:
            conn.close()

    def get_product(self, product_id: int) -> Optional[Dict]:
        """Get a specific product by ID"""
        conn = self.connect()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT id, name, category, price, stock, description, product_url, image_url FROM products WHERE id = ?",
                (product_id,),
            )
            result = cursor.fetchone()

            if result:
                return {
                    "id": result[0],
                    "name": result[1],
                    "category": result[2],
                    "price": result[3],
                    "stock": result[4],
                    "description": result[5],
                    "product_url": result[6],
                    "image_url": result[7],
                }
            return None
        finally:
            conn.close()

    def get_products_by_category(self, category: str, limit: int = 10) -> List[Dict]:
        """Get products by category"""
        conn = self.connect()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT id, name, category, price, stock, description, product_url, image_url FROM products WHERE LOWER(category) = ? LIMIT ?",
                (category.lower(), limit),
            )
            results = cursor.fetchall()

            products = [
                {
                    "id": r[0],
                    "name": r[1],
                    "category": r[2],
                    "price": r[3],
                    "stock": r[4],
                    "description": r[5],
                    "product_url": r[6],
                    "image_url": r[7],
                }
                for r in results
            ]

            return products
        finally:
            conn.close()
