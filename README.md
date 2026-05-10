# Retail Customer Support Agent

A professional-grade AI-powered customer support chatbot for Nashad Jewellers. Built with Streamlit, OpenAI GPT-4, and SQLite.

## Features

- 💬 **AI-Powered Chat**: Natural language conversations with GPT-4o-mini
- 🔍 **Product Search**: Intelligent product discovery with grid display
- 💳 **Order Management**: Streamlined order placement process
- 📊 **Report Generation**: Automated report creation in Word format
- 📈 **Analytics**: Chart generation and performance tracking
- 🗄️ **Database**: 360+ jewelry products with full details


<img width="797" height="922" alt="Retail Store" src="https://github.com/user-attachments/assets/73426099-7db9-4384-8a38-342b6e11196e" />

## Project Structure

```
retail-agent/
├── src/                    # Source code
│   ├── chatbot/           # Streamlit application
│   ├── database/          # Database operations
│   ├── utils/             # Helper functions
│   └── reports/           # Report generation
├── config/                 # Configuration management
├── data/                   # Data files
│   ├── databases/         # SQLite databases
│   ├── reports/           # Generated reports
│   └── charts/            # Generated charts
├── tests/                  # Test suite
├── docs/                   # Documentation
├── requirements.txt        # Python dependencies
├── setup.py                # Package setup
└── .env.example            # Environment template
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

### 3. Initialize Database

```bash
python -m src.database.setup
```

### 4. Run the Application

```bash
streamlit run src/chatbot/app.py
```

The app will be available at `http://localhost:8501`

## Configuration

Edit `config/settings.py` to customize:
- OpenAI model selection
- Database path
- Display preferences
- Feature toggles

## API Reference

### Search Products

```python
from src.database import DatabaseManager
from config.settings import get_config

config = get_config()
db = DatabaseManager(config.DB_PATH)
products = db.search_products("gold rings", max_price=5000)
```

### Generate Reports

```python
from src.reports import ReportGenerator

generator = ReportGenerator()
report_path = generator.create_report(
    title="Customer Analysis",
    sections={
        "Summary": "Key findings...",
        "Recommendations": ["Item 1", "Item 2"]
    }
)
```

## Testing

Run tests:
```bash
pytest tests/
```

## Development

### Prerequisites
- Python 3.9+
- OpenAI API key
- Virtual environment

### Setup Development Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Contributing

1. Create a feature branch
2. Make changes
3. Write tests
4. Submit pull request

## License

MIT License - See LICENSE file for details

## Support

For issues or questions, contact: asifejaz.me@gmail.com
