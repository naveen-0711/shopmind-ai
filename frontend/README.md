# ShopMind AI

AI-powered shopping decision engine that helps users **search, compare, and understand products before buying**.

## Features

- Natural-language product search
- Google Shopping product search via SerpApi
- Product normalization & duplicate detection
- Multi-store offer comparison
- Price intelligence & price history
- Deal detection
- ShopMind recommendation score
- Recommendation reasons
- Best Overall / Best Value / Cheapest / Best Rated / Best Deal
- Pros & Cons analysis
- Product details page
- Automated backend tests

## Tech Stack

**Frontend**
- React
- TypeScript
- Vite
- React Router
- Lucide React

**Backend**
- Python 3.10
- FastAPI
- Pydantic
- SQLAlchemy
- Uvicorn
- Pytest

**Database**
- PostgreSQL

**External API**
- SerpApi + Google Shopping

## Project Structure

```text
shopmind-ai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── ingestion/
│   │   ├── intelligence/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   └── services/
│   ├── tests/
│   ├── requirements.txt
│   └── pytest.ini
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
│
└── README.md


### Run Backend
cd E:\shopmind-ai\backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload

Backend:

http://127.0.0.1:8000

API docs:

http://127.0.0.1:8000/docs
Run Frontend

Open another terminal:

cd E:\shopmind-ai\frontend
npm install
npm run dev

### Frontend:

http://localhost:5173


User
  ↓
React Frontend
  ↓
FastAPI Backend
  ↓
SerpApi / Google Shopping
  ↓
Product Processing
  ├── Normalization
  ├── Offer Grouping
  ├── Price Intelligence
  ├── Deal Detection
  ├── Ranking
  ├── Comparison
  └── Pros & Cons
  ↓
Shopping Decision
