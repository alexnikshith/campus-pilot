import apiClient from '../lib/api';
import {
  StudentProfileData,
  StudentProfileUpdatePayload,
  TaxonomyResponse,
  ProfileCompletenessBreakdown,
  OnboardingPayload,
  ApiResponse,
} from '../types';

export const profileService = {
  /**
   * Retrieves the authenticated student's full profile including completeness metrics.
   */
  async getProfile(): Promise<StudentProfileData> {
    const response = await apiClient.get<ApiResponse<StudentProfileData>>('/profile');
    return response.data.data;
  },

  /**
   * Updates academic credentials, placement targets, skills, or hostel details.
   */
  async updateProfile(payload: StudentProfileUpdatePayload): Promise<StudentProfileData> {
    const response = await apiClient.put<ApiResponse<StudentProfileData>>('/profile', payload);
    return response.data.data;
  },

  /**
   * Fetches standardized engineering degree, branch, skills, and roles taxonomy.
   */
  async getTaxonomy(): Promise<TaxonomyResponse> {
    const response = await apiClient.get<ApiResponse<TaxonomyResponse>>('/profile/taxonomy');
    return response.data.data;
  },

  /**
   * Retrieves detailed 5-dimension completeness breakdown and recommendations.
   */
  async getCompleteness(): Promise<ProfileCompletenessBreakdown> {
    const response = await apiClient.get<ApiResponse<ProfileCompletenessBreakdown>>('/profile/completeness');
    return response.data.data;
  },

  /**
   * Submits the complete multi-step onboarding wizard.
   */
  async completeOnboarding(payload: OnboardingPayload): Promise<StudentProfileData> {
    const response = await apiClient.post<ApiResponse<StudentProfileData>>('/profile/onboarding', payload);
    return response.data.data;
  },

  /**
   * Admin / Staff lookup of a student's profile.
   */
  async getProfileById(userId: number): Promise<StudentProfileData> {
    const response = await apiClient.get<ApiResponse<StudentProfileData>>(`/profile/${userId}`);
    return response.data.data;
  },
};

export default profileService;

