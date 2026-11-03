// Global TypeScript definitions for PlacementPilot & Campus Super-App

export type UserRole = 'student' | 'admin' | 'campus_staff' | 'recruiter';

export interface StudentProfileBrief {
  id?: string;
  department?: string;
  degree?: string;
  academic_year?: number;
  current_cgpa?: number;
  target_roles?: string[];
  skills?: string[];
  hostel_block?: string;
  room_number?: string;
}

export interface AuthUser {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  campus_name: string;
  is_active: boolean;
  phone_number?: string | null;
  bio?: string | null;
  avatar_url?: string | null;
  profile?: StudentProfileBrief | null;
  created_at?: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export interface UserLoginRequest {
  email: string;
  password: string;
}

export interface UserRegisterRequest {
  email: string;
  password: string;
  full_name: string;
  campus_name: string;
  role?: UserRole;
  phone_number?: string;
  department?: string;
  degree?: string;
  academic_year?: number;
}

export interface ApiResponse<T = any> {
  success: boolean;
  data: T;
  message: string;
}

export interface ApiErrorDetail {
  code: string;
  message: string;
  details?: Record<string, any>;
}

export interface ApiErrorEnvelope {
  success: false;
  error: ApiErrorDetail;
}

export interface NavItem {
  title: string;
  href: string;
  icon: string;
  badge?: string;
  badgeVariant?: 'default' | 'brand' | 'success' | 'warning';
  description?: string;
}

export interface NavGroup {
  label: string;
  items: NavItem[];
}
