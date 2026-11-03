import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Menu,
  Bell,
  Search,
  User,
  LogOut,
  ChevronDown,
  Sparkles,
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { Badge } from '../ui/Badge';

interface HeaderProps {
  onToggleMobileNav: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onToggleMobileNav }) => {
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  // Generate dynamic title from route pathname
  const getPageTitle = (path: string) => {
    switch (path) {
      case '/dashboard':
        return 'Placement Dashboard';
      case '/assessments':
        return 'Diagnostic Readiness Assessments';
      case '/study-plan':
        return 'Deterministic Study Roadmap';
      case '/coding':
        return 'DSA Coding Practice';
      case '/resume':
        return 'ATS Resume Rubric & Scoring';
      case '/mock-interviews':
        return 'Technical & HR Mock Interviews';
      case '/study-assistant':
        return 'AI Study Assistant';
      case '/opportunities':
        return 'Universal Opportunity Hub';
      case '/marketplace':
        return 'Campus Peer Marketplace';
      case '/community':
        return 'Campus Technical Community';
      case '/hostel':
        return 'Hostel & Facility Services';
      case '/profile':
        return 'Student Profile & Academic Settings';
      default:
        return 'PlacementPilot';
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="sticky top-0 z-20 flex items-center justify-between h-16 px-4 sm:px-6 border-b border-slate-800 bg-slate-950/80 backdrop-blur-md">
      {/* 1. Left Section: Mobile Menu + Page Title */}
      <div className="flex items-center gap-3">
        <button
          onClick={onToggleMobileNav}
          className="p-2 -ml-2 text-slate-400 hover:text-white rounded-xl md:hidden hover:bg-slate-800 transition-colors"
          aria-label="Open mobile navigation"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div>
          <h1 className="text-base sm:text-lg font-bold text-white tracking-tight">
            {getPageTitle(location.pathname)}
          </h1>
        </div>
      </div>

      {/* 2. Right Section: Search, Notifications, Profile Dropdown */}
      <div className="flex items-center gap-2 sm:gap-3">
        {/* Quick Search Shortcut Display */}
        <div className="hidden lg:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-400 cursor-pointer hover:border-slate-700 transition-colors">
          <Search className="w-3.5 h-3.5 text-slate-400" />
          <span>Search opportunities, problems, notes...</span>
          <kbd className="px-1.5 py-0.5 rounded bg-slate-800 border border-slate-700 text-[10px] font-mono text-slate-300">
            Ctrl+K
          </kbd>
        </div>

        {/* AI Ready Indicator */}
        <div className="hidden sm:inline-flex">
          <Badge variant="brand" dot pulse>
            <Sparkles className="w-3 h-3 mr-1 inline" />
            AI Online
          </Badge>
        </div>

        {/* Notifications Icon */}
        <button
          className="relative p-2 text-slate-400 hover:text-white rounded-xl hover:bg-slate-900 transition-colors"
          aria-label="View notifications"
        >
          <Bell className="w-5 h-5" />
          <span className="absolute top-2 right-2 w-2 h-2 rounded-full bg-brand-500" />
        </button>

        <div className="h-6 w-px bg-slate-800 mx-1" />

        {/* User Profile Dropdown */}
        <div className="relative">
          <button
            onClick={() => setIsDropdownOpen((prev) => !prev)}
            className="flex items-center gap-2 p-1.5 rounded-xl hover:bg-slate-900 transition-colors focus:outline-none"
            aria-expanded={isDropdownOpen}
            aria-haspopup="true"
          >
            <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-600 flex items-center justify-center font-bold text-xs text-white shadow-md shadow-brand-500/20">
              {user?.full_name ? user.full_name.charAt(0).toUpperCase() : 'U'}
            </div>
            <div className="hidden sm:block text-left">
              <p className="text-xs font-semibold text-white leading-none">
                {user?.full_name?.split(' ')[0] || 'Student'}
              </p>
              <p className="text-[10px] text-slate-400 capitalize mt-0.5">
                {user?.role || 'Student'}
              </p>
            </div>
            <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
          </button>

          {isDropdownOpen && (
            <>
              <div
                className="fixed inset-0 z-30"
                onClick={() => setIsDropdownOpen(false)}
              />
              <div className="absolute right-0 mt-2 w-56 rounded-2xl bg-slate-900 border border-slate-800 shadow-2xl z-40 py-1.5 animate-in fade-in zoom-in-95">
                <div className="px-4 py-2 border-b border-slate-800">
                  <p className="text-xs font-semibold text-white truncate">
                    {user?.full_name || 'Campus Student'}
                  </p>
                  <p className="text-[10px] text-slate-400 truncate mt-0.5">{user?.email}</p>
                  <p className="text-[10px] text-brand-400 font-medium truncate mt-1">
                    {user?.campus_name || 'Apex Institute of Technology'}
                  </p>
                </div>

                <div className="p-1 space-y-0.5">
                  <button
                    onClick={() => {
                      setIsDropdownOpen(false);
                      navigate('/profile');
                    }}
                    className="w-full flex items-center gap-2.5 px-3 py-2 text-xs font-medium text-slate-300 hover:text-white hover:bg-slate-800 rounded-xl transition-colors text-left"
                  >
                    <User className="w-4 h-4 text-slate-400" />
                    <span>Academic Profile</span>
                  </button>

                  <div className="h-px bg-slate-800 my-1" />

                  <button
                    onClick={handleLogout}
                    className="w-full flex items-center gap-2.5 px-3 py-2 text-xs font-medium text-rose-400 hover:text-rose-300 hover:bg-rose-500/10 rounded-xl transition-colors text-left"
                  >
                    <LogOut className="w-4 h-4 text-rose-400" />
                    <span>Sign Out</span>
                  </button>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </header>
  );
};
