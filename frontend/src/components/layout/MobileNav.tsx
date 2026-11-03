import React, { useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import {
  X,
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
  GraduationCap,
  Sparkles,
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { cn } from '../../lib/utils';

interface MobileNavProps {
  isOpen: boolean;
  onClose: () => void;
}

export const MobileNav: React.FC<MobileNavProps> = ({ isOpen, onClose }) => {
  const { user } = useAuth();

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  if (!isOpen) return null;

  const placementLinks = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { name: 'Diagnostic Assessments', href: '/assessments', icon: ClipboardCheck },
    { name: 'Study Plan', href: '/study-plan', icon: CalendarRange },
    { name: 'DSA Coding Practice', href: '/coding', icon: Code2 },
    { name: 'Resume ATS Analysis', href: '/resume', icon: FileText },
    { name: 'Mock Interviews', href: '/mock-interviews', icon: Video },
  ];

  const campusPillarLinks = [
    { name: 'AI Study Assistant', href: '/study-assistant', icon: Sparkles },
    { name: 'Opportunity Hub', href: '/opportunities', icon: Briefcase },
    { name: 'Campus Marketplace', href: '/marketplace', icon: ShoppingBag },
    { name: 'Campus Community', href: '/community', icon: Users },
    { name: 'Hostel & Facilities', href: '/hostel', icon: Wrench },
  ];

  return (
    <div className="fixed inset-0 z-50 md:hidden flex" role="dialog" aria-modal="true">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm transition-opacity"
        onClick={onClose}
        data-testid="mobile-nav-backdrop"
      />

      {/* Drawer */}
      <div className="relative flex flex-col w-4/5 max-w-xs h-full bg-slate-950 border-r border-slate-800 shadow-2xl p-4 z-10 overflow-y-auto animate-in slide-in-from-left duration-200">
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-500 flex items-center justify-center shadow-md">
              <GraduationCap className="w-4 h-4 text-white" />
            </div>
            <div>
              <span className="text-base font-bold text-white tracking-tight">PlacementPilot</span>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-900"
            aria-label="Close navigation"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="my-3 p-3 rounded-xl bg-slate-900 border border-slate-800">
          <p className="text-xs font-semibold text-slate-200 truncate">
            {user?.campus_name || 'Apex Institute of Technology'}
          </p>
          <p className="text-[10px] text-slate-400 capitalize mt-0.5">
            {user?.role || 'Student'} Scope
          </p>
        </div>

        <div className="flex-1 space-y-6 pt-2">
          <div>
            <h4 className="px-2 mb-2 text-[10px] font-bold uppercase tracking-wider text-slate-400">
              Placement Preparation
            </h4>
            <nav className="space-y-1">
              {placementLinks.map((item) => (
                <NavLink
                  key={item.href}
                  to={item.href}
                  onClick={onClose}
                  className={({ isActive }) =>
                    cn(
                      'flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-medium transition-colors',
                      isActive
                        ? 'bg-brand-600/20 text-brand-400 font-semibold border-l-2 border-brand-400'
                        : 'text-slate-400 hover:text-white hover:bg-slate-900'
                    )
                  }
                >
                  <item.icon className="w-4 h-4 shrink-0" />
                  <span>{item.name}</span>
                </NavLink>
              ))}
            </nav>
          </div>

          <div>
            <h4 className="px-2 mb-2 text-[10px] font-bold uppercase tracking-wider text-slate-400">
              Campus Super-App
            </h4>
            <nav className="space-y-1">
              {campusPillarLinks.map((item) => (
                <NavLink
                  key={item.href}
                  to={item.href}
                  onClick={onClose}
                  className={({ isActive }) =>
                    cn(
                      'flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-medium transition-colors',
                      isActive
                        ? 'bg-brand-600/20 text-brand-400 font-semibold border-l-2 border-brand-400'
                        : 'text-slate-400 hover:text-white hover:bg-slate-900'
                    )
                  }
                >
                  <item.icon className="w-4 h-4 shrink-0" />
                  <span>{item.name}</span>
                </NavLink>
              ))}
            </nav>
          </div>
        </div>
      </div>
    </div>
  );
};
