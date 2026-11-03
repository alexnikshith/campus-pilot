import React from 'react';
import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { AppLayout } from '../components/layout/AppLayout';
import {
  LoginPage,
  RegisterPage,
  DashboardPage,
  AssessmentsPage,
  StudyPlanPage,
  CodingPage,
  ResumePage,
  MockInterviewsPage,
  StudyAssistantPage,
  OpportunitiesPage,
  MarketplacePage,
  CommunityPage,
  HostelPage,
  ProfilePage,
  NotFoundPage,
} from '../pages';
import { GraduationCap, Loader2 } from 'lucide-react';

export const ProtectedRoute: React.FC<{ children?: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center space-y-4">
        <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-brand-600 to-indigo-500 flex items-center justify-center shadow-xl shadow-brand-500/25">
          <GraduationCap className="w-6 h-6 text-white" />
        </div>
        <div className="flex items-center gap-2 text-slate-400 text-xs font-medium">
          <Loader2 className="w-4 h-4 animate-spin text-brand-400" />
          <span>Authenticating campus session...</span>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children ? <>{children}</> : <AppLayout />;
};

export const AppRoutes: React.FC = () => {
  return (
    <Routes>
      {/* Public Authentication Routes */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      {/* Protected App Routes under Master Shell */}
      <Route element={<ProtectedRoute />}>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/assessments" element={<AssessmentsPage />} />
        <Route path="/study-plan" element={<StudyPlanPage />} />
        <Route path="/coding" element={<CodingPage />} />
        <Route path="/resume" element={<ResumePage />} />
        <Route path="/mock-interviews" element={<MockInterviewsPage />} />
        <Route path="/study-assistant" element={<StudyAssistantPage />} />
        <Route path="/opportunities" element={<OpportunitiesPage />} />
        <Route path="/marketplace" element={<MarketplacePage />} />
        <Route path="/community" element={<CommunityPage />} />
        <Route path="/hostel" element={<HostelPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
};
