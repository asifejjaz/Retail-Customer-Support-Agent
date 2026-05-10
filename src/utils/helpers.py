"""
Utility helper functions
"""

import re
from typing import List


def normalize_query(query: str) -> List[str]:
    """Normalize and split search query into words"""
    query = query.lower().strip()

    # Remove trailing 's' unless word ends in 'ss'
    if query.endswith("s") and not query.endswith("ss"):
        query = query[:-1]

    # Split into words
    words = query.split()
    return [word for word in words if word]  # Remove empty strings


def format_currency(amount: float, currency: str = "£") -> str:
    """Format amount as currency"""
    return f"{currency}{amount:,.2f}"


def extract_price_from_query(query: str) -> tuple:
    """Extract price limit from query (e.g., 'under 5000' -> 5000)"""
    # Match patterns like "under 5000", "below 5000", "max 5000"
    pattern = r"(?:under|below|max|upto|up to)\s+(\d+(?:\.\d{2})?)"
    match = re.search(pattern, query, re.IGNORECASE)

    if match:
        return (query, float(match.group(1)))

    return (query, None)


def clean_product_name(name: str) -> str:
    """Clean product name for display"""
    return name.strip().title()


def chunk_list(items: list, chunk_size: int) -> list:
    """Split list into chunks of specified size"""
    return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]
