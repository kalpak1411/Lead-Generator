# Lead Research & Qualification Assistant

An intelligent, production-ready Python & Django platform that automates company research, Ideal Customer Profile (ICP) qualification, and drafts personalized outreach angles grounded in verified evidence.

> **Strict Anti-Hallucination Mandate:** The assistant strictly uses verified textual evidence from the target company's public website and publicly supplied context. It **never invents personal details**, fake mutual connections, or unverified claims.

---

## 🌟 Key Capabilities

1. **Automated Web Scraping Engine** ([`assistant/services/scraper.py`](assistant/services/scraper.py)):
   - Fetches live website metadata, page titles, OpenGraph descriptions, structural headers (`<h1>`, `<h2>`), and core narrative paragraphs.
   - Cleans HTML, extracts navigational offerings, and strips out scripts, trackers, and noise.

2. **ICP Qualification Engine** ([`assistant/services/qualifier.py`](assistant/services/qualifier.py)):
   - Analyzes company positioning against custom Ideal Customer Profiles (industry alignment, company size, stated pain points, target market model B2B vs B2C).
   - Computes a numerical fit score (0-100) and assigns an actionable tier: `Strong Fit`, `Moderate Fit`, `Low Fit`, or `Disqualified`.
   - Generates transparent, bulleted qualification justification reasons.

3. **Evidence Citations & Quote Verification**:
   - Collects exact text excerpts with source URLs directly from the scraped website.
   - Anchors outreach angles directly to these quotes, providing ground-truth verification.

4. **Personalized Outreach Angle Generator**:
   - Drafts role-aware outreach emails referencing the company's real products and pain points.
   - Strictly respects supplied information (e.g., if no personal contact name is provided, addresses the team neutrally without fabricating identity).
   - Built-in 1-click clipboard copy and in-place editing.

5. **Export & Multi-Profile Management**:
   - Create and customize multiple Ideal Customer Profiles (ICPs) with distinct pain points, value propositions, and disqualifying negative signals.
   - Download complete lead dossiers and evidence citations in CSV format.

---

## 🚀 Quick Start Instructions (Local Execution)

### 1. Prerequisites
- Python 3.10+ installed.

### 2. Setup Virtual Environment & Install Dependencies
Open Windows PowerShell or your terminal in the `Lead Generator` folder:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Run Migrations & Seed Sample Data
```powershell
python manage.py migrate
python seed_demo.py
```

### 4. Start the Django Server
```powershell
python manage.py runserver
```

Open your browser and navigate to: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🌐 Deploying Live to Production

The application is structured to deploy smoothly to any modern cloud host:

### Option A: Railway / Render / Fly.io
1. Add a `Procfile` containing:
   ```procfile
   web: gunicorn core.wsgi:application
   ```
2. Set Environment Variables:
   - `DJANGO_SECRET_KEY`: High-entropy random key.
   - `DJANGO_DEBUG`: `False`
   - `ALLOWED_HOSTS`: `yourdomain.com,*.railway.app`
3. Static files are collected using `python manage.py collectstatic`.

### Option B: DigitalOcean / AWS EC2 / VPS with Nginx & Gunicorn
1. Install Gunicorn: `pip install gunicorn`
2. Run Gunicorn: `gunicorn --workers 3 --bind 127.0.0.1:8000 core.wsgi:application`
3. Configure Nginx reverse proxy pointing to `127.0.0.1:8000`.

---

## 📂 Project Structure

```
Lead Generator/
├── core/                   # Django Project Configuration
│   ├── settings.py         # Config with .env and static files
│   ├── urls.py             # Root routing
│   └── wsgi.py             # Production WSGI gateway
├── assistant/              # Qualification & Research App
│   ├── models.py           # Lead & IdealCustomerProfile models
│   ├── views.py            # Dashboard, lead dossier, live scraper & CSV export
│   ├── urls.py             # App URL patterns
│   └── services/
│       ├── scraper.py      # BeautifulSoup live website extraction
│       └── qualifier.py    # ICP scoring & evidence-grounded outreach drafting
├── templates/assistant/    # Responsive UI with Dark/Light mode
│   ├── base.html           # Shared layout, sidebar & navigation
│   ├── dashboard.html      # Stats counters & recent companies
│   ├── lead_list.html      # Filterable lead directory
│   ├── lead_create.html    # Web research input form
│   ├── lead_detail.html    # Full dossier, evidence quotes & copyable pitch
│   └── icp_list.html       # ICP profile definitions & rules
├── static/css/main.css     # Clean modern SaaS styling
├── seed_demo.py            # Demo seeder with real companies (Datadog, Snyk, Chewy)
├── requirements.txt        # Dependencies
└── manage.py
```

