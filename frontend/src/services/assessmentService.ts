import apiClient from '../lib/api';
import {
  AssessmentSummary,
  AssessmentDetail,
  StartAttemptResponse,
  AnswerSubmission,
  AttemptResult,
  AttemptHistoryItem,
  AssessmentOverviewStats,
  ApiResponse,
} from '../types';

export const assessmentService = {
  /**
   * Retrieves available assessment catalog with optional type filter.
   */
  async getAssessments(assessmentType?: string): Promise<AssessmentSummary[]> {
    const params: Record<string, string> = {};
    if (assessmentType && assessmentType !== 'all') {
      params.assessment_type = assessmentType;
    }
    const response = await apiClient.get<ApiResponse<AssessmentSummary[]>>('/assessments', { params });
    return response.data.data;
  },

  /**
   * Retrieves high-level placement assessment statistics.
   */
  async getStats(): Promise<AssessmentOverviewStats> {
    const response = await apiClient.get<ApiResponse<AssessmentOverviewStats>>('/assessments/stats');
    return response.data.data;
  },

  /**
   * Retrieves student's past assessment attempts.
   */
  async getHistory(): Promise<AttemptHistoryItem[]> {
    const response = await apiClient.get<ApiResponse<AttemptHistoryItem[]>>('/assessments/history');
    return response.data.data;
  },

  /**
   * Retrieves assessment overview and question sequence with answers masked.
   */
  async getAssessmentDetail(assessmentId: number): Promise<AssessmentDetail> {
    const response = await apiClient.get<ApiResponse<AssessmentDetail>>(`/assessments/${assessmentId}`);
    return response.data.data;
  },

  /**
   * Initiates or resumes a timed assessment session.
   */
  async startAssessment(assessmentId: number): Promise<StartAttemptResponse> {
    const response = await apiClient.post<ApiResponse<StartAttemptResponse>>(`/assessments/${assessmentId}/start`);
    return response.data.data;
  },

  /**
   * Submits selected answers for server-side evaluation.
   */
  async submitAssessment(attemptId: number, answers: AnswerSubmission[]): Promise<AttemptResult> {
    const response = await apiClient.post<ApiResponse<AttemptResult>>(
      `/assessments/attempts/${attemptId}/submit`,
      { answers }
    );
    return response.data.data;
  },

  /**
   * Retrieves full scorecard, diagnostic breakdown, and question review.
   */
  async getAttemptResults(attemptId: number): Promise<AttemptResult> {
    const response = await apiClient.get<ApiResponse<AttemptResult>>(
      `/assessments/attempts/${attemptId}/results`
    );
    return response.data.data;
  },
};

