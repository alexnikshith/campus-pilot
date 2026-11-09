import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { AssessmentCard } from '../components/assessment/AssessmentCard';
import { AssessmentExamModal } from '../components/assessment/AssessmentExamModal';
import { AssessmentResultModal } from '../components/assessment/AssessmentResultModal';
import { AssessmentsPage } from '../pages/AssessmentsPage';
import { ToastProvider } from '../context/ToastContext';
import {
  AssessmentSummary,
  StartAttemptResponse,
  AttemptResult,
  AttemptHistoryItem,
  AssessmentOverviewStats,
} from '../types';
import * as assessmentServiceModule from '../services/assessmentService';

describe('Phase 7: Placement Readiness Assessment Engine', () => {
  const sampleSummary: AssessmentSummary = {
    id: 1,
    title: 'Comprehensive Technical Placement Readiness Diagnostic (2026)',
    description: 'Diagnostic placement evaluation covering DSA, Programming Fundamentals, DBMS, Operating Systems, Networks, and Aptitude.',
    assessment_type: 'diagnostic',
    duration_minutes: 45,
    pass_percentage: 60,
    total_questions: 12,
    total_marks: 12,
    subjects: ['Data Structures & Algorithms', 'Operating Systems', 'DBMS', 'Computer Networks', 'Programming Fundamentals', 'Aptitude'],
    is_active: true,
    created_at: new Date().toISOString(),
  };

  const sampleAttempt: StartAttemptResponse = {
    attempt_id: 101,
    assessment_id: 1,
    assessment_title: 'Comprehensive Technical Placement Readiness Diagnostic (2026)',
    duration_minutes: 45,
    started_at: new Date().toISOString(),
    expires_at: new Date(Date.now() + 45 * 60 * 1000).toISOString(),
    total_questions: 2,
    questions: [
      {
        id: 201,
        subject: 'Data Structures & Algorithms',
        topic: 'Binary Search Trees',
        difficulty: 'medium',
        question_text: 'What is the worst-case search complexity of an unbalanced BST?',
        question_type: 'mcq',
        options: [
          { id: 'A', text: 'O(1)' },
          { id: 'B', text: 'O(log n)' },
          { id: 'C', text: 'O(n)' },
          { id: 'D', text: 'O(n log n)' },
        ],
        marks: 1,
      },
      {
        id: 202,
        subject: 'Operating Systems',
        topic: 'Deadlocks',
        difficulty: 'hard',
        question_text: 'Which is NOT one of Coffman conditions?',
        question_type: 'mcq',
        options: [
          { id: 'A', text: 'Mutual Exclusion' },
          { id: 'B', text: 'Preemption Allowed' },
          { id: 'C', text: 'Hold and Wait' },
          { id: 'D', text: 'Circular Wait' },
        ],
        marks: 1,
      },
    ],
  };

  const sampleResult: AttemptResult = {
    attempt_id: 101,
    assessment_id: 1,
    assessment_title: 'Comprehensive Technical Placement Readiness Diagnostic (2026)',
    started_at: new Date().toISOString(),
    submitted_at: new Date().toISOString(),
    duration_seconds_taken: 360,
    total_score: 10,
    maximum_score: 12,
    percentage: 83.33,
    passed: true,
    pass_percentage: 60,
    status: 'completed',
    subject_breakdown: {
      'Data Structures & Algorithms': {
        score: 2,
        max: 2,
        percentage: 100,
        status: 'proficient',
        topics_needing_work: [],
      },
      'Operating Systems': {
        score: 0,
        max: 2,
        percentage: 0,
        status: 'needs_focus',
        topics_needing_work: ['Deadlocks', 'Paging'],
      },
    },
    strengths: ['Data Structures & Algorithms'],
    weaknesses: ['Operating Systems'],
    recommendations: ['Prioritize revision on Deadlocks in Operating Systems'],
    answers: [
      {
        id: 201,
        subject: 'Data Structures & Algorithms',
        topic: 'Binary Search Trees',
        difficulty: 'medium',
        question_text: 'What is the worst-case search complexity of an unbalanced BST?',
        question_type: 'mcq',
        options: [
          { id: 'A', text: 'O(1)' },
          { id: 'B', text: 'O(log n)' },
          { id: 'C', text: 'O(n)' },
          { id: 'D', text: 'O(n log n)' },
        ],
        correct_option: 'C',
        explanation: 'Degenerated BST traversal takes O(n).',
        marks: 1,
        selected_option: 'C',
        is_correct: true,
        marks_awarded: 1,
      },
      {
        id: 202,
        subject: 'Operating Systems',
        topic: 'Deadlocks',
        difficulty: 'hard',
        question_text: 'Which is NOT one of Coffman conditions?',
        question_type: 'mcq',
        options: [
          { id: 'A', text: 'Mutual Exclusion' },
          { id: 'B', text: 'Preemption Allowed' },
          { id: 'C', text: 'Hold and Wait' },
          { id: 'D', text: 'Circular Wait' },
        ],
        correct_option: 'B',
        explanation: 'No Preemption is required for deadlock; preemption prevents it.',
        marks: 1,
        selected_option: 'A',
        is_correct: false,
        marks_awarded: 0,
      },
    ],
  };

  describe('AssessmentCard Component', () => {
    it('renders assessment details, tags, and start action', () => {
      const onStart = vi.fn();
      render(<AssessmentCard assessment={sampleSummary} onStart={onStart} />);

      expect(screen.getByText('Comprehensive Technical Placement Readiness Diagnostic (2026)')).toBeInTheDocument();
      expect(screen.getByText('Diagnostic Baseline')).toBeInTheDocument();
      expect(screen.getByText('45 mins')).toBeInTheDocument();
      expect(screen.getByText('12 Questions')).toBeInTheDocument();
      expect(screen.getByText('60% to Pass')).toBeInTheDocument();
      expect(screen.getByText('Operating Systems')).toBeInTheDocument();

      const startBtn = screen.getByRole('button', { name: /Start Assessment/i });
      fireEvent.click(startBtn);
      expect(onStart).toHaveBeenCalledWith(sampleSummary);
    });
  });

  describe('AssessmentExamModal Component', () => {
    it('renders question and options without revealing correct answer', () => {
      const onSubmit = vi.fn().mockResolvedValue(undefined);
      render(
        <AssessmentExamModal
          isOpen={true}
          attempt={sampleAttempt}
          onClose={vi.fn()}
          onSubmit={onSubmit}
        />
      );

      // Question text and options
      expect(screen.getByText('What is the worst-case search complexity of an unbalanced BST?')).toBeInTheDocument();
      expect(screen.getByText('O(n)')).toBeInTheDocument();
      expect(screen.getByText('Question 1 of 2')).toBeInTheDocument();

      // Ensure explanation is NOT present
      expect(screen.queryByText(/Degenerated BST traversal/i)).not.toBeInTheDocument();
    });

    it('allows option selection, question navigation, and submission confirmation', async () => {
      const onSubmit = vi.fn().mockResolvedValue(undefined);
      render(
        <AssessmentExamModal
          isOpen={true}
          attempt={sampleAttempt}
          onClose={vi.fn()}
          onSubmit={onSubmit}
        />
      );

      // Select option C for Question 1
      const optC = screen.getByText('O(n)');
      fireEvent.click(optC);

      // Navigate to Next question
      const nextBtn = screen.getByRole('button', { name: /Next/i });
      fireEvent.click(nextBtn);

      expect(screen.getByText('Question 2 of 2')).toBeInTheDocument();
      expect(screen.getByText('Which is NOT one of Coffman conditions?')).toBeInTheDocument();

      // Submit test
      const reviewSubmitBtn = screen.getByRole('button', { name: /Review & Submit/i });
      fireEvent.click(reviewSubmitBtn);

      // Confirmation modal appears
      expect(screen.getByText('Confirm Submission')).toBeInTheDocument();
      const confirmBtn = screen.getByRole('button', { name: /Confirm & Submit/i });
      fireEvent.click(confirmBtn);

      await waitFor(() => {
        expect(onSubmit).toHaveBeenCalledTimes(1);
        const submittedAnswers = onSubmit.mock.calls[0][0];
        expect(submittedAnswers[0]).toEqual({ question_id: 201, selected_option: 'C' });
      });
    });
  });

  describe('AssessmentResultModal Component', () => {
    it('renders scorecard, subject breakdown, and review explanations', () => {
      render(
        <AssessmentResultModal
          isOpen={true}
          result={sampleResult}
          onClose={vi.fn()}
        />
      );

      // Score banner
      expect(screen.getByText('Assessment Passed')).toBeInTheDocument();
      expect(screen.getByText('83.33%')).toBeInTheDocument();
      expect(screen.getByText('Passing Requirement: 60% • Tested on', { exact: false })).toBeInTheDocument();

      // Subject breakdown
      expect(screen.getAllByText('Data Structures & Algorithms').length).toBeGreaterThan(0);
      expect(screen.getAllByText('Operating Systems').length).toBeGreaterThan(0);
      expect(screen.getByText('Focus Topics:')).toBeInTheDocument();

      // Review accordion
      expect(screen.getByText('Detailed Question-by-Question Review')).toBeInTheDocument();
      expect(screen.getByText('Q1. Data Structures & Algorithms')).toBeInTheDocument();

      // Expanding review shows technical explanation
      fireEvent.click(screen.getByText('Expand All'));
      expect(screen.getByText(/Degenerated BST traversal takes O\(n\)/i)).toBeInTheDocument();
      expect(screen.getByText(/No Preemption is required for deadlock/i)).toBeInTheDocument();
    });
  });

  describe('AssessmentsPage Full View', () => {
    beforeEach(() => {
      vi.spyOn(assessmentServiceModule.assessmentService, 'getAssessments').mockResolvedValue([sampleSummary]);
      vi.spyOn(assessmentServiceModule.assessmentService, 'getStats').mockResolvedValue({
        total_attempts: 1,
        completed_attempts: 1,
        average_score_percentage: 83.33,
        best_subject: 'Data Structures & Algorithms',
        focus_area: 'Operating Systems',
      } as AssessmentOverviewStats);
      vi.spyOn(assessmentServiceModule.assessmentService, 'getHistory').mockResolvedValue([
        {
          id: 101,
          assessment_id: 1,
          assessment_title: sampleSummary.title,
          assessment_type: sampleSummary.assessment_type,
          started_at: new Date().toISOString(),
          submitted_at: new Date().toISOString(),
          total_score: 10,
          maximum_score: 12,
          percentage: 83.33,
          passed: true,
          pass_percentage: 60,
          status: 'completed',
        } as AttemptHistoryItem,
      ]);
    });

    it('renders assessment catalog and overview metrics', async () => {
      render(
        <ToastProvider>
          <AssessmentsPage />
        </ToastProvider>
      );

      await waitFor(() => {
        expect(screen.getByText('Placement Readiness Assessments')).toBeInTheDocument();
        expect(screen.getByText('83.33%')).toBeInTheDocument();
        expect(screen.getAllByText(/Operating Systems/i).length).toBeGreaterThan(0);
        expect(screen.getByText('Comprehensive Technical Placement Readiness Diagnostic (2026)')).toBeInTheDocument();
      });

      // Switch to History tab
      const historyTab = screen.getByRole('button', { name: /My Attempt History/i });
      fireEvent.click(historyTab);

      await waitFor(() => {
        expect(screen.getByText('View Scorecard')).toBeInTheDocument();
        expect(screen.getByText('10 / 12')).toBeInTheDocument();
      });
    });
  });
});
