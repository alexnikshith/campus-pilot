# PlacementPilot — Comprehensive Master Implementation Plan (All Pillars)

> **Platform:** PlacementPilot — Placement Preparation & Campus Super-App  
> **Status:** Phases 1, 2, 3 & 4 COMPLETED & VERIFIED | 34 Pytest + 2 Vitest Passing  
> **Execution Strategy:** Incremental, verified phases triggered with one-click transitions.

---

## Unified Phase Matrix

| Phase | Title | Scope Summary | Dependencies | Status | One-Click Command |
|---|---|---|---|---|---|
| **Phase 1** | **Environment & Setup** | Python 3.12 venv, Node 20, Vite, React, Tailwind, Alembic, DB verifier, Health endpoint | None | **COMPLETED & VERIFIED** | `scripts/run_tests.bat` |
| **Phase 2** | **Unified Database Design** | SQLAlchemy 2.0 models for all 25 tables, Alembic migration `001`, development seed script | Phase 1 | **COMPLETED & VERIFIED** | `scripts/run_tests.bat` |
| **Phase 3** | **Backend Foundation** | Standardized response envelopes, centralized exception handlers, pagination, repositories | Phase 2 | **COMPLETED & VERIFIED** | `scripts/run_tests.bat` |
| **Phase 4** | **Auth & Campus Scoping** | Argon2id hashing, JWT claims with `campus_name`, RBAC (student/admin/staff), rate limiting, bounds | Phase 2, 3 | **COMPLETED & VERIFIED** | `scripts/run_tests.bat` |
| **Phase 5** | **Frontend Design System** | Modern educational SaaS shell, responsive sidebar, campus theme, modals | Phase 1 | **QUEUED** | Phase 5 Trigger |
| **Phase 6** | **Student Profile & Onboarding** | Degree, branch, graduation year, CGPA, skills, target roles, campus & hostel block | Phase 4, 5 | **QUEUED** | Phase 6 Trigger |
| **Phase 7** | **Readiness Assessment Engine** | 6 subjects, question bank, timed attempts, server-side scoring | Phase 2, 4 | **QUEUED** | Phase 7 Trigger |
| **Phase 8** | **Deterministic Study Plan** | Rule-based algorithm generating weekly roadmap & daily tasks from diagnostic gaps | Phase 6, 7 | **QUEUED** | Phase 8 Trigger |
| **Phase 9** | **Placement Dashboard** | Real-time analytics, subject proficiency radar, daily task toggle | Phase 7, 8 | **QUEUED** | Phase 9 Trigger |
| **Phase 10** | **Coding Practice Module** | Curated DSA problems, in-browser editor, sandboxed test case runner | Phase 3, 5 | **QUEUED** | Phase 10 Trigger |
| **Phase 11** | **Resume Analysis Workflow** | PDF parser, signature check, skill extraction, deterministic ATS rubric | Phase 3, 4 | **QUEUED** | Phase 11 Trigger |
| **Phase 12** | **Mock Interview Simulator** | Role & category selection, structured rubric feedback, offline practice mode | Phase 4, 19 | **QUEUED** | Phase 12 Trigger |
| **Phase 13** | **Feature 1: AI Study Assistant** | Lecture PDF upload, local text extraction, summaries, flashcards, note MCQs | Phase 4, 11 | **QUEUED** | Phase 13 Trigger |
| **Phase 14** | **Feature 2: Opportunity Hub** | Internships, hackathons, coding contests, research, scholarships, app tracker | Phase 4, 5 | **QUEUED** | Phase 14 Trigger |
| **Phase 15** | **Feature 3: Campus Marketplace** | P2P marketplace for books, calculators, lab kits, tutoring; single-campus trust | Phase 4, 5 | **QUEUED** | Phase 15 Trigger |
| **Phase 16** | **Feature 4: Campus Community** | Technical clubs, hackathon teammate matching, project showcases, event feed | Phase 4, 5 | **QUEUED** | Phase 16 Trigger |
| **Phase 17** | **Feature 5: Hostel Services** | Facility grievance tickets (water, electricity, wifi), resolution workflow | Phase 4, 5 | **QUEUED** | Phase 17 Trigger |
| **Phase 18** | **Admin & Staff Console** | Content moderation, opportunity verification, ticket management, metrics | Phase 4, 14, 17 | **QUEUED** | Phase 18 Trigger |
| **Phase 19** | **AI Service & Cost Controls** | Provider abstraction (Gemini/OpenAI/Mock), token budgets, prompt sanitization | Phase 3 | **QUEUED** | Phase 19 Trigger |
| **Phase 20** | **Security & Privacy Hardening** | Rate limiting, campus isolation, data retention & deletion endpoints | All Phases | **QUEUED** | Phase 20 Trigger |
| **Phase 21** | **End-to-End QA Suite** | Complete user workflows across all 5 features + placement engine | All Phases | **QUEUED** | Phase 21 Trigger |
| **Phase 22** | **Production Deployment** | Docker multi-stage build, Nginx reverse proxy, production startup script | All Phases | **QUEUED** | Phase 22 Trigger |

