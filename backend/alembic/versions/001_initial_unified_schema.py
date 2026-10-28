"""initial_unified_schema

Revision ID: 001_initial_unified_schema
Revises: 
Create Date: 2026-10-28 22:55:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001_initial_unified_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=150), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=30), nullable=False, server_default='student'),
        sa.Column('campus_name', sa.String(length=120), nullable=False, server_default='Main Campus'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_campus_name'), 'users', ['campus_name'], unique=False)

    # 2. student_profiles
    op.create_table(
        'student_profiles',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('degree', sa.String(length=100), nullable=False),
        sa.Column('branch', sa.String(length=100), nullable=False),
        sa.Column('graduation_year', sa.Integer(), nullable=False),
        sa.Column('cgpa', sa.Numeric(precision=4, scale=2), nullable=True),
        sa.Column('skills', sa.JSON(), nullable=False),
        sa.Column('target_roles', sa.JSON(), nullable=False),
        sa.Column('preferred_locations', sa.JSON(), nullable=True),
        sa.Column('prep_hours_week', sa.Integer(), nullable=False, server_default='15'),
        sa.Column('hostel_block', sa.String(length=100), nullable=True),
        sa.Column('room_number', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_student_profiles_id'), 'student_profiles', ['id'], unique=False)
    op.create_index(op.f('ix_student_profiles_user_id'), 'student_profiles', ['user_id'], unique=True)
    op.create_index(op.f('ix_student_profiles_graduation_year'), 'student_profiles', ['graduation_year'], unique=False)

    # 3. questions
    op.create_table(
        'questions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('subject', sa.String(length=80), nullable=False),
        sa.Column('topic', sa.String(length=120), nullable=False),
        sa.Column('difficulty', sa.String(length=20), nullable=False, server_default='medium'),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('question_type', sa.String(length=30), nullable=False, server_default='mcq'),
        sa.Column('options', sa.JSON(), nullable=False),
        sa.Column('correct_option', sa.String(length=10), nullable=False),
        sa.Column('explanation', sa.Text(), nullable=False),
        sa.Column('marks', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_questions_id'), 'questions', ['id'], unique=False)
    op.create_index(op.f('ix_questions_subject'), 'questions', ['subject'], unique=False)
    op.create_index(op.f('ix_questions_topic'), 'questions', ['topic'], unique=False)

    # 4. assessments
    op.create_table(
        'assessments',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('assessment_type', sa.String(length=50), nullable=False, server_default='diagnostic'),
        sa.Column('duration_minutes', sa.Integer(), nullable=False, server_default='60'),
        sa.Column('pass_percentage', sa.Numeric(precision=5, scale=2), nullable=False, server_default='50.00'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assessments_id'), 'assessments', ['id'], unique=False)

    # 5. assessment_questions
    op.create_table(
        'assessment_questions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('assessment_id', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('order_index', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('marks', sa.Integer(), nullable=False, server_default='1'),
        sa.ForeignKeyConstraint(['assessment_id'], ['assessments.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assessment_questions_id'), 'assessment_questions', ['id'], unique=False)
    op.create_index(op.f('ix_assessment_questions_assessment_id'), 'assessment_questions', ['assessment_id'], unique=False)
    op.create_index(op.f('ix_assessment_questions_question_id'), 'assessment_questions', ['question_id'], unique=False)

    # 6. assessment_attempts
    op.create_table(
        'assessment_attempts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('assessment_id', sa.Integer(), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('total_score', sa.Numeric(precision=5, scale=2), nullable=False, server_default='0.00'),
        sa.Column('maximum_score', sa.Numeric(precision=5, scale=2), nullable=False, server_default='0.00'),
        sa.Column('percentage', sa.Numeric(precision=5, scale=2), nullable=False, server_default='0.00'),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='in_progress'),
        sa.Column('subject_breakdown', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['assessment_id'], ['assessments.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assessment_attempts_id'), 'assessment_attempts', ['id'], unique=False)
    op.create_index(op.f('ix_assessment_attempts_user_id'), 'assessment_attempts', ['user_id'], unique=False)
    op.create_index(op.f('ix_assessment_attempts_assessment_id'), 'assessment_attempts', ['assessment_id'], unique=False)

    # 7. assessment_attempt_answers
    op.create_table(
        'assessment_attempt_answers',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('attempt_id', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('selected_option', sa.String(length=10), nullable=True),
        sa.Column('is_correct', sa.Boolean(), nullable=True),
        sa.Column('marks_awarded', sa.Numeric(precision=5, scale=2), nullable=False, server_default='0.00'),
        sa.ForeignKeyConstraint(['attempt_id'], ['assessment_attempts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assessment_attempt_answers_id'), 'assessment_attempt_answers', ['id'], unique=False)
    op.create_index(op.f('ix_assessment_attempt_answers_attempt_id'), 'assessment_attempt_answers', ['attempt_id'], unique=False)
    op.create_index(op.f('ix_assessment_attempt_answers_question_id'), 'assessment_attempt_answers', ['question_id'], unique=False)

    # 8. study_plans
    op.create_table(
        'study_plans',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('target_role', sa.String(length=120), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='active'),
        sa.Column('total_tasks', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('completed_tasks', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('recommendation_rules', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_study_plans_id'), 'study_plans', ['id'], unique=False)
    op.create_index(op.f('ix_study_plans_user_id'), 'study_plans', ['user_id'], unique=False)

    # 9. study_plan_tasks
    op.create_table(
        'study_plan_tasks',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('study_plan_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('subject', sa.String(length=80), nullable=False),
        sa.Column('topic', sa.String(length=120), nullable=False),
        sa.Column('scheduled_date', sa.Date(), nullable=False),
        sa.Column('estimated_minutes', sa.Integer(), nullable=False, server_default='45'),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='pending'),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['study_plan_id'], ['study_plans.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_study_plan_tasks_id'), 'study_plan_tasks', ['id'], unique=False)
    op.create_index(op.f('ix_study_plan_tasks_study_plan_id'), 'study_plan_tasks', ['study_plan_id'], unique=False)
    op.create_index(op.f('ix_study_plan_tasks_subject'), 'study_plan_tasks', ['subject'], unique=False)
    op.create_index(op.f('ix_study_plan_tasks_topic'), 'study_plan_tasks', ['topic'], unique=False)
    op.create_index(op.f('ix_study_plan_tasks_scheduled_date'), 'study_plan_tasks', ['scheduled_date'], unique=False)
    op.create_index(op.f('ix_study_plan_tasks_status'), 'study_plan_tasks', ['status'], unique=False)

    # 10. resumes
    op.create_table(
        'resumes',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('original_filename', sa.String(length=255), nullable=False),
        sa.Column('storage_filename', sa.String(length=255), nullable=False),
        sa.Column('file_size_bytes', sa.Integer(), nullable=False),
        sa.Column('mime_type', sa.String(length=80), nullable=False, server_default='application/pdf'),
        sa.Column('extracted_text', sa.Text(), nullable=True),
        sa.Column('extracted_skills', sa.JSON(), nullable=False),
        sa.Column('ats_score', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('analysis_json', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('storage_filename')
    )
    op.create_index(op.f('ix_resumes_id'), 'resumes', ['id'], unique=False)
    op.create_index(op.f('ix_resumes_user_id'), 'resumes', ['user_id'], unique=False)

    # 11. mock_interviews
    op.create_table(
        'mock_interviews',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(length=120), nullable=False),
        sa.Column('category', sa.String(length=80), nullable=False),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('student_answer', sa.Text(), nullable=False),
        sa.Column('technical_accuracy_score', sa.Numeric(precision=4, scale=2), nullable=True),
        sa.Column('clarity_score', sa.Numeric(precision=4, scale=2), nullable=True),
        sa.Column('completeness_score', sa.Numeric(precision=4, scale=2), nullable=True),
        sa.Column('overall_score', sa.Numeric(precision=4, scale=2), nullable=True),
        sa.Column('evaluation_rubric', sa.JSON(), nullable=True),
        sa.Column('feedback_json', sa.JSON(), nullable=True),
        sa.Column('is_ai_evaluated', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mock_interviews_id'), 'mock_interviews', ['id'], unique=False)
    op.create_index(op.f('ix_mock_interviews_user_id'), 'mock_interviews', ['user_id'], unique=False)
    op.create_index(op.f('ix_mock_interviews_category'), 'mock_interviews', ['category'], unique=False)

    # 12. opportunities
    op.create_table(
        'opportunities',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False, server_default='internship'),
        sa.Column('company_name', sa.String(length=150), nullable=False),
        sa.Column('job_title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('required_skills', sa.JSON(), nullable=False),
        sa.Column('eligibility_criteria', sa.Text(), nullable=False),
        sa.Column('graduation_years', sa.JSON(), nullable=False),
        sa.Column('minimum_cgpa', sa.Numeric(precision=4, scale=2), nullable=True),
        sa.Column('location', sa.String(length=120), nullable=False, server_default='Remote'),
        sa.Column('prize_or_stipend', sa.String(length=100), nullable=True),
        sa.Column('application_url', sa.String(length=500), nullable=False),
        sa.Column('deadline', sa.DateTime(timezone=True), nullable=False),
        sa.Column('source', sa.String(length=150), nullable=False, server_default='Verified Campus Board'),
        sa.Column('verification_status', sa.String(length=30), nullable=False, server_default='unverified'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_opportunities_id'), 'opportunities', ['id'], unique=False)
    op.create_index(op.f('ix_opportunities_category'), 'opportunities', ['category'], unique=False)
    op.create_index(op.f('ix_opportunities_company_name'), 'opportunities', ['company_name'], unique=False)
    op.create_index(op.f('ix_opportunities_deadline'), 'opportunities', ['deadline'], unique=False)
    op.create_index(op.f('ix_opportunities_verification_status'), 'opportunities', ['verification_status'], unique=False)

    # 13. saved_opportunities
    op.create_table(
        'saved_opportunities',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('opportunity_id', sa.Integer(), nullable=False),
        sa.Column('saved_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['opportunity_id'], ['opportunities.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'opportunity_id', name='uq_user_saved_opportunity')
    )
    op.create_index(op.f('ix_saved_opportunities_id'), 'saved_opportunities', ['id'], unique=False)
    op.create_index(op.f('ix_saved_opportunities_user_id'), 'saved_opportunities', ['user_id'], unique=False)
    op.create_index(op.f('ix_saved_opportunities_opportunity_id'), 'saved_opportunities', ['opportunity_id'], unique=False)

    # 14. application_tracking
    op.create_table(
        'application_tracking',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('opportunity_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=40), nullable=False, server_default='Interested'),
        sa.Column('applied_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['opportunity_id'], ['opportunities.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'opportunity_id', name='uq_user_application_tracking')
    )
    op.create_index(op.f('ix_application_tracking_id'), 'application_tracking', ['id'], unique=False)
    op.create_index(op.f('ix_application_tracking_user_id'), 'application_tracking', ['user_id'], unique=False)
    op.create_index(op.f('ix_application_tracking_opportunity_id'), 'application_tracking', ['opportunity_id'], unique=False)
    op.create_index(op.f('ix_application_tracking_status'), 'application_tracking', ['status'], unique=False)

    # 15. lecture_notes
    op.create_table(
        'lecture_notes',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('subject', sa.String(length=100), nullable=False),
        sa.Column('original_filename', sa.String(length=255), nullable=False),
        sa.Column('storage_filename', sa.String(length=255), nullable=False),
        sa.Column('file_size_bytes', sa.Integer(), nullable=False),
        sa.Column('extracted_text', sa.Text(), nullable=False),
        sa.Column('page_count', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('storage_filename')
    )
    op.create_index(op.f('ix_lecture_notes_id'), 'lecture_notes', ['id'], unique=False)
    op.create_index(op.f('ix_lecture_notes_user_id'), 'lecture_notes', ['user_id'], unique=False)
    op.create_index(op.f('ix_lecture_notes_subject'), 'lecture_notes', ['subject'], unique=False)

    # 16. note_summaries
    op.create_table(
        'note_summaries',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('note_id', sa.Integer(), nullable=False),
        sa.Column('summary_type', sa.String(length=50), nullable=False, server_default='executive'),
        sa.Column('summary_content', sa.Text(), nullable=False),
        sa.Column('is_ai_generated', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['note_id'], ['lecture_notes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_note_summaries_id'), 'note_summaries', ['id'], unique=False)
    op.create_index(op.f('ix_note_summaries_note_id'), 'note_summaries', ['note_id'], unique=False)

    # 17. flashcard_decks
    op.create_table(
        'flashcard_decks',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('note_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('card_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['note_id'], ['lecture_notes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_flashcard_decks_id'), 'flashcard_decks', ['id'], unique=False)
    op.create_index(op.f('ix_flashcard_decks_note_id'), 'flashcard_decks', ['note_id'], unique=False)
    op.create_index(op.f('ix_flashcard_decks_user_id'), 'flashcard_decks', ['user_id'], unique=False)

    # 18. flashcards
    op.create_table(
        'flashcards',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('deck_id', sa.Integer(), nullable=False),
        sa.Column('front_prompt', sa.Text(), nullable=False),
        sa.Column('back_solution', sa.Text(), nullable=False),
        sa.Column('mastery_level', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('last_reviewed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['deck_id'], ['flashcard_decks.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_flashcards_id'), 'flashcards', ['id'], unique=False)
    op.create_index(op.f('ix_flashcards_deck_id'), 'flashcards', ['deck_id'], unique=False)

    # 19. note_mcqs
    op.create_table(
        'note_mcqs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('note_id', sa.Integer(), nullable=False),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('options', sa.JSON(), nullable=False),
        sa.Column('correct_option', sa.String(length=10), nullable=False),
        sa.Column('explanation', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['note_id'], ['lecture_notes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_note_mcqs_id'), 'note_mcqs', ['id'], unique=False)
    op.create_index(op.f('ix_note_mcqs_note_id'), 'note_mcqs', ['note_id'], unique=False)

    # 20. marketplace_items
    op.create_table(
        'marketplace_items',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('seller_id', sa.Integer(), nullable=False),
        sa.Column('campus_name', sa.String(length=120), nullable=False),
        sa.Column('title', sa.String(length=180), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False, server_default='0.00'),
        sa.Column('condition', sa.String(length=30), nullable=False, server_default='used_good'),
        sa.Column('contact_method', sa.String(length=50), nullable=False, server_default='campus_email'),
        sa.Column('contact_details', sa.String(length=255), nullable=False),
        sa.Column('images_json', sa.JSON(), nullable=False),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='available'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['seller_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_marketplace_items_id'), 'marketplace_items', ['id'], unique=False)
    op.create_index(op.f('ix_marketplace_items_seller_id'), 'marketplace_items', ['seller_id'], unique=False)
    op.create_index(op.f('ix_marketplace_items_campus_name'), 'marketplace_items', ['campus_name'], unique=False)
    op.create_index(op.f('ix_marketplace_items_category'), 'marketplace_items', ['category'], unique=False)
    op.create_index(op.f('ix_marketplace_items_status'), 'marketplace_items', ['status'], unique=False)

    # 21. campus_clubs
    op.create_table(
        'campus_clubs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('lead_user_id', sa.Integer(), nullable=False),
        sa.Column('campus_name', sa.String(length=120), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('category', sa.String(length=60), nullable=False, server_default='coding'),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('logo_url', sa.String(length=300), nullable=True),
        sa.Column('is_official', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['lead_user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_campus_clubs_id'), 'campus_clubs', ['id'], unique=False)
    op.create_index(op.f('ix_campus_clubs_lead_user_id'), 'campus_clubs', ['lead_user_id'], unique=False)
    op.create_index(op.f('ix_campus_clubs_campus_name'), 'campus_clubs', ['campus_name'], unique=False)
    op.create_index(op.f('ix_campus_clubs_category'), 'campus_clubs', ['category'], unique=False)

    # 22. club_memberships
    op.create_table(
        'club_memberships',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('club_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(length=40), nullable=False, server_default='member'),
        sa.Column('joined_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['club_id'], ['campus_clubs.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('club_id', 'user_id', name='uq_club_user_membership')
    )
    op.create_index(op.f('ix_club_memberships_id'), 'club_memberships', ['id'], unique=False)
    op.create_index(op.f('ix_club_memberships_club_id'), 'club_memberships', ['club_id'], unique=False)
    op.create_index(op.f('ix_club_memberships_user_id'), 'club_memberships', ['user_id'], unique=False)

    # 23. community_posts
    op.create_table(
        'community_posts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.Column('campus_name', sa.String(length=120), nullable=False),
        sa.Column('post_type', sa.String(length=50), nullable=False, server_default='project_showcase'),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tags', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['author_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_community_posts_id'), 'community_posts', ['id'], unique=False)
    op.create_index(op.f('ix_community_posts_author_id'), 'community_posts', ['author_id'], unique=False)
    op.create_index(op.f('ix_community_posts_campus_name'), 'community_posts', ['campus_name'], unique=False)
    op.create_index(op.f('ix_community_posts_post_type'), 'community_posts', ['post_type'], unique=False)

    # 24. team_requests
    op.create_table(
        'team_requests',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('creator_id', sa.Integer(), nullable=False),
        sa.Column('campus_name', sa.String(length=120), nullable=False),
        sa.Column('event_or_project_name', sa.String(length=180), nullable=False),
        sa.Column('roles_needed', sa.JSON(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='open'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_team_requests_id'), 'team_requests', ['id'], unique=False)
    op.create_index(op.f('ix_team_requests_creator_id'), 'team_requests', ['creator_id'], unique=False)
    op.create_index(op.f('ix_team_requests_campus_name'), 'team_requests', ['campus_name'], unique=False)
    op.create_index(op.f('ix_team_requests_status'), 'team_requests', ['status'], unique=False)

    # 25. facility_tickets
    op.create_table(
        'facility_tickets',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('reporter_id', sa.Integer(), nullable=False),
        sa.Column('campus_name', sa.String(length=120), nullable=False),
        sa.Column('facility_area', sa.String(length=80), nullable=False, server_default='hostel'),
        sa.Column('block_or_building', sa.String(length=100), nullable=False),
        sa.Column('room_or_location', sa.String(length=100), nullable=False),
        sa.Column('issue_category', sa.String(length=60), nullable=False),
        sa.Column('title', sa.String(length=180), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('urgency', sa.String(length=20), nullable=False, server_default='medium'),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='open'),
        sa.Column('assigned_staff', sa.String(length=120), nullable=True),
        sa.Column('resolution_notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['reporter_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_facility_tickets_id'), 'facility_tickets', ['id'], unique=False)
    op.create_index(op.f('ix_facility_tickets_reporter_id'), 'facility_tickets', ['reporter_id'], unique=False)
    op.create_index(op.f('ix_facility_tickets_campus_name'), 'facility_tickets', ['campus_name'], unique=False)
    op.create_index(op.f('ix_facility_tickets_facility_area'), 'facility_tickets', ['facility_area'], unique=False)
    op.create_index(op.f('ix_facility_tickets_issue_category'), 'facility_tickets', ['issue_category'], unique=False)
    op.create_index(op.f('ix_facility_tickets_status'), 'facility_tickets', ['status'], unique=False)


def downgrade() -> None:
    op.drop_table('facility_tickets')
    op.drop_table('team_requests')
    op.drop_table('community_posts')
    op.drop_table('club_memberships')
    op.drop_table('campus_clubs')
    op.drop_table('marketplace_items')
    op.drop_table('note_mcqs')
    op.drop_table('flashcards')
    op.drop_table('flashcard_decks')
    op.drop_table('note_summaries')
    op.drop_table('lecture_notes')
    op.drop_table('application_tracking')
    op.drop_table('saved_opportunities')
    op.drop_table('opportunities')
    op.drop_table('mock_interviews')
    op.drop_table('resumes')
    op.drop_table('study_plan_tasks')
    op.drop_table('study_plans')
    op.drop_table('assessment_attempt_answers')
    op.drop_table('assessment_attempts')
    op.drop_table('assessment_questions')
    op.drop_table('assessments')
    op.drop_table('questions')
    op.drop_table('student_profiles')
    op.drop_table('users')
