# PlacementPilot — Comprehensive REST API Specification

> **Base URL:** `http://localhost:8000/api/v1`  
> **Interactive Swagger UI:** `http://localhost:8000/docs`  
> **ReDoc Alternative:** `http://localhost:8000/redoc`

---

## 1. Global Standards & Envelope

All JSON responses follow the standardized envelope:
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully"
}
```

---

## 2. API Endpoints Catalog by Module

### 2.1 System & Core Auth (`/api/v1/auth`)
- `GET /api/v1/health` — System status and sanitized database connectivity.
- `POST /api/v1/auth/register` — Register student with Argon2id password hashing and auto-initialized profile.
- `POST /api/v1/auth/login` — Authenticate and receive JWT with campus & role claims (IP rate-limited to 5 attempts / 5-min sliding window).
- `POST /api/v1/auth/logout` — RFC-compliant stateless logout response.
- `GET /api/v1/auth/me` — Current authenticated user profile with academic metadata.
- `PUT /api/v1/auth/me` — Update user profile details (full name, phone, bio, avatar).
- `POST /api/v1/auth/change-password` — Secure password rotation verifying old credentials and enforcing complexity.
- `GET /api/v1/auth/admin-check` — Administrator-only RBAC protected verification route.
- `GET /api/v1/auth/student-private-data/{user_id}` — Resource ownership protected route (only the owner or admin/staff).

### 2.2 Student Profile (`/api/v1/profile`)
- `GET /api/v1/profile` — Academic profile, target roles, skills, and hostel room.
- `PUT /api/v1/profile` — Update academic details and campus preferences.

### 2.3 Placement Preparation Engine
- `GET /api/v1/assessments` — List diagnostic assessments across 6 core subjects.
- `POST /api/v1/assessments/{id}/start` — Begin timed attempt.
- `POST /api/v1/assessments/attempts/{id}/submit` — Submit answers for server-side score calculation.
- `GET /api/v1/assessments/attempts/{id}/results` — Detailed subject and topic score report.
- `POST /api/v1/study-plans/generate` — Generate deterministic study plan from assessment weaknesses.
- `GET /api/v1/study-plans/active` — Active plan with daily task checklist.
- `PATCH /api/v1/study-plans/tasks/{id}/toggle` — Mark task complete/reopen.
- `GET /api/v1/coding/problems` — DSA problems filtered by topic and difficulty.
- `POST /api/v1/resumes/upload` — Upload PDF resume (magic byte validated, 5MB limit).
- `POST /api/v1/interviews/sessions` — Start technical or behavioral mock interview.

---

### 2.4 Feature 1: AI Study Assistant (`/api/v1/study-assistant`)
- `POST /api/v1/study-assistant/notes/upload` — Upload lecture PDF or document (max 15MB, local text extraction).
- `GET /api/v1/study-assistant/notes` — List student's uploaded lecture notes by subject.
- `POST /api/v1/study-assistant/notes/{id}/summarize` — Generate executive or detailed revision summary.
- `GET /api/v1/study-assistant/notes/{id}/flashcards` — Generate or fetch flashcard decks from note content.
- `PATCH /api/v1/study-assistant/flashcards/{id}/review` — Update flashcard mastery level (0-5).
- `POST /api/v1/study-assistant/notes/{id}/generate-mcqs` — Generate practice MCQs based on lecture concepts.
- `POST /api/v1/study-assistant/notes/{id}/ask` — Answer student questions based on the uploaded notes.

---

### 2.5 Feature 2: Universal Opportunity Hub (`/api/v1/opportunities`)
- `GET /api/v1/opportunities` — Search and filter opportunities by category (`internship`, `hackathon`, `competition`, `research`, `scholarship`, `placement_prep`), location, eligibility, and deadline.
- `GET /api/v1/opportunities/{id}` — Full opportunity details with verified eligibility criteria.
- `POST /api/v1/opportunities/{id}/save` — Save opportunity to personal shortlist.
- `GET /api/v1/opportunities/applications` — Fetch user's application pipeline.
- `POST /api/v1/opportunities/{id}/track` — Update status (`Interested`, `Applied`, `Shortlisted`, `Interview`, `Offer`, `Rejected`).

---

### 2.6 Feature 3: Campus Marketplace (`/api/v1/marketplace`)
- `GET /api/v1/marketplace/items` — Browse items scoped to user's campus (`books`, `calculators_lab`, `furniture`, `tutoring`, `services`).
- `POST /api/v1/marketplace/items` — Create a new item listing with condition, price, and contact method.
- `GET /api/v1/marketplace/items/{id}` — Item details and verified student seller contact info.
- `PATCH /api/v1/marketplace/items/{id}/status` — Seller marks item as `available`, `reserved`, or `sold`.
- `DELETE /api/v1/marketplace/items/{id}` — Remove listing.

---

### 2.7 Feature 4: Campus Community (`/api/v1/community`)
- `GET /api/v1/community/clubs` — Discover campus technical and cultural clubs.
- `POST /api/v1/community/clubs/{id}/join` — Request club membership.
- `GET /api/v1/community/posts` — Campus feed for project showcases, ideas, and event announcements.
- `POST /api/v1/community/posts` — Publish project idea or event.
- `GET /api/v1/community/team-requests` — Browse hackathon and project teammate requests.
- `POST /api/v1/community/team-requests` — Post a teammate request specifying required roles.

---

### 2.8 Feature 5: Hostel & Campus Services (`/api/v1/hostel`)
- `POST /api/v1/hostel/tickets` — Report maintenance issue (*e.g., broken water dispenser, electricity fault, WiFi outage*).
- `GET /api/v1/hostel/tickets` — View student's reported tickets and live status (`open`, `acknowledged`, `in_progress`, `resolved`).
- `GET /api/v1/hostel/tickets/{id}` — Detailed ticket audit trail and assigned staff notes.
- `PATCH /api/v1/hostel/tickets/{id}/status` — (Admin / Campus Staff) Update ticket resolution status and add resolution notes.

---

### 2.9 Administrator Console (`/api/v1/admin`)
- `GET /api/v1/admin/stats` — High-level campus metrics across all 5 features and placement tests.
- `POST /api/v1/admin/questions` — Manage assessment question bank.
- `PUT /api/v1/admin/opportunities/{id}/verify` — Verify/approve official opportunities.
- `PATCH /api/v1/admin/marketplace/{id}/moderate` — Deactivate inappropriate marketplace listings.
