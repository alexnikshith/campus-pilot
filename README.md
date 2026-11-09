# PlacementPilot & Campus Super-App 🚀

> **AI-Powered Placement Preparation & Unified Campus Platform for Engineering Students**  
> Complete preparation ecosystem: Diagnostic Assessments, Deterministic Study Plans, Coding Practice, Resume ATS Parsing, and Mock Interviews — alongside a complete Campus Super-App (*AI Study Assistant, Opportunity Hub, Marketplace, Community, and Hostel Services*).

---

## 🌟 The 5 Campus & Preparation Pillars

### 1. 📚 AI Study Assistant
Students upload lecture notes and PDFs:
- **Automatic Summarization:** Executive and topic-wise breakdown.
- **Note-Based MCQs:** Generates targeted practice quizzes directly from uploaded lecture material.
- **Interactive Note Q&A:** Grounded answers to student doubts based on uploaded notes.
- **Adaptive Flashcards:** Key term flashcard decks with spaced mastery tracking.
- **Revision Schedules:** Generates structured exam revision plans.

### 2. 💼 Universal Opportunity Hub
A dedicated, verified board for engineering students to discover:
- **Internships & Full-Time Jobs**
- **Hackathons & Coding Competitions**
- **Research Opportunities & Fellowships**
- **Scholarships & Grants**
- **Placement Preparation Resources**  
*Features:* Filter by graduation year, branch, and CGPA, with a personalized application status tracking pipeline (`Interested` $\rightarrow$ `Applied` $\rightarrow$ `Interview` $\rightarrow$ `Offer`).

### 3. 🛒 Campus Marketplace
Trusted peer-to-peer student marketplace restricted to a single campus:
- Second-hand textbooks & engineering notes.
- Scientific calculators & lab equipment.
- Used hostel furniture & electronics.
- Student tutoring and campus-approved services.

### 4. 🎓 Campus Community & Collaboration
Student networking and project incubator:
- **Club Discovery:** Technical clubs (Coding, Robotics, AI) and cultural societies.
- **Hackathon Teammate Finder:** Post team requests by role (e.g., *"Need Frontend Dev for SIH 2026"*).
- **Project Showcase:** Share ideas, open-source repositories, and research initiatives.
- **Campus Event Feed:** Hackathon and seminar announcements.

### 5. 🏠 Hostel & Campus Facility Services
Campus grievance and maintenance ticketing system:
- Report issues with photo attachments and exact locations (*e.g., "Broken water dispenser on 2nd floor, Block B"*).
- Real-time ticket lifecycle tracking (`Open` $\rightarrow$ `Acknowledged` $\rightarrow$ `In Progress` $\rightarrow$ `Resolved`).
- Staff resolution notes and student feedback.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 18, Vite 5, TypeScript 5, Tailwind CSS 3, Lucide React, Recharts, React Hook Form, Zod |
| **Backend** | Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic, Uvicorn, Argon2id, HTTPX, PyPDF |
| **Database** | PostgreSQL 16 (Docker Compose / native Windows service), Asyncpg, Psycopg2-binary |
| **Testing** | Pytest, Vitest, React Testing Library, JSDOM |
| **AI Layer** | Provider-independent abstraction (Gemini 1.5, OpenAI, Mock Fallback) |

---

## 🚀 Development Progress & Roadmap Status

