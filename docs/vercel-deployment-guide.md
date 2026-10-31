# PlacementPilot & Campus Super-App — Vercel Deployment Guide

> **Target Platform:** [Vercel](https://vercel.com)  
> **Architecture:** Full-Stack Serverless (Vite React SPA Frontend + Python FastAPI Serverless Functions Backend)  
> **Configuration Files:** `vercel.json`, `api/index.py`, root `requirements.txt`, root `package.json`

---

## 1. Architecture Overview on Vercel

```
Incoming Request
       │
       ├── /api/*, /docs, /openapi.json ──────► api/index.py (FastAPI Serverless via @vercel/python)
       │
       └── All other routes (/*) ────────────► frontend/dist/ (Vite React SPA via rewrites)
```

1. **Frontend**: Vite compiles React + TypeScript + Tailwind into `frontend/dist`.
2. **Backend**: Vercel executes `api/index.py` using Python 3.12 Serverless Functions.
3. **Database**: Serverless functions are ephemeral, so production data is stored in a cloud-hosted PostgreSQL database (such as **Neon**, **Supabase**, or **Vercel Postgres**).
4. **CORS**: Requests to `/api/*` originate from the same domain in production. Preview URLs (`https://*-vercel.app`) are handled by regex in `CORSMiddleware`.

---

## 2. Environment Variables Configuration (Vercel Dashboard)

Under your Vercel Project **Settings -> Environment Variables**, add the following:

| Key | Example Value | Description |
|---|---|---|
| `APP_ENV` | `production` | Enables production mode |
| `DEBUG` | `false` | Disables debug stack traces in production |
| `SECRET_KEY` | `strong_random_secret_at_least_32_characters_here` | Key for JWT cryptographic signing |
| `DATABASE_URL` | `postgresql://user:pass@ep-host.region.aws.neon.tech/dbname?sslmode=require` | Connection string to cloud Postgres |
| `FRONTEND_ORIGIN` | `https://your-production-domain.vercel.app` | Production frontend domain |
| `AI_PROVIDER` | `mock` (or `gemini`) | AI provider selection |
| `AI_API_KEY` | `your_gemini_api_key` | Only needed if `AI_PROVIDER=gemini` |

> **Automatic Cloud URL Normalization:**  
> If your cloud provider supplies a URL starting with `postgres://` (e.g. Supabase, Neon), our `Settings.sync_database_url` converts it to `postgresql://` for SQLAlchemy 2.0.

---

## 3. Database Setup & Initial Migration

Because Vercel serverless functions do not run persistent background processes, run Alembic migrations once from your terminal targeting your cloud database:

```powershell
# Set your cloud database URL in your shell
$env:DATABASE_URL="postgresql://user:password@your-cloud-db-host/dbname?sslmode=require"

# Run migrations to create all 25 tables
backend\.venv\Scripts\alembic -c backend\alembic.ini upgrade head

# Optional: Seed initial development/demo data
backend\.venv\Scripts\python backend\scripts\seed_dev_data.py
```

---

## 4. Deploying to Vercel (2 Simple Methods)

### Method A: Git Push (Recommended)
1. Push your changes to GitHub: `git push origin main`.
2. Open [vercel.com](https://vercel.com) and click **"Add New Project"**.
3. Select your `campus-pilot` repository.
4. Keep the default settings (**Root Directory:** `./`).
5. Add the **Environment Variables** listed in Section 2.
6. Click **Deploy**. Vercel will build both the frontend and backend automatically.

### Method B: Vercel CLI
```powershell
# Install Vercel CLI globally if not already installed
npm install -g vercel

# Deploy preview
vercel

# Deploy to production
vercel --prod
```

---

## 5. Verification Checklist

After deployment finishes, verify:
- [ ] Frontend loads at: `https://<your-project>.vercel.app`
- [ ] API health endpoint responds: `https://<your-project>.vercel.app/api/v1/health`
- [ ] Swagger API Docs load: `https://<your-project>.vercel.app/docs`
- [ ] User registration / login works: `POST https://<your-project>.vercel.app/api/v1/auth/register`

