"""
Tests for utility functions
"""

import unittest
from src.utils.helpers import (
    normalize_query,
    format_currency,
    extract_price_from_query,
    chunk_list,
)


class TestHelperFunctions(unittest.TestCase):
    """Test cases for helper functions"""

    def test_normalize_query(self):
        """Test query normalization"""
        result = normalize_query("Gold Rings")
        self.assertEqual(result, ["gold", "ring"])

    def test_format_currency(self):
        """Test currency formatting"""
        result = format_currency(1234.56)
        self.assertEqual(result, "£1,234.56")

    def test_extract_price_from_query(self):
        """Test price extraction from query"""
        query, price = extract_price_from_query("show me rings under 5000")
        self.assertEqual(price, 5000.0)

    def test_chunk_list(self):
        """Test list chunking"""
        items = list(range(10))
        chunks = chunk_list(items, 3)
        self.assertEqual(len(chunks), 4)
        self.assertEqual(len(chunks[0]), 3)


if __name__ == "__main__":
    unittest.main()
