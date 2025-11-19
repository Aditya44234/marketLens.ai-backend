# MarketLens AI Backend

The **MarketLens AI Backend** is a Django-based RESTful API designed for analyzing real estate trends and integrating AI-powered data science. It is fully compatible with modern frontend frameworks (React/Next.js, Vercel deployments) and deploys seamlessly to Render for production use.

>  Try the live frontend: [market-lens-ai.vercel.app](https://market-lens-ai.vercel.app) 

---

## Table of Contents

- [Project Structure](#project-structure)
- [Key Features](#key-features)
- [Setup](#setup)
- [Deployment](#deployment-to-render)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Static and Media Files](#static-and-media-files)
- [Tech Stack](#tech-stack)
- [Contributing](#contributing)
- [License](#license)

---

## Project Structure

```

realestate_backend/
│
├── analysis/ # Main Django app (business logic, views, models)
├── realestate_api/ # Django project settings, wsgi, urls
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ └── init.py
├── static/ # Collected static files (not tracked in Git)
├── media/ # Uploaded media files (not tracked in Git)
├── manage.py # Django project runner
├── requirements.txt # All Python dependencies
├── Procfile # Process type declaration for Render/Heroku
├── .gitignore # Ignore venv, static, db, secrets
└── README.md 
```


- **analysis/**  
  Custom Django app with API endpoints (e.g., `/api/analyze/`).
- **realestate_api/**  
  Contains Django core configuration (settings, URLs, WSGI).
- **static/** and **media/**  
  Auto-generated. Not committed to Git—regenerated on deploy.

---

## Key Features

- **AI-driven analysis:** Uses Google Gemini and pandas for real estate data calculation.
- **REST API:** Fully compatible with frontend SPA frameworks, accepts and serves JSON.
- **CORS support:** Connect securely to production (Vercel) and local (localhost:5173) frontends.
- **Admin:** Built-in Django admin for data management.
- **Secure deployment:** SECRET_KEY and other secrets managed securely via environment variables.

---

## Setup

**1. Clone the repo:**

```
git clone https://github.com/Aditya44234/marketlens-ai-backend.git
cd marketlens-ai-backend
```


**2. Install dependencies:**
```
python -m venv venv
source venv/bin/activate # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```


**3. Environment setup:**
Create a `.env` file for local development (not tracked in Git):
```
DJANGO_SECRET_KEY=your-super-secret-key
GOOGLE_API_KEY=your-google-api-key
```


**4. Migrate DB and collect static files:**
```
python manage.py migrate
python manage.py collectstatic
```


**5. Run locally:**
```
python manage.py runserver
```

---
## Deployment to Render

1. **Push code to GitHub.**
2. **Create new Web Service on Render.**
3. **Connect your repository.**
4. **Set environment variables:**
   - `DJANGO_SECRET_KEY` (your secret key)
   - `GOOGLE_API_KEY` (Gemini API key, if used)
5. **Build command:**

```
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```

6. **Start command:**

```
gunicorn realestate_api.wsgi
```

7. **Update `ALLOWED_HOSTS` in settings.py with your Render URL.**
8. **Access live backend at:**

```
https://marketlens-ai-backend.onrender.com
```


---

## Environment Variables

| Name               | Purpose                                    |
|--------------------|--------------------------------------------|
| DJANGO_SECRET_KEY  | Django security key (DO NOT share)         |
| GOOGLE_API_KEY     | For Gemini AI integration                  |

Set these in your Render dashboard (recommended) or `.env` for local dev.

---

## API Endpoints

**Example:**

- `POST /api/analyze/`  
Analyzes provided real estate data and returns AI-powered insights.
---

## Static and Media Files

- Static files are collected to `/static` on `collectstatic` (not stored in git).
- Media files uploaded by users are stored in `/media`.
- Both paths are set in `settings.py` and automatically handled in deployment (not manually managed).

---

## Tech Stack

- **Backend:** Python, Django, Django REST Framework
- **Admin:** Django admin
- **AI Integration:** Google Gemini (via API)
- **Data:** pandas (for data analysis)
- **DevOps:** Render (production server), Gunicorn (WSGI), Vercel (frontend SPA)

---

## Contributing

Open to improvements—submit PRs or issues!

---

## License

MIT License (or your chosen license—update if needed).

---

**Contact:**  
For help, reach out via issues or connect at [adityajoshi4002@example.com].