---

## Detailed Phase Execution Logs

### Phase 1: Environment & Setup (COMPLETED)
- Verified Python 3.12, Node v20, npm 10.8, Git 2.55, Docker 29.1.
- Initialized FastAPI backend and React Vite Tailwind frontend.
- Created `scripts/verify_db.py`, `scripts/run_backend.bat`, `scripts/run_frontend.bat`, `scripts/run_tests.bat`.
- Initial tests verified: Pytest (3 passed), Vitest (2 passed).

### Phase 2: Unified Database Design (COMPLETED & VERIFIED)
- **Objective:** Design, implement, test, and migrate the normalized relational schema covering all 25 tables across the placement preparation engine and the 5 campus pillars.
- **Models Implemented:**
  1. `app/models/base.py`: `Base(DeclarativeBase)` and `TimestampMixin` with UTC timezone awareness.
  2. `app/models/user.py`: `User` and `StudentProfile` (Argon2id password hashes, campus scoping, academic fields, and hostel room).
  3. `app/models/assessment.py`: `Question`, `Assessment`, `AssessmentQuestion`, `AssessmentAttempt`, `AssessmentAttemptAnswer` (hidden correct answers, subject indexes, scoring integrity).
  4. `app/models/study_plan.py`: `StudyPlan` and `StudyPlanTask` (deterministic scheduler attributes, status, completion timestamps).
  5. `app/models/resume.py`: `Resume` (file metadata, extracted skills JSON, ATS score, storage UUID).
  6. `app/models/mock_interview.py`: `MockInterview` (category, student answer, accuracy/clarity/completeness scores, feedback rubric).
  7. `app/models/opportunity.py`: `Opportunity`, `SavedOpportunity`, `ApplicationTracking` (categories: internship, hackathon, competition, research, scholarship; status pipeline).
  8. `app/models/study_assistant.py`: `LectureNote`, `NoteSummary`, `FlashcardDeck`, `Flashcard`, `NoteMCQ` (PDF storage, extracted text, adaptive flashcards, grounded MCQs).
  9. `app/models/marketplace.py`: `MarketplaceItem` (books, calculators, lab kits, tutoring; single-campus trust boundary, pricing, condition).
  10. `app/models/community.py`: `CampusClub`, `ClubMembership`, `CommunityPost`, `TeamRequest` (club directory, project showcase, hackathon teammate matchmaking).
  11. `app/models/facility.py`: `FacilityTicket` (maintenance grievances like broken water coolers, room location, urgency, status lifecycle).
  12. `app/models/__init__.py`: Aggregates and exports all 25 entities.
- **Alembic Migration:**
  - `alembic/versions/001_initial_unified_schema.py`: Explicit, pristine migration with tables, primary keys, foreign key constraints with `ON DELETE CASCADE`, unique constraints, and B-tree indexes.
- **Development Seed Script:**
  - `scripts/seed_dev_data.py`: Seeds realistic sample data across all 6 placement subjects and campus pillars.

### Phase 3: Backend Foundation & API Architecture (COMPLETED & VERIFIED)
- **Objective:** Establish production-grade error handling, response envelopes, pagination utilities, request tracing, and generic repository/service patterns.
- **Components Built:**
  1. `app/schemas/common.py`: Standardized envelopes `ResponseEnvelope[T]`, `ErrorDetail`, `ErrorEnvelope`, `PaginationParams` (page, page_size, sort_by, order, offset), and `PaginatedResponse[T]` (items, total, total_pages, has_next, has_prev).
  2. `app/core/exceptions.py`: Comprehensive domain exception hierarchy (`AppException`, `EntityNotFoundException`, `BadRequestException`, `UnauthorizedException`, `ForbiddenException`, `ConflictException`, `ValidationException`, `RateLimitException`, `DatabaseException`).
  3. `app/core/error_handlers.py`: Centralized exception handlers for FastAPI catching `AppException`, Pydantic `RequestValidationError`, `StarletteHTTPException`, `SQLAlchemyError`, and uncaught server errors without leaking credentials.
  4. `app/middleware/request_context.py`: `RequestIDAndTimingMiddleware` attaching unique `X-Request-ID` and `X-Process-Time-Ms` headers and logging request latency.
  5. `app/repositories/base.py`: Type-safe generic `BaseRepository[ModelType, CreateSchemaType, UpdateSchemaType]` providing standardized CRUD and pagination operations (`get`, `get_or_404`, `get_multi`, `create`, `update`, `delete`, `count`).
  6. `app/services/base.py`: Generic `BaseService` encapsulating business rules and orchestrating repository queries.
  7. `app/api/v1/routes/system.py`: Foundation demonstration endpoints for query validation, custom exception triggering, and pagination navigation.
  8. `backend/tests/test_foundation.py`: 7 comprehensive tests verifying response envelopes, validation error details, domain exception catching, pagination navigation math, telemetry headers, and repository/service CRUD operations.
