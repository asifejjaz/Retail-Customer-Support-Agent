"""
Tests for database operations
"""

import unittest
import tempfile
import os
from src.database import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    """Test cases for DatabaseManager"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test.db")

    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        os.rmdir(self.temp_dir)

    def test_database_initialization(self):
        """Test database connection initialization"""
        db = DatabaseManager(self.db_path)
        self.assertIsNotNone(db)

    def test_connect(self):
        """Test database connection"""
        db = DatabaseManager(self.db_path)
        conn = db.connect()
        self.assertIsNotNone(conn)
        conn.close()


if __name__ == "__main__":
    unittest.main()
