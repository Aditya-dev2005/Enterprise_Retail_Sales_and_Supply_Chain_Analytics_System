# Enterprise Retail Sales – Inventory – Supply Chain Analytics Platform

A backend platform that ingests raw retail data through an automated
ETL pipeline, stores it in MySQL, and exposes it through a full REST
API — including an AI-powered natural language query interface.

Built as a team training project and extended into a full-fledged
platform with pipeline automation and AI capabilities.

---

## 🚀 Features

- **ETL Data Pipeline** — Extract → Validate → Transform → Load, with
  rejected-record logging so bad data is never silently lost.
- **29 REST API endpoints** across Products, Customers, Stores, Sales,
  Inventory, Analytics, Pipeline, and AI modules.
- **Pipeline-as-a-Service** — trigger the ETL pipeline directly via an
  API call, with background execution, live status, run history, and
  log access — no manual script running required.
- **AI Query Endpoint** — ask questions about the data in plain
  English (e.g. *"Which store had the highest sales last month?"*)
  and get back both the generated SQL and a natural-language answer,
  powered by an LLM via [OpenRouter](https://openrouter.ai/).
- **Analytics API** — top-selling products, store-wise performance,
  and daily sales trends.
- **JWT Authentication** — all write operations (create/update/delete
  across Products, Customers, Stores, Sales, and the pipeline trigger)
  are protected behind a bearer token. Read endpoints stay public.
  Login integrates directly with Swagger UI's "Authorize" button.
- **Structured logging & custom exceptions** across every module for
  clean, traceable error handling.

---

## 🛠️ Tech Stack

| Layer          | Technology                     |
|----------------|---------------------------------|
| API Framework  | FastAPI                        |
| ORM            | SQLAlchemy                     |
| Database       | MySQL                          |
| Data Pipeline  | Pandas                         |
| AI Integration | OpenRouter (LLM API gateway)   |
| Server         | Uvicorn                        |

---

## 📂 Project Structure

```
├── api/                # All API route modules (products, sales, stores,
│                        # customers, inventory, analytics, pipeline, ai)
├── configs/             # Settings & environment configuration
├── database/            # DB connection + table creation script
├── models/               # SQLAlchemy ORM models
├── schemas/              # Pydantic request/response schemas
├── services/             # Business logic (e.g. AI query service)
├── pipeline/             # ETL pipeline (extract, validate, transform, load)
├── data/                 # Raw & rejected CSV data
├── logger_config.py      # Centralized logging setup
└── main.py                # FastAPI app entry point
```

---

## ⚙️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/<repo-name>.git
   cd <repo-name>
   ```

2. **Create a virtual environment & install dependencies**
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS/Linux
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Copy `.env.example` to `.env` and fill in your own values:
   ```bash
   cp .env.example .env
   ```

4. **Create the database tables**
   ```bash
   python -m database.create_tables
   ```

5. **Run the ETL pipeline** (loads sample data from `data/raw/`)
   ```bash
   python -m pipeline.run_pipeline
   ```
   Or trigger it via API once the server is running:
   `POST /api/pipeline/run`

6. **Start the API server**
   ```bash
   uvicorn main:app --reload
   ```

7. **Explore the API**
   Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for
   the interactive Swagger UI.

---

## 🔑 Environment Variables

| Variable            | Description                                  |
|----------------------|-----------------------------------------------|
| `DB_HOST`            | MySQL host                                    |
| `DB_USERNAME`        | MySQL username                                |
| `DB_PASSWORD`        | MySQL password                                |
| `DB_PORT`            | MySQL port (default `3306`)                   |
| `DB_NAME`            | Database name                                 |
| `OPENROUTER_API_KEY` | API key from [openrouter.ai](https://openrouter.ai/keys) |
| `OPENROUTER_MODEL`   | Model ID (a free model is set by default)     |

---

## 📡 API Overview

| Module     | Endpoints |
|------------|-----------|
| Auth       | Register, login, current user |
| Products   | Create 🔒, list, get by ID, update 🔒, delete 🔒 |
| Customers  | Create 🔒, list, get by ID, update 🔒, delete 🔒 |
| Stores     | Create 🔒, list, get by ID, update 🔒 |
| Sales      | Create 🔒, list, get by ID, update 🔒, delete 🔒 |
| Inventory  | List, by store, low-stock alert |
| Analytics  | Top products, store-wise sales, daily sales trends |
| Pipeline   | Run 🔒, status, history, logs |
| AI         | Natural language query |

🔒 = requires a valid JWT bearer token

Full request/response details are available in the auto-generated
Swagger docs at `/docs`.

---

## 🧠 AI Query — How It Works

1. You send a plain-English question to `POST /api/ai/query`.
2. An LLM (via OpenRouter) converts it into a single, read-only SQL
   `SELECT` query based on the database schema.
3. The query is validated — only `SELECT` statements are allowed;
   any destructive keyword (`DROP`, `DELETE`, `UPDATE`, `INSERT`,
   etc.) is rejected before it ever touches the database.
4. The query runs, and the results are sent back to the LLM to
   generate a short natural-language answer.

Example:
```json
POST /api/ai/query
{
  "question": "Which store had the highest total sales?"
}
```

---

## 👥 Team

| Name              | Module Owned                              |
|-------------------|--------------------------------------------|
| Mukund Chaturvedi | Initial setup, DB models, Products API     |
| Kriti Puri        | Data extraction, Stores API                |
| Mrigank Rai       | Data validation, Customers API             |
| Aditya Chaturvedi | Data transformation, Sales API             |
| Saad Ahmed        | Pipeline execution, Inventory API          |
| Tanishka Tyagi    | Logging & exception handling, Analytics API|

---

## 🙏 Acknowledgements

A big thank you to **Saurabh Aggarwal** for his guidance and mentorship
throughout this project — his feedback pushed us to take this from a
training assignment to a genuinely full-fledged platform.

---

## 🔐 Authentication

1. Register: `POST /api/auth/register` with `{ "username", "password" }`
   — returns a JWT access token immediately.
2. Login: `POST /api/auth/login` (standard OAuth2 form) — also works
   directly from the "Authorize" button in Swagger UI at `/docs`.
3. Include the token on protected requests:
   `Authorization: Bearer <your_token>`

---

## 🔮 Future Enhancements

- Role-based access control (admin-only endpoints)
- Upsert logic in the pipeline for updating existing records
- Pagination & filtering on list endpoints
- Automated testing (Pytest) + CI/CD
- Frontend dashboard for analytics visualization
- Rate limiting on the AI query endpoint

---

## 📄 License

This project was built for educational/training purposes.