- **Test Summary:**
  - Pytest: **18/18 passed** in 0.47s.
  - Vitest: **2/2 passed** in 200ms.
  - Combined `scripts/run_tests.bat`: **PASSED with exit code 0**.

### Phase 4: Authentication & Authorization (COMPLETED & VERIFIED)
- **Objective:** Build enterprise-grade security infrastructure with modern Argon2id password hashing, JWT authentication enriched with campus scoping and role claims, granular RBAC dependencies, IP-aware sliding-window rate limiting on sensitive auth endpoints, and student resource ownership boundary enforcement.
- **Components Built:**
  1. `app/core/security.py`:
     - **Argon2id Hashing:** Password hashing configured with RFC 9106 Argon2id parameters via `passlib.hash.argon2.using(type="ID")`. Zero MD5/SHA1/plain bcrypt legacy.
     - **Password Strength Rules:** Strict validation enforcing minimum 8 characters, uppercase, lowercase, numbers, and special symbols.
     - **JWT Tokens:** HS256 JWT encoding and decoding carrying `sub` (User ID), `role`, `campus_name`, `email`, `iat`, and `exp` claims.
  2. `app/core/rate_limiter.py`:
     - Thread-safe sliding-window in-memory rate limiter `InMemoryRateLimiter` with automatic expiration cleanup.
     - Applied to `/login` endpoint (5 attempts per 5-minute sliding window per client IP) returning HTTP 429 `RateLimitException` with `Retry-After` header.
  3. `app/schemas/auth.py`:
     - Strongly typed Pydantic V2 schemas: `UserRegisterRequest`, `UserLoginRequest`, `UserResponse`, `StudentProfileBrief`, `CurrentUserResponse`, `TokenResponse`, `UserUpdateRequest`, `PasswordChangeRequest`.
     - Zero credential leakage: `hashed_password` is never included in any API response model.
  4. `app/repositories/user.py`:
     - `UserRepository` extending `BaseRepository[User, UserRegisterRequest, UserUpdateRequest]`.
     - Atomic creation of `User` and connected `StudentProfile` with department, academic year, campus, and default CGPA.
     - Case-insensitive email indexing and lookup methods (`get_by_email`).
  5. `app/services/auth_service.py`:
     - Domain logic orchestration: prevents self-assignment of `admin` role during public registration, verifies active account status, verifies current password prior to rotation, and generates signed tokens.
  6. `app/api/deps.py`:
     - `get_current_user`: OAuth2 Bearer token extractor, decoder, and user retrieval dependency.
     - `get_current_active_user`: Enforces user active status.
     - `require_role(*allowed_roles)`: Factory dependency producing reusable RBAC guards (e.g. `require_role(UserRole.ADMIN)`).
     - `verify_resource_ownership(resource_user_id, current_user)`: Guarantees students can only read/write their own data while allowing staff/admin oversight.
     - `get_client_ip`: Client IP extractor honoring reverse proxy forwarding headers (`X-Forwarded-For`).
  7. `app/api/v1/routes/auth.py`:
     - `POST /api/v1/auth/register`: Public student registration with Argon2id hashing.
     - `POST /api/v1/auth/login`: IP rate-limited authentication returning scoped JWT bearer token.
     - `POST /api/v1/auth/logout`: RFC-compliant stateless logout response with cache-clearing instructions.
     - `GET /api/v1/auth/me`: Authenticated profile retrieval with student academic metadata.
     - `PUT /api/v1/auth/me`: Profile updates (full name, phone number, bio, avatar URL).
     - `POST /api/v1/auth/change-password`: Secure password rotation verifying old credentials and password complexity.
     - `GET /api/v1/auth/admin-check`: Protected RBAC route restricted strictly to admins.
     - `GET /api/v1/auth/student-private-data/{user_id}`: Protected ownership-guarded route.
  8. `backend/tests/test_auth.py`:
     - 16 comprehensive integration test cases covering successful registration, duplicate email rejection, weak password rejection, admin privilege self-assignment prevention, login success, invalid credentials rejection, inactive user block, profile retrieval & updates, token tampering/expiration, password rotation verification, RBAC role guard enforcement, student ownership boundary enforcement, and sliding-window rate limit triggers.
- **Test Summary:**
  - Pytest Backend: **34/34 passed** (100% pass rate in 8.35s).
  - Vitest Frontend: **2/2 passed** (100% pass rate).
  - Frontend Build: **TypeScript + Vite bundled in 6.08s with 0 errors**.
