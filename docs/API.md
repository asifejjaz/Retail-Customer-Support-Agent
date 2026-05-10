# API Documentation

## DatabaseManager

### Methods

#### `search_products(query: str, max_price: Optional[float] = None, limit: int = 9) -> List[Dict]`

Search for products matching the query.

**Parameters:**
- `query` (str): Search query
- `max_price` (float, optional): Maximum price filter
- `limit` (int): Maximum number of results (default: 9)

**Returns:**
- List of product dictionaries

**Example:**
```python
from src.database import DatabaseManager
from config.settings import get_config

db = DatabaseManager(get_config().DB_PATH)
products = db.search_products("gold rings", max_price=5000, limit=9)
```

#### `get_product(product_id: int) -> Optional[Dict]`

Get a specific product by ID.

**Parameters:**
- `product_id` (int): Product ID

**Returns:**
- Product dictionary or None if not found

**Example:**
```python
product = db.get_product(110)
print(product['name'], product['price'])
```

#### `get_products_by_category(category: str, limit: int = 10) -> List[Dict]`

Get products by category.

**Parameters:**
- `category` (str): Product category
- `limit` (int): Maximum number of results

**Returns:**
- List of product dictionaries

**Example:**
```python
rings = db.get_products_by_category("Ring", limit=20)
```

## ReportGenerator

### Methods

#### `create_report(title: str, sections: dict, filename: str = None) -> str`

Create a professional report in Word format.

**Parameters:**
- `title` (str): Report title
- `sections` (dict): Dictionary of section titles and content
- `filename` (str, optional): Custom filename

**Returns:**
- Path to generated report file

**Example:**
```python
from src.reports import ReportGenerator

generator = ReportGenerator()
report_path = generator.create_report(
    title="Product Analysis",
    sections={
        "Overview": "Summary of findings",
        "Top Products": ["Product 1", "Product 2", "Product 3"],
        "Recommendations": ["Increase stock", "Launch promotion"]
    }
)
```

## Utility Functions

### `normalize_query(query: str) -> List[str]`

Normalize and split search query into words.

### `format_currency(amount: float, currency: str = "£") -> str`

Format amount as currency string.

### `extract_price_from_query(query: str) -> tuple`

Extract price limit from natural language query.

**Example:**
```python
query, max_price = extract_price_from_query("show me rings under 5000")
# Returns: ("show me ring", 5000.0)
```

## Configuration

Access settings from `config/settings.py`:

```python
from config.settings import get_config

config = get_config()
print(config.APP_TITLE)  # "💎 Nashad Jewellers Assistant"
print(config.OPENAI_MODEL)  # "gpt-4o-mini"
print(config.PRODUCTS_PER_ROW)  # 3
```

### Available Configuration Classes

- `Config`: Base configuration
- `DevelopmentConfig`: Development settings (debug mode)
- `ProductionConfig`: Production settings (minimal logging)
