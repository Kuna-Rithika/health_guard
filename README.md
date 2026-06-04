# HealthGuard

HealthGuard is a small FastAPI + static frontend project demonstrating an AI-assisted health assistant.

## Requirements
- Python 3.10+
- pip

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Initialize Database

```bash
python backend/database.py
```

This creates `healthguard.db` and seeds demo users.

## Run Backend

Start the backend API server:

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

## Serve Frontend

The frontend is static files in the `frontend/` folder. To serve locally:

```bash
cd frontend
python -m http.server 8001
# then open http://127.0.0.1:8001/dashboard.html
```

Alternatively open the HTML files directly in your browser, but some browsers restrict `fetch()` on file:// URLs.

## Features
- Signup / Login (stores `user_id`, `user_name`, `token` in localStorage)
- Dashboard that loads user data and history dynamically
- Health analysis endpoint that runs AI pipeline and saves history
- PDF report generation endpoint: `/report/{user_id}`
- Chart.js visualizations on dashboard

## Useful commands (Windows PowerShell)

```powershell
# install deps
python -m pip install -r requirements.txt

# init DB
python backend/database.py

# start backend
python -m uvicorn backend.main:app --reload --port 8000

# serve frontend
Push-Location frontend; python -m http.server 8001; Pop-Location
```

## Notes
- The AI agents use a mock/local `groq_service` interface — replace with a real LLM service for production.
- The `report_generator` uses ReportLab to produce PDFs.

