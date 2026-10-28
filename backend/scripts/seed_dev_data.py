#!/usr/bin/env python3
"""
PlacementPilot & Campus Super-App — Comprehensive Development Seed Script
Seeds sample data for local testing across all 5 campus pillars and the placement engine.
All sample records are explicitly labeled and do not represent live production data.
"""

import sys
import os
from datetime import datetime, timezone, timedelta, date
from decimal import Decimal

# Ensure backend root is on sys.path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from passlib.hash import argon2
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine, Base
import app.models as models

def seed_database():
    print("=" * 70)
    print(" PlacementPilot & Campus Super-App: Seeding Development Data")
    print("=" * 70)

    # Ensure tables exist (creates them if not present)
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # Check if already seeded
        existing_user = db.query(models.User).filter_by(email="student@placementpilot.local").first()
        if existing_user:
            print("[INFO] Database already contains seed data. Skipping seed to prevent duplication.")
            return

        print("[1/10] Seeding Users & Credentials (Argon2id hashing)...")
        now = datetime.now(timezone.utc)
        student_pw_hash = argon2.using(type="ID").hash("StudentSecurePass2026!")
        admin_pw_hash = argon2.using(type="ID").hash("AdminSecurePass2026!")
        staff_pw_hash = argon2.using(type="ID").hash("StaffSecurePass2026!")

        student_user = models.User(
            email="student@placementpilot.local",
            full_name="Aarav Sharma",
            password_hash=student_pw_hash,
            role="student",
            campus_name="National Institute of Engineering (NIE)",
            is_active=True,
            created_at=now,
            updated_at=now
        )
        admin_user = models.User(
            email="admin@placementpilot.local",
            full_name="Dr. Sunita Rao (Placement Dean)",
            password_hash=admin_pw_hash,
            role="admin",
            campus_name="National Institute of Engineering (NIE)",
            is_active=True,
            created_at=now,
            updated_at=now
        )
        staff_user = models.User(
            email="facilities@placementpilot.local",
            full_name="Rajesh Kumar (Campus Works)",
            password_hash=staff_pw_hash,
            role="campus_staff",
            campus_name="National Institute of Engineering (NIE)",
            is_active=True,
            created_at=now,
            updated_at=now
        )
        db.add_all([student_user, admin_user, staff_user])
        db.flush()

        print("[2/10] Seeding Student Profile...")
        profile = models.StudentProfile(
            user_id=student_user.id,
            degree="B.Tech",
            branch="Computer Science and Engineering",
            graduation_year=2026,
            cgpa=Decimal("8.85"),
            skills=["Python", "FastAPI", "React", "TypeScript", "SQL", "Data Structures", "Docker"],
            target_roles=["Software Development Engineer (SDE-1)", "Full Stack Developer"],
            preferred_locations=["Bangalore", "Hyderabad", "Remote"],
            prep_hours_week=20,
            hostel_block="Aryabhata Boys Hostel, Block B",
            room_number="B-304"
        )
        db.add(profile)

        print("[3/10] Seeding Placement Readiness Questions (6 Subjects)...")
        questions_data = [
            # 1. DSA
            {
                "subject": "Data Structures & Algorithms",
                "topic": "Binary Search Trees",
                "difficulty": "medium",
                "question_text": "What is the worst-case time complexity of searching for an element in an unbalanced Binary Search Tree (BST) with n nodes?",
                "options": [
                    {"id": "A", "text": "O(1)"},
                    {"id": "B", "text": "O(log n)"},
                    {"id": "C", "text": "O(n)"},
                    {"id": "D", "text": "O(n log n)"}
                ],
                "correct_option": "C",
                "explanation": "In an unbalanced BST, elements can be inserted in strictly sorted order, degenerating the tree into a linked list structure of height n. Consequently, worst-case search traversal is O(n)."
            },
            # 2. Programming Fundamentals
            {
                "subject": "Programming Fundamentals",
                "topic": "Memory Management & Pointers",
                "difficulty": "medium",
                "question_text": "Which of the following conditions leads to a 'dangling pointer' in C/C++?",
                "options": [
                    {"id": "A", "text": "A pointer assigned to NULL"},
                    {"id": "B", "text": "A pointer pointing to a deallocated memory block"},
                    {"id": "C", "text": "A pointer that has not been initialized"},
                    {"id": "D", "text": "A pointer holding a constant memory address"}
                ],
                "correct_option": "B",
                "explanation": "A dangling pointer arises when memory pointed to by the pointer is freed or deallocated, while the pointer variable still retains the old address."
            },
            # 3. DBMS
            {
                "subject": "DBMS",
                "topic": "Normalization & Keys",
                "difficulty": "medium",
                "question_text": "A relation is in Boyce-Codd Normal Form (BCNF) if and only if for every non-trivial functional dependency X -> Y:",
                "options": [
                    {"id": "A", "text": "Y is a prime attribute"},
                    {"id": "B", "text": "X is a super key"},
                    {"id": "C", "text": "X is a candidate key and Y is prime"},
                    {"id": "D", "text": "No multi-valued dependencies exist"}
                ],
                "correct_option": "B",
                "explanation": "BCNF requires that for every non-trivial functional dependency X -> Y, the determinant X must be a super key in the relation."
            },
            # 4. Operating Systems
            {
                "subject": "Operating Systems",
                "topic": "Deadlock & Concurrency",
                "difficulty": "hard",
                "question_text": "Which of the following is NOT one of the four necessary Coffman conditions for a deadlock to occur?",
                "options": [
                    {"id": "A", "text": "Mutual Exclusion"},
                    {"id": "B", "text": "Hold and Wait"},
                    {"id": "C", "text": "Preemption allowed"},
                    {"id": "D", "text": "Circular Wait"}
                ],
                "correct_option": "C",
                "explanation": "The condition is 'No Preemption' (resources cannot be forcibly taken from a process). If preemption is allowed, deadlocks can be broken or prevented."
            },
            # 5. Computer Networks
            {
                "subject": "Computer Networks",
                "topic": "TCP/IP & Transport Layer",
                "difficulty": "easy",
                "question_text": "What is the primary role of the SYN flag during the standard TCP three-way handshake?",
                "options": [
                    {"id": "A", "text": "To request graceful connection termination"},
                    {"id": "B", "text": "To synchronize sequence numbers between client and server"},
                    {"id": "C", "text": "To acknowledge packet receipt without payload"},
                    {"id": "D", "text": "To reset an invalid connection session"}
                ],
                "correct_option": "B",
                "explanation": "The SYN (Synchronize) packet initiates connection establishment and allows endpoints to agree upon and synchronize Initial Sequence Numbers (ISNs)."
            },
            # 6. Aptitude
            {
                "subject": "Aptitude",
                "topic": "Time and Work",
                "difficulty": "medium",
                "question_text": "Person A can complete a project in 12 days, and Person B can complete the same project in 24 days. How many days will it take if they work together?",
                "options": [
                    {"id": "A", "text": "6 days"},
                    {"id": "B", "text": "8 days"},
                    {"id": "C", "text": "10 days"},
                    {"id": "D", "text": "16 days"}
                ],
                "correct_option": "B",
                "explanation": "Rate of A = 1/12 per day. Rate of B = 1/24 per day. Combined rate = 1/12 + 1/24 = 3/24 = 1/8. Total time = 8 days."
            }
        ]

        question_objs = []
        for qd in questions_data:
            q = models.Question(
                subject=qd["subject"],
                topic=qd["topic"],
                difficulty=qd["difficulty"],
                question_text=qd["question_text"],
                question_type="mcq",
                options=qd["options"],
                correct_option=qd["correct_option"],
                explanation=qd["explanation"],
                marks=1,
                is_active=True,
                created_at=now
            )
            db.add(q)
            question_objs.append(q)
        db.flush()

        print("[4/10] Seeding Comprehensive Diagnostic Assessment...")
        diag_assessment = models.Assessment(
            title="Comprehensive Technical Placement Readiness Diagnostic (2026)",
            description="Diagnostic placement evaluation covering DSA, Programming Fundamentals, DBMS, Operating Systems, Networks, and Aptitude.",
            assessment_type="diagnostic",
            duration_minutes=45,
            pass_percentage=Decimal("60.00"),
            is_active=True,
            created_at=now
        )
        db.add(diag_assessment)
        db.flush()

        for idx, q in enumerate(question_objs):
            aq = models.AssessmentQuestion(
                assessment_id=diag_assessment.id,
                question_id=q.id,
                order_index=idx + 1,
                marks=1
            )
            db.add(aq)
        db.flush()

        # Seed sample completed attempt for Aarav
        attempt = models.AssessmentAttempt(
            user_id=student_user.id,
            assessment_id=diag_assessment.id,
            started_at=now - timedelta(hours=2),
            submitted_at=now - timedelta(hours=1, minutes=15),
            total_score=Decimal("5.00"),
            maximum_score=Decimal("6.00"),
            percentage=Decimal("83.33"),
            status="completed",
            subject_breakdown={
                "Data Structures & Algorithms": {"score": 1, "max": 1, "percentage": 100},
                "Programming Fundamentals": {"score": 1, "max": 1, "percentage": 100},
                "DBMS": {"score": 1, "max": 1, "percentage": 100},
                "Operating Systems": {"score": 0, "max": 1, "percentage": 0},
                "Computer Networks": {"score": 1, "max": 1, "percentage": 100},
                "Aptitude": {"score": 1, "max": 1, "percentage": 100}
            }
        )
        db.add(attempt)
        db.flush()

        # Answers for attempt
        for q in question_objs:
            is_correct = (q.subject != "Operating Systems")
            selected = q.correct_option if is_correct else "A"
            ans = models.AssessmentAttemptAnswer(
                attempt_id=attempt.id,
                question_id=q.id,
                selected_option=selected,
                is_correct=is_correct,
                marks_awarded=Decimal("1.00") if is_correct else Decimal("0.00")
            )
            db.add(ans)

        print("[5/10] Seeding Deterministic Study Plan & Daily Tasks...")
        study_plan = models.StudyPlan(
            user_id=student_user.id,
            target_role="Software Development Engineer (SDE-1)",
            title="Operating Systems & Concurrency Mastery Plan",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=14),
            status="active",
            total_tasks=3,
            completed_tasks=1,
            recommendation_rules={
                "trigger": "Diagnostic score in Operating Systems was 0%",
                "weak_topic": "Deadlock & Concurrency",
                "recommended_weekly_hours": 15
            }
        )
        db.add(study_plan)
        db.flush()

        task1 = models.StudyPlanTask(
            study_plan_id=study_plan.id,
            title="Review Process Synchronization & Mutex Primitives",
            description="Deep dive into critical section problems, Peterson's algorithm, and semaphores.",
            subject="Operating Systems",
            topic="Process Synchronization",
            scheduled_date=date.today(),
            estimated_minutes=45,
            status="completed",
            completed_at=now
        )
        task2 = models.StudyPlanTask(
            study_plan_id=study_plan.id,
            title="Study Deadlock Avoidance & Banker's Algorithm",
            description="Understand resource allocation graphs and safe sequence determination.",
            subject="Operating Systems",
            topic="Deadlock Avoidance",
            scheduled_date=date.today() + timedelta(days=1),
            estimated_minutes=60,
            status="pending"
        )
        task3 = models.StudyPlanTask(
            study_plan_id=study_plan.id,
            title="Practice Operating Systems MCQ Diagnostic Drill",
            description="Complete 15 timed questions on virtual memory and paging.",
            subject="Operating Systems",
            topic="Virtual Memory",
            scheduled_date=date.today() + timedelta(days=2),
            estimated_minutes=30,
            status="pending"
        )
        db.add_all([task1, task2, task3])

        print("[6/10] Seeding Resume & Mock Interview records...")
        sample_resume = models.Resume(
            user_id=student_user.id,
            original_filename="Aarav_Sharma_Resume.pdf",
            storage_filename="seed_resume_aarav_sharma.pdf",
            file_size_bytes=142850,
            mime_type="application/pdf",
            extracted_text="Aarav Sharma | B.Tech CSE | Skills: Python, FastAPI, React, SQL, Algorithms...",
            extracted_skills=["Python", "FastAPI", "React", "SQL", "Git", "Docker", "Algorithms"],
            ats_score=Decimal("87.50"),
            analysis_json={
                "strengths": ["Quantified project achievements", "Clear technical stack listing"],
                "improvements": ["Add direct links to live GitHub repositories", "Include deployment metrics"],
                "format_check": "Clean single-column layout conforming to standard ATS parsing."
            }
        )
        db.add(sample_resume)

        sample_interview = models.MockInterview(
            user_id=student_user.id,
            role="Software Engineer",
            category="Technical Fundamentals",
            question_text="Explain the difference between optimistic and pessimistic locking in database transaction management.",
            student_answer="Optimistic locking assumes conflicts rarely happen, verifying version counters at commit time. Pessimistic locking acquires record locks immediately upon read to prevent concurrent changes.",
            technical_accuracy_score=Decimal("9.00"),
            clarity_score=Decimal("8.50"),
            completeness_score=Decimal("8.50"),
            overall_score=Decimal("8.67"),
            is_ai_evaluated=False,
            evaluation_rubric={
                "criteria": ["Accuracy", "Clarity", "Real-world trade-off mention"],
                "feedback": "Strong concise answer. Mentioning transaction rollback costs under high write contention would make it exceptional."
            }
        )
        db.add(sample_interview)

        print("[7/10] Seeding AI Study Assistant (Lecture Notes, Flashcards, MCQs)...")
        sample_note = models.LectureNote(
            user_id=student_user.id,
            title="Database Systems - Lecture 6: BCNF and Functional Dependencies",
            subject="DBMS",
            original_filename="DBMS_Lecture6_BCNF.pdf",
            storage_filename="seed_note_dbms_bcnf.pdf",
            file_size_bytes=385200,
            extracted_text="Relational Database Design Theory. Functional dependencies X -> Y. A relation R is in BCNF if for every non-trivial functional dependency X -> Y, X is a superkey of R. Lossless-join decomposition is always achievable in BCNF, but dependency preservation is not guaranteed.",
            page_count=12
        )
        db.add(sample_note)
        db.flush()

        note_summary = models.NoteSummary(
            note_id=sample_note.id,
            summary_type="key_takeaways",
            summary_content="1. Functional Dependency: X uniquely determines Y.\n2. BCNF Criterion: Every determinant must be a superkey.\n3. Trade-off: BCNF eliminates all redundancy due to functional dependencies, but may sacrifice dependency preservation.",
            is_ai_generated=False
        )
        db.add(note_summary)

        deck = models.FlashcardDeck(
            note_id=sample_note.id,
            user_id=student_user.id,
            title="BCNF & Normalization Flashcard Deck",
            card_count=2
        )
        db.add(deck)
        db.flush()

        fc1 = models.Flashcard(
            deck_id=deck.id,
            front_prompt="What is the strict mathematical definition of BCNF?",
            back_solution="For every non-trivial functional dependency X -> Y in relation R, X must be a superkey of R.",
            mastery_level=4,
            last_reviewed_at=now
        )
        fc2 = models.Flashcard(
            deck_id=deck.id,
            front_prompt="Can every relation be decomposed into BCNF while preserving all dependencies?",
            back_solution="No. BCNF guarantees lossless-join decomposition, but dependency preservation is not always achievable (unlike 3NF).",
            mastery_level=3,
            last_reviewed_at=now
        )
        db.add_all([fc1, fc2])

        note_mcq = models.NoteMCQ(
            note_id=sample_note.id,
            question_text="Which of the following is guaranteed when decomposing a schema into 3NF, but NOT always guaranteed in BCNF?",
            options=[
                {"id": "A", "text": "Lossless-join property"},
                {"id": "B", "text": "Dependency preservation"},
                {"id": "C", "text": "Elimination of all update anomalies"},
                {"id": "D", "text": "Minimal key constraint"}
            ],
            correct_option="B",
            explanation="3NF synthesis always guarantees both lossless-join and dependency preservation. BCNF guarantees lossless-join, but dependency preservation cannot always be satisfied."
        )
        db.add(note_mcq)

        print("[8/10] Seeding Opportunity Hub (Internships, Hackathons, Contests)...")
        opps = [
            models.Opportunity(
                category="internship",
                company_name="[SAMPLE DATA] CloudScale Technologies",
                job_title="Backend Engineering Intern (Summer 2026)",
                description="Sample opportunity: Work on distributed event-driven microservices using Python and PostgreSQL.",
                required_skills=["Python", "FastAPI", "SQL", "Git"],
                eligibility_criteria="Pre-final year B.Tech students (Class of 2026). Minimum CGPA 7.5.",
                graduation_years=[2026],
                minimum_cgpa=Decimal("7.50"),
                location="Bangalore (Hybrid)",
                prize_or_stipend="₹45,000 / month",
                application_url="https://example.com/careers/sample-internship",
                deadline=now + timedelta(days=30),
                source="Campus Placement Cell Verified",
                verification_status="verified"
            ),
            models.Opportunity(
                category="hackathon",
                company_name="[SAMPLE DATA] National Open Innovation Hub",
                job_title="Smart Campus Hackathon 2026",
                description="Sample hackathon: 36-hour nationwide hackathon building IoT and web solutions for campus sustainability.",
                required_skills=["Web Development", "AI/ML", "IoT", "Problem Solving"],
                eligibility_criteria="All undergraduate engineering students across accredited universities.",
                graduation_years=[2025, 2026, 2027, 2028],
                minimum_cgpa=Decimal("6.00"),
                location="National Institute of Engineering Campus / Hybrid",
                prize_or_stipend="₹2,50,000 Cash Prize Pool",
                application_url="https://example.com/hackathons/smart-campus-2026",
                deadline=now + timedelta(days=20),
                source="Student Technical Council",
                verification_status="verified"
            ),
            models.Opportunity(
                category="competition",
                company_name="[SAMPLE DATA] Algorithmic Arena",
                job_title="Annual Inter-College Algorithmic Challenge",
                description="Sample contest: Speed coding challenge testing dynamic programming and graph theory.",
                required_skills=["C++", "Java", "Python", "Algorithms"],
                eligibility_criteria="Open to all active B.Tech/B.E. students.",
                graduation_years=[2025, 2026, 2027],
                minimum_cgpa=None,
                location="Online",
                prize_or_stipend="Top performers receive fast-track interview passes",
                application_url="https://example.com/contests/algo-arena-2026",
                deadline=now + timedelta(days=15),
                source="Coding Club Registry",
                verification_status="verified"
            )
        ]
        db.add_all(opps)
        db.flush()

        # Save and track first opportunity for Aarav
        saved_opp = models.SavedOpportunity(
            user_id=student_user.id,
            opportunity_id=opps[0].id,
            saved_at=now
        )
        app_track = models.ApplicationTracking(
            user_id=student_user.id,
            opportunity_id=opps[0].id,
            status="Applied",
            applied_date=now - timedelta(days=3),
            notes="Submitted custom resume highlighting FastAPI & PostgreSQL project."
        )
        db.add_all([saved_opp, app_track])

        print("[9/10] Seeding Campus Marketplace, Clubs & Community...")
        item1 = models.MarketplaceItem(
            seller_id=student_user.id,
            campus_name="National Institute of Engineering (NIE)",
            title="[SAMPLE] Casio fx-991EX ClassWiz Scientific Calculator",
            category="calculators_lab",
            description="Used for 2 semesters, perfect working condition with protective cover and solar cell intact.",
            price=Decimal("850.00"),
            condition="like_new",
            contact_method="hostel_room",
            contact_details="Room B-304, Aryabhata Hostel",
            images_json=["https://images.unsplash.com/photo-1594980596870-8aa52a78d8cd?w=400"],
            status="available"
        )
        item2 = models.MarketplaceItem(
            seller_id=student_user.id,
            campus_name="National Institute of Engineering (NIE)",
            title="[SAMPLE] Operating System Concepts (Silberschatz) 10th Ed.",
            category="books",
            description="Paperback textbook, no highlights, essential for 5th semester OS course.",
            price=Decimal("450.00"),
            condition="used_good",
            contact_method="campus_email",
            contact_details="aarav.sharma@nie.edu.local",
            images_json=["https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400"],
            status="available"
        )
        db.add_all([item1, item2])

        club = models.CampusClub(
            lead_user_id=student_user.id,
            campus_name="National Institute of Engineering (NIE)",
            name="NIE Open Source & Developers Club (NODC)",
            category="coding",
            description="Official student chapter dedicated to open-source contributions, technical workshops, and hackathons.",
            logo_url="https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=200",
            is_official=True
        )
        db.add(club)
        db.flush()

        membership = models.ClubMembership(
            club_id=club.id,
            user_id=student_user.id,
            role="lead"
        )
        db.add(membership)

        team_req = models.TeamRequest(
            creator_id=student_user.id,
            campus_name="National Institute of Engineering (NIE)",
            event_or_project_name="Smart Campus Hackathon 2026",
            roles_needed=["UI/UX Designer (Figma)", "ML Engineer (Computer Vision)"],
            description="Building an automated campus energy auditing system. Looking for enthusiastic 2nd/3rd year teammates.",
            status="open"
        )
        db.add(team_req)

        comm_post = models.CommunityPost(
            author_id=student_user.id,
            campus_name="National Institute of Engineering (NIE)",
            post_type="project_showcase",
            title="PlacementPilot Open Source Preparation Platform Initialized",
            content="Excited to announce the initialization of PlacementPilot on campus! An AI-powered placement platform with local study roadmaps and verified opportunity feeds.",
            tags=["OpenSource", "FastAPI", "React", "CampusPlacements"]
        )
        db.add(comm_post)

        print("[10/10] Seeding Hostel & Campus Services (Facility Tickets)...")
        ticket = models.FacilityTicket(
            reporter_id=student_user.id,
            campus_name="National Institute of Engineering (NIE)",
            facility_area="hostel",
            block_or_building="Aryabhata Boys Hostel, Block B",
            room_or_location="2nd Floor Water Cooler Area",
            issue_category="water",
            title="[SAMPLE] Water cooler cooling compressor malfunctioning",
            description="The water cooler is dispensing water at room temperature. Compressor fan appears stopped.",
            urgency="medium",
            status="in_progress",
            assigned_staff="Rajesh Kumar (Campus Works)",
            resolution_notes="Technician dispatched to inspect compressor fuse and thermostat."
        )
        db.add(ticket)

        db.commit()
        print("\n" + "=" * 70)
        print("[SUCCESS] All sample development data seeded cleanly!")
        print(f"  • Users created: 3 (Student, Admin, Staff)")
        print(f"  • Questions seeded: {len(questions_data)} across 6 placement subjects")
        print(f"  • Assessments & Attempts: 1 Diagnostic with 6 questions & score audit")
        print(f"  • Study Plan: 1 Plan with 3 daily scheduled tasks")
        print(f"  • Study Assistant: 1 Lecture Note with summaries, 2 flashcards, 1 MCQ")
        print(f"  • Opportunities: 3 categorized listings with application pipeline")
        print(f"  • Marketplace: 2 items with campus trust scoping")
        print(f"  • Community: 1 Club, 1 Team Request, 1 Showcase Post")
        print(f"  • Facility Services: 1 active maintenance grievance ticket")
        print("=" * 70)

    except Exception as exc:
        db.rollback()
        print(f"\n[ERROR] Seeding failed: {exc}")
        raise exc
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