| Phase | Module | Status | Verification & Tests |
|---|---|:---:|---|
| **Phase 1** | Project Initialization & Base Stack | ✅ Complete | Python 3.12 venv, FastAPI, React 18, Vite 5, Tailwind CSS |
| **Phase 2** | Database Models & Initial Migrations | ✅ Complete | 25 SQLAlchemy 2.0 ORM models, Alembic schema `001_initial_unified_schema` |
| **Phase 3** | Core Infrastructure & Standard Envelope | ✅ Complete | `ResponseEnvelope[T]`, request tracing, centralized exception handling |
| **Phase 4** | Authentication, RBAC & Security Bounds | ✅ Complete | Argon2id hashing, scoped JWTs, rate-limiting, resource ownership guards |
| **Phase 5** | Frontend Design System & Shell Architecture | ✅ Complete | High-craft UI primitives, responsive dual-nav sidebar, protected routes |
| **Phase 6** | Student Profile & Onboarding Engine | ✅ Complete | 5-dimension completeness scoring, skills taxonomy, 4-step wizard |
| **Phase 7** | Readiness Assessment Engine | ✅ Complete | 6 subjects, timed attempts, server-side grading, diagnostic breakdown |
| **Phase 8** | Deterministic Study Planner | ⏳ Next | Weakness-driven calendar schedules, daily task generation |
| **Phase 9** | Coding Practice Sandbox | 📋 Planned | In-browser code runner, problem set, test cases |
| **Phase 10** | ATS Resume Scanner | 📋 Planned | PDF parsing, keyword extraction, score reports |
| **Phase 11** | Mock Interview Simulator | 📋 Planned | Speech/text interview drills, feedback reports |
| **Phase 12-22** | Campus Super-App Features & Final Deploy | 📋 Planned | Study assistant, opportunity hub, marketplace, community, hostel |

**Current Quality Baseline:**
- **Backend Tests:** 52 / 52 Pytest passed (100%)
- **Frontend Tests:** 26 / 26 Vitest passed (100%)
- **Production Build:** TypeScript + Vite bundle passed with 0 errors

---

## 📁 Repository Structure

```
startup/
├── backend/
│   ├── app/
│   │   ├── api/v1/routes/     # Modular route controllers
│   │   ├── core/              # Settings, security, config
│   │   ├── db/                # SQLAlchemy session, engine, verifier
│   │   ├── models/            # SQLAlchemy 2.0 database models
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   ├── services/          # Business logic & algorithms
│   │   ├── repositories/      # Database queries
│   │   └── main.py            # FastAPI application entrypoint
│   ├── alembic/               # Database migration scripts
│   ├── tests/                 # Pytest test suite
│   ├── requirements.txt       # Python dependencies
│   ├── pytest.ini             # Pytest config
│   └── alembic.ini            # Alembic migration config
├── frontend/
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/             # Page views
│   │   ├── test/              # Vitest test files
│   │   ├── App.tsx            # Root application component
│   │   └── index.css          # Tailwind CSS stylesheet
│   ├── package.json           # Frontend dependencies & scripts
│   ├── vite.config.ts         # Vite bundler & Vitest config
│   └── tailwind.config.js     # Design tokens & color system
├── docs/
│   ├── implementation-plan.md # Master 22-phase roadmap & task status
│   ├── architecture.md        # System design & security blueprint
│   ├── database-schema.md     # Relational schema for all 5 pillars
│   ├── setup-guide.md         # Environment setup instructions
│   ├── api-documentation.md   # Complete REST API reference
│   └── testing-guide.md       # Testing guidelines & results
├── scripts/
│   ├── verify_db.py           # Database connectivity verifier
│   ├── run_backend.bat        # One-click backend dev server startup
│   ├── run_frontend.bat       # One-click frontend dev server startup
│   └── run_tests.bat          # One-click test runner
├── docker-compose.yml         # PostgreSQL 16 container definition
├── .env.example               # Template environment configuration
└── .gitignore                 # Secrets, cache, and build ignore rules
```

---

## ⚡ Quick Start

### 1. Verify Database Connection
```powershell
.\backend\.venv\Scripts\python.exe scripts\verify_db.py
```

### 2. One-Click Launch
- **Start Backend:** `.\scripts\run_backend.bat` (Server at [http://localhost:8000](http://localhost:8000), Swagger at `/docs`)
- **Start Frontend:** `.\scripts\run_frontend.bat` (Web App at [http://localhost:5173](http://localhost:5173))
- **Run All Tests:** `.\scripts\run_tests.bat` (Runs backend Pytest + frontend Vitest)
