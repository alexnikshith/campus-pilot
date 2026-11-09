import { AuthUser } from './index';

export interface TaxonomyItem {
  category: string;
  items: string[];
}

export interface TaxonomyResponse {
  degrees: string[];
  branches: string[];
  skills_by_category: TaxonomyItem[];
  target_roles: string[];
  hostel_blocks: string[];
  preferred_locations: string[];
}

export interface ProfileCompletenessBreakdown {
  total_percentage: number;
  basic_info: number;
  academic_info: number;
  target_roles: number;
  skills: number;
  hostel_info: number;
  missing_fields: string[];
  next_step_recommendation: string;
}

export interface StudentProfileData {
  id: number;
  user_id: number;
  user: AuthUser;
  degree: string;
  branch: string;
  graduation_year: number;
  cgpa: number | null;
  skills: string[];
  target_roles: string[];
  preferred_locations: string[];
  prep_hours_week: number;
  hostel_block: string | null;
  room_number: string | null;
  created_at: string;
  updated_at: string;
  completeness: ProfileCompletenessBreakdown;
}

export interface StudentProfileUpdatePayload {
  degree?: string;
  branch?: string;
  graduation_year?: number;
  cgpa?: number | null;
  skills?: string[];
  target_roles?: string[];
  preferred_locations?: string[];
  prep_hours_week?: number;
  hostel_block?: string | null;
  room_number?: string | null;
  phone_number?: string | null;
  bio?: string | null;
}

export interface OnboardingPayload {
  degree: string;
  branch: string;
  graduation_year: number;
  cgpa?: number | null;
  skills: string[];
  target_roles: string[];
  preferred_locations?: string[];
  prep_hours_week: number;
  hostel_block?: string | null;
  room_number?: string | null;
  phone_number?: string | null;
  bio?: string | null;
}

