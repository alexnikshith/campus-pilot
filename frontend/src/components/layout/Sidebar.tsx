import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
  Sparkles,
  LayoutDashboard,
  ClipboardCheck,
  CalendarRange,
  Code2,
  FileText,
  Video,
  Briefcase,
  ShoppingBag,
  Users,
  Wrench,
  ChevronLeft,
  ChevronRight,
  LogOut,
  Building2,
  GraduationCap,
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { cn } from '../../lib/utils';

interface SidebarProps {
  isCollapsed: boolean;
  onToggleCollapse: () => void;
  className?: string;
}

export const Sidebar: React.FC<SidebarProps> = ({
  isCollapsed,
  onToggleCollapse,
  className,
}) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const placementLinks = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { name: 'Diagnostic Assessments', href: '/assessments', icon: ClipboardCheck },
    { name: 'Deterministic Study Plan', href: '/study-plan', icon: CalendarRange },
    { name: 'DSA Coding Practice', href: '/coding', icon: Code2 },
    { name: 'Resume ATS Analysis', href: '/resume', icon: FileText },
    { name: 'Mock Interviews', href: '/mock-interviews', icon: Video },
  ];

  const campusPillarLinks = [
    { name: 'AI Study Assistant', href: '/study-assistant', icon: Sparkles, badge: 'AI' },
    { name: 'Opportunity Hub', href: '/opportunities', icon: Briefcase },
    { name: 'Campus Marketplace', href: '/marketplace', icon: ShoppingBag },
    { name: 'Campus Community', href: '/community', icon: Users },
    { name: 'Hostel & Facilities', href: '/hostel', icon: Wrench },
  ];

  return (
    <aside
      className={cn(
        'relative flex flex-col h-screen border-r border-slate-800 bg-slate-950/95 backdrop-blur-xl transition-all duration-300 z-30 select-none',
        isCollapsed ? 'w-20' : 'w-72',
        className
      )}
    >
      {/* 1. Brand Header */}
      <div className="flex items-center justify-between h-16 px-4 border-b border-slate-800/80">
        <div className="flex items-center space-x-3 overflow-hidden">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-500 flex items-center justify-center shrink-0 shadow-lg shadow-brand-500/25">
            <GraduationCap className="w-5 h-5 text-white" />
          </div>
          {!isCollapsed && (
            <div className="truncate">
              <span className="text-lg font-bold tracking-tight text-white">
                Placement<span className="text-brand-400">Pilot</span>
              </span>
              <span className="block text-[10px] uppercase font-semibold tracking-wider text-slate-400">
                Campus Super-App
              </span>
            </div>
          )}
        </div>

        <button
          onClick={onToggleCollapse}
          className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/80 transition-colors focus:outline-none"
          aria-label={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>

      {/* 2. Campus Affiliation Pill */}
      {!isCollapsed && (
        <div className="mx-3 my-3 p-3 rounded-xl bg-slate-900/90 border border-slate-800">
          <div className="flex items-center gap-2">
            <Building2 className="w-4 h-4 text-brand-400 shrink-0" />
            <div className="min-w-0 flex-1">
              <p className="text-xs font-semibold text-slate-200 truncate">
                {user?.campus_name || 'Apex Institute of Technology'}
              </p>
              <div className="flex items-center gap-1.5 mt-0.5">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                <span className="text-[10px] text-slate-400 font-medium capitalize">
                  {user?.role || 'Student'} Scope
                </span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 3. Navigation Links List */}
      <div className="flex-1 overflow-y-auto px-3 py-2 space-y-6">
        {/* Placement Preparation Engine */}
        <div>
          {!isCollapsed && (
            <h4 className="px-3 mb-2 text-[10px] font-bold uppercase tracking-wider text-slate-400">
              Placement Preparation
            </h4>
          )}
          <nav className="space-y-1">
            {placementLinks.map((item) => (
              <NavLink
                key={item.href}
                to={item.href}
                className={({ isActive }) =>
                  cn(
                    'group flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-all duration-150',
                    isActive
                      ? 'bg-gradient-to-r from-brand-600/20 to-indigo-600/10 text-white font-semibold border-l-2 border-brand-400 pl-[10px]'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
                  )
                }
                title={isCollapsed ? item.name : undefined}
              >
                <item.icon className="w-4 h-4 shrink-0 transition-transform group-hover:scale-110" />
                {!isCollapsed && <span className="truncate">{item.name}</span>}
              </NavLink>
            ))}
          </nav>
        </div>

        {/* 5 Campus Pillars */}
        <div>
          {!isCollapsed && (
            <h4 className="px-3 mb-2 text-[10px] font-bold uppercase tracking-wider text-slate-400">
              Campus Ecosystem
            </h4>
          )}
          <nav className="space-y-1">
            {campusPillarLinks.map((item) => (
              <NavLink
                key={item.href}
                to={item.href}
                className={({ isActive }) =>
                  cn(
                    'group flex items-center justify-between px-3 py-2.5 rounded-xl text-xs font-medium transition-all duration-150',
                    isActive
                      ? 'bg-gradient-to-r from-brand-600/20 to-indigo-600/10 text-white font-semibold border-l-2 border-brand-400 pl-[10px]'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
                  )
                }
                title={isCollapsed ? item.name : undefined}
              >
                <div className="flex items-center gap-3 min-w-0">
                  <item.icon className="w-4 h-4 shrink-0 transition-transform group-hover:scale-110" />
                  {!isCollapsed && <span className="truncate">{item.name}</span>}
                </div>
                {!isCollapsed && item.badge && (
                  <span className="px-1.5 py-0.5 rounded text-[9px] font-bold bg-brand-500/20 text-brand-400 border border-brand-500/30">
                    {item.badge}
                  </span>
                )}
              </NavLink>
            ))}
          </nav>
        </div>
      </div>

      {/* 4. User Profile Footer */}
      <div className="p-3 border-t border-slate-800/80 bg-slate-950">
        <div
          className={cn(
            'flex items-center gap-3 p-2 rounded-xl hover:bg-slate-900 transition-colors',
            isCollapsed && 'justify-center'
          )}
        >
          <div className="w-9 h-9 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center font-bold text-xs text-brand-400 shrink-0">
            {user?.full_name ? user.full_name.charAt(0).toUpperCase() : 'U'}
          </div>
          {!isCollapsed && (
            <div className="min-w-0 flex-1">
              <p className="text-xs font-semibold text-white truncate">
                {user?.full_name || 'Campus Student'}
              </p>
              <p className="text-[10px] text-slate-400 truncate">{user?.email || 'student@campus.edu'}</p>
            </div>
          )}
          {!isCollapsed && (
            <button
              onClick={handleLogout}
              className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-lg transition-colors"
              title="Sign Out"
              aria-label="Sign out"
            >
              <LogOut className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </aside>
  );
};
