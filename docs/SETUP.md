# Setup and Installation

## System Requirements

- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/asifejjaz/Retail-Customer-Support-Agent.git
cd Retail-Customer-Support-Agent
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create `.env` file in project root:

```env
OPENAI_API_KEY=your_api_key_here
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### 5. Initialize Database

```bash
python -c "from src.database.setup import DatabaseSetup; from config.settings import get_config; s = DatabaseSetup(get_config().DB_PATH + '/jewelry_store.db'); s.create_schema()"
```

### 6. Run Application

```bash
streamlit run src/chatbot/app.py
```

## Troubleshooting

### ImportError: No module named 'streamlit'

**Solution**: Ensure virtual environment is activated and requirements are installed
```bash
pip install -r requirements.txt
```

### OpenAI API Key Error

**Solution**: Verify `.env` file has valid `OPENAI_API_KEY`
```bash
# Check if .env exists
cat .env
```

### Database Connection Error

**Solution**: Ensure data/databases directory exists
```bash
mkdir -p data/databases
```

## Development Setup

### Additional Dependencies for Development

```bash
pip install pytest pytest-cov black flake8 mypy
```

### Code Formatting

```bash
black src/
flake8 src/
```

### Type Checking

```bash
mypy src/
```

## Running Tests

```bash
pytest tests/ -v
```

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for production setup guidelines.
