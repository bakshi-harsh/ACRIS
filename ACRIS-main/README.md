# HireFlow — AI Career Intelligence Platform

A production-ready SaaS web app built with **FastAPI + Jinja2 + SQLite + Google OAuth**.

---

## Project Structure

```
backend/
├── main.py                  # FastAPI application
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── app.db                   # SQLite database (auto-created)
├── uploads/                 # Resume uploads (auto-created)
├── static/
│   └── style.css            # Premium SaaS dark theme CSS
└── templates/
    ├── landing.html          # Landing page
    ├── login.html            # Login page
    ├── register.html         # Register page
    └── dashboard.html        # Protected dashboard
```

---

## Setup Instructions

### 1. Clone / navigate to backend/

```bash
cd backend
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in:

```env
SECRET_KEY=any-long-random-string
GOOGLE_CLIENT_ID=<from Google Cloud Console>
GOOGLE_CLIENT_SECRET=<from Google Cloud Console>
```

### 5. Set up Google OAuth (optional but recommended)

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a project → APIs & Services → Credentials
3. Create OAuth 2.0 Client ID (Web Application)
4. Add **Authorized Redirect URI**: `http://localhost:8000/auth/google/callback`
5. Copy Client ID + Secret to `.env`

> **Note:** Without Google credentials, the Google OAuth button will fail gracefully. Email/password login works independently without any setup.

### 6. Run the application

```bash
uvicorn main:app --reload --port 8000
```

Open: [http://localhost:8000](http://localhost:8000)

---

## Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Landing page |
| `/login` | GET/POST | Email login |
| `/register` | GET/POST | Email registration |
| `/dashboard` | GET | Protected dashboard |
| `/submit-profile` | POST | Save job preferences + resume |
| `/logout` | GET | Clear session |
| `/auth/google` | GET | Start Google OAuth |
| `/auth/google/callback` | GET | Google OAuth callback |

---

## Features

- **Google OAuth** — one-click sign in/sign up via Google
- **Email/Password Auth** — SHA-256 hashed passwords
- **Session-based auth** — via `SessionMiddleware` (secure cookie)
- **Resume upload** — PDF/DOCX stored in `uploads/`
- **Job preferences** — persisted per user in SQLite
- **Dynamic navbar** — shows Login/Register vs Dashboard/Logout
- **Protected routes** — dashboard redirects unauthenticated users to `/login`

---

## Tech Stack

- **FastAPI** — async Python web framework
- **Jinja2** — server-side HTML templating
- **SQLite** — zero-config local database
- **Authlib** — Google OAuth 2.0
- **Starlette SessionMiddleware** — signed cookie sessions
- **Google Fonts** — Syne + DM Sans
