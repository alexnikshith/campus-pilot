export interface QuestionOption {
  id: string;
  text: string;
}

export interface QuestionPublic {
  id: number;
  subject: string;
  topic: string;
  difficulty: 'easy' | 'medium' | 'hard' | string;
  question_text: string;
  question_type: string;
  options: QuestionOption[];
  marks: number;
}

export interface QuestionReview {
  id: number;
  subject: string;
  topic: string;
  difficulty: string;
  question_text: string;
  question_type: string;
  options: QuestionOption[];
  correct_option: string;
  explanation: string;
  marks: number;
  selected_option: string | null;
  is_correct: boolean | null;
  marks_awarded: number;
}

export interface AssessmentSummary {
  id: number;
  title: string;
  description: string;
  assessment_type: 'diagnostic' | 'subject_mock' | 'company_mock' | string;
  duration_minutes: number;
  pass_percentage: number;
  total_questions: number;
  total_marks: number;
  subjects: string[];
  is_active: boolean;
  created_at: string;
}

export interface AssessmentDetail extends AssessmentSummary {
  questions: QuestionPublic[];
}

export interface StartAttemptResponse {
  attempt_id: number;
  assessment_id: number;
  assessment_title: string;
  duration_minutes: number;
  started_at: string;
  expires_at: string;
  total_questions: number;
  questions: QuestionPublic[];
}

export interface AnswerSubmission {
  question_id: number;
  selected_option?: string | null;
}

export interface SubmitAttemptRequest {
  answers: AnswerSubmission[];
}

export interface SubjectScoreDetail {
  score: number;
  max: number;
  percentage: number;
  status: 'proficient' | 'competent' | 'needs_focus' | string;
  topics_needing_work: string[];
}

export interface AttemptResult {
  attempt_id: number;
  assessment_id: number;
  assessment_title: string;
  started_at: string;
  submitted_at: string | null;
  duration_seconds_taken: number | null;
  total_score: number;
  maximum_score: number;
  percentage: number;
  passed: boolean;
  pass_percentage: number;
  status: 'completed' | 'in_progress' | 'expired' | string;
  subject_breakdown: Record<string, SubjectScoreDetail>;
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
  answers: QuestionReview[];
}

export interface AttemptHistoryItem {
  id: number;
  assessment_id: number;
  assessment_title: string;
  assessment_type: string;
  started_at: string;
  submitted_at: string | null;
  total_score: number;
  maximum_score: number;
  percentage: number;
  passed: boolean;
  pass_percentage: number;
  status: string;
}

export interface AssessmentOverviewStats {
  total_attempts: number;
  completed_attempts: number;
  average_score_percentage: number;
  best_subject: string | null;
  focus_area: string | null;
}
