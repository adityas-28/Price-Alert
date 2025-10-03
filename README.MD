## PriceAlert — Price Tracker App

A simple price tracker that scrapes product pages and stores price history in MongoDB. The plan is to run scheduled scraping for listed products, visualize price history on the frontend, allow users to set price-drop alerts, and experiment with LSTM-based future price predictions. Currently, the scraper is implemented and saves product data to the database.

### Core features

- **Scraping to DB**: Save `asin`, `name`, `url`, `price` for a product.
- **Price history**: Track historical prices over time (via scheduled runs).
- **Alerts (planned)**: Notify when the price falls below a user-set threshold.
- **LSTM prediction (planned)**: Forecast future prices.

### Project structure

- `backend/`: API, DB utilities, tasks (cron-ready)
- `scraper/` or `bewakoof_scraper/`: Scraper scripts (Selenium/requests/BS4)
- `amazon_scraper/` (if present): Amazon-focused experiments
- `frontend/`: UI to submit product URLs and view history (planned)

### Technology

- **Python**, **Selenium/Requests/BeautifulSoup** for scraping
- **MongoDB** (Atlas or local)
- Planned: **Celery/cron** for schedules, **FastAPI/Flask** for API, **LSTM** (TensorFlow/PyTorch)

### Prerequisites

- Python 3.10+
- MongoDB (Atlas or local)
- Chrome + ChromeDriver (for Selenium-based scrapers)

### Setup

1. Create and activate a virtual environment

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install backend/scraper requirements

```bash
pip install -r backend/requirements/requirements.txt
```

3. Configure environment

- Set MongoDB URI (examples):
  - Atlas: `MONGODB_URI=mongodb+srv://USER:PASS@CLUSTER/db?retryWrites=true&w=majority`
  - Local: `MONGODB_URI=mongodb://localhost:27017`

### Running the scraper (current state)

- Provide a product URL and save to DB. Example patterns:

```bash
# From project root
python -m bewakoof_scraper.bewakoof_scraper
# or another scraper entry if present
python -m scraper.bewakoof_scraper
```

### Scheduling (cron/tasks)

- Goal: run a scheduled job (e.g., every 6 hours) to scrape all saved products and append new prices.
- Options:
  - System cron (Linux) or Task Scheduler (Windows)
  - Python scheduler (APScheduler) or Celery + beat for distributed scheduling

### API and frontend (planned)

- Backend API endpoints:
  - Add a product by URL
  - Get product price history
  - Set alert threshold
- Frontend:
  - Form to submit URL
  - Chart to visualize price history
  - Alert configuration

### Notes and tips

- For Atlas with TLS, install `certifi` and use `tlsCAFile=certifi.where()` in `MongoClient`.
- Allow your IP in Atlas Network Access.
- If using Selenium headless, ensure ChromeDriver version matches Chrome.

### Roadmap

- [ ] Finalize unified scraper interface
- [ ] Add product listing + scheduled job
- [ ] Expose REST API for products/history/alerts
- [ ] Frontend price history chart + alert UI
- [ ] LSTM model experiment and endpoint
