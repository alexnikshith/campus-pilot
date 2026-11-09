import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Sparkles,
  ClipboardCheck,
  CalendarRange,
  Code2,
  FileText,
  Video,
  Briefcase,
  ShoppingBag,
  Users,
  Wrench,
  ArrowRight,
  TrendingUp,
  Target,
  CheckCircle2,
  Clock,
  AlertCircle,
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, Button, Badge } from '../components/ui';
import profileService from '../services/profileService';
import { ProfileCompletenessBreakdown } from '../types';

export const DashboardPage: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [completeness, setCompleteness] = useState<ProfileCompletenessBreakdown | null>(null);

  useEffect(() => {
    profileService
      .getCompleteness()
      .then(setCompleteness)
      .catch(() => {
        // Silent fail on dashboard if network is offline
      });
  }, []);

  const placementModules = [
    {
      title: 'Diagnostic Assessments',
      desc: 'Evaluate readiness across Data Structures, Algorithms, DBMS, OS, Networks, and Aptitude.',
      icon: ClipboardCheck,
      href: '/assessments',
      color: 'from-blue-500 to-indigo-600',
      action: 'Start Diagnostic',
    },
    {
      title: 'Deterministic Study Plan',
      desc: 'Algorithmically mapped daily tasks and weekly schedules targeting your assessment gaps.',
      icon: CalendarRange,
      href: '/study-plan',
      color: 'from-indigo-500 to-purple-600',
      action: 'View Roadmap',
    },
    {
      title: 'DSA Coding Sandbox',
      desc: 'Curated technical interview coding problems with browser editor and sandboxed runner.',
      icon: Code2,
      href: '/coding',
      color: 'from-emerald-500 to-teal-600',
      action: 'Practice DSA',
    },
    {
      title: 'ATS Resume Rubric',
      desc: 'Upload your PDF resume for instant keyword matching, parsing, and placement score.',
      icon: FileText,
      href: '/resume',
      color: 'from-amber-500 to-orange-600',
      action: 'Analyze Resume',
    },
    {
      title: 'Mock Interview Simulator',
      desc: 'Technical and behavioral interview practice with structured scoring rubrics and feedback.',
      icon: Video,
      href: '/mock-interviews',
      color: 'from-rose-500 to-pink-600',
      action: 'Start Interview',
    },
  ];

  const campusPillars = [
    {
      title: 'AI Study Assistant',
      desc: 'Upload lecture PDFs for instant summaries, flashcards, and grounded MCQs.',
      icon: Sparkles,
      href: '/study-assistant',
      badge: 'Feature 1',
    },
    {
      title: 'Opportunity Hub',
      desc: 'Verified off-campus & on-campus jobs, hackathons, and personal application tracker.',
      icon: Briefcase,
      href: '/opportunities',
      badge: 'Feature 2',
    },
    {
      title: 'Campus Marketplace',
      desc: 'Peer-to-peer textbook, calculator, lab kit, and tutoring exchange with verified peers.',
      icon: ShoppingBag,
      href: '/marketplace',
      badge: 'Feature 3',
    },
    {
      title: 'Campus Community',
      desc: 'Technical clubs, hackathon teammate matchmaking, and project showcase feeds.',
      icon: Users,
      href: '/community',
      badge: 'Feature 4',
    },
    {
      title: 'Hostel Services',
      desc: 'Report and track maintenance tickets (water, power, WiFi) with campus staff.',
      icon: Wrench,
      href: '/hostel',
      badge: 'Feature 5',
    },
  ];

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* 1. Hero Welcome & Readiness Overview */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-brand-900/60 via-slate-900 to-indigo-950/60 border border-slate-800 p-6 sm:p-8 shadow-2xl backdrop-blur-md">
        <div className="relative z-10 max-w-3xl space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-500/10 border border-brand-500/20 text-xs font-semibold text-brand-400">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Campus Scoped: {user?.campus_name || 'Apex Institute of Technology'}</span>
          </div>

          <h1 className="text-2xl sm:text-4xl font-extrabold text-white tracking-tight">
            Welcome back, <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-400 to-indigo-300">{user?.full_name?.split(' ')[0] || 'Student'}</span>!
          </h1>

          <p className="text-sm sm:text-base text-slate-300 leading-relaxed max-w-2xl">
            Your placement readiness journey is active. Take your diagnostic assessments to generate a personalized daily roadmap and unlock verified campus opportunities.
          </p>

          <div className="flex flex-wrap items-center gap-3 pt-2">
            <Button
              variant="primary"
              onClick={() => navigate('/assessments')}
              rightIcon={<ArrowRight className="w-4 h-4" />}
            >
              Take Assessment
            </Button>
            <Button
              variant="outline"
              onClick={() => navigate('/study-plan')}
            >
              Today&apos;s Study Tasks
            </Button>
          </div>
        </div>

        {/* Ambient background blur */}
        <div className="absolute right-0 top-0 -mt-12 -mr-12 w-96 h-96 bg-brand-600/15 rounded-full blur-3xl pointer-events-none" />
      </div>

      {/* Profile Completeness Alert (if incomplete) */}
      {completeness && completeness.total_percentage < 100 && (
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-4 rounded-2xl bg-gradient-to-r from-amber-500/10 via-slate-900 to-amber-500/5 border border-amber-500/20">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center shrink-0">
              <AlertCircle className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs sm:text-sm font-semibold text-white">
                Placement Profile is {completeness.total_percentage}% Complete
              </p>
              <p className="text-xs text-slate-400">
                {completeness.next_step_recommendation}
              </p>
            </div>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={() => navigate('/profile')}
            rightIcon={<ArrowRight className="w-3.5 h-3.5" />}
          >
            Complete Profile
          </Button>
        </div>
      )}

      {/* 2. Key Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card hoverEffect>
          <CardContent className="p-5 flex items-center justify-between">
            <div className="space-y-1">
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Readiness Score</p>
              <h3 className="text-2xl font-bold text-white">72%</h3>
              <p className="text-[11px] text-emerald-400 flex items-center gap-1">
                <TrendingUp className="w-3 h-3" /> +8% from baseline
              </p>
            </div>
            <div className="w-12 h-12 rounded-2xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center text-brand-400">
              <Target className="w-6 h-6" />
            </div>
          </CardContent>
        </Card>

        <Card hoverEffect>
          <CardContent className="p-5 flex items-center justify-between">
            <div className="space-y-1">
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Assessments Taken</p>
              <h3 className="text-2xl font-bold text-white">4 / 6</h3>
              <p className="text-[11px] text-slate-400">Core Technical Subjects</p>
            </div>
            <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
              <ClipboardCheck className="w-6 h-6" />
            </div>
          </CardContent>
        </Card>

        <Card hoverEffect>
          <CardContent className="p-5 flex items-center justify-between">
            <div className="space-y-1">
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Tasks Done Today</p>
              <h3 className="text-2xl font-bold text-white">3 / 5</h3>
              <p className="text-[11px] text-emerald-400 flex items-center gap-1">
                <CheckCircle2 className="w-3 h-3" /> 2 tasks remaining
              </p>
            </div>
            <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
              <Clock className="w-6 h-6" />
            </div>
          </CardContent>
        </Card>

        <Card hoverEffect>
          <CardContent className="p-5 flex items-center justify-between">
            <div className="space-y-1">
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Target Role</p>
              <h3 className="text-lg font-bold text-white truncate max-w-[140px]">Software Dev</h3>
              <p className="text-[11px] text-brand-400">Full-Stack / Backend</p>
            </div>
            <div className="w-12 h-12 rounded-2xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
              <Briefcase className="w-6 h-6" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* 3. Core Placement Preparation Modules */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold text-white tracking-tight">
              Placement Preparation Engine
            </h2>
            <p className="text-xs text-slate-400">
              Complete diagnostic evaluations, practice coding, and optimize your resume.
            </p>
          </div>
          <Badge variant="brand">Engine Active</Badge>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {placementModules.map((module) => (
            <Card key={module.title} hoverEffect className="flex flex-col justify-between">
              <CardHeader>
                <div className="flex items-center gap-3">
                  <div className={`w-10 h-10 rounded-xl bg-gradient-to-tr ${module.color} flex items-center justify-center text-white shadow-lg shadow-brand-500/10`}>
                    <module.icon className="w-5 h-5" />
                  </div>
                  <CardTitle className="text-base">{module.title}</CardTitle>
                </div>
                <CardDescription className="pt-2 text-xs">{module.desc}</CardDescription>
              </CardHeader>
              <div className="p-6 pt-0">
                <Button
                  variant="outline"
                  size="sm"
                  className="w-full justify-between"
                  onClick={() => navigate(module.href)}
                  rightIcon={<ArrowRight className="w-3.5 h-3.5" />}
                >
                  {module.action}
                </Button>
              </div>
            </Card>
          ))}
        </div>
      </div>

      {/* 4. The 5 Campus Super-App Pillars */}
      <div className="space-y-4 pt-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold text-white tracking-tight">
              Campus Super-App Ecosystem
            </h2>
            <p className="text-xs text-slate-400">
              Everyday engineering college life: AI lecture notes, opportunities, marketplace, and hostel services.
            </p>
          </div>
          <Badge variant="success">Single-Campus Scoped</Badge>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {campusPillars.map((pillar) => (
            <Card
              key={pillar.title}
              hoverEffect
              className="cursor-pointer group flex flex-col justify-between p-4"
              onClick={() => navigate(pillar.href)}
            >
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className="w-9 h-9 rounded-xl bg-slate-800 border border-slate-700/80 flex items-center justify-center text-brand-400 group-hover:scale-110 transition-transform">
                    <pillar.icon className="w-4 h-4" />
                  </div>
                  <span className="text-[10px] font-bold text-slate-400 bg-slate-800/80 px-2 py-0.5 rounded-full">
                    {pillar.badge}
                  </span>
                </div>
                <h3 className="text-sm font-semibold text-white group-hover:text-brand-300 transition-colors">
                  {pillar.title}
                </h3>
                <p className="text-[11px] text-slate-400 leading-relaxed line-clamp-3">
                  {pillar.desc}
                </p>
              </div>
              <div className="pt-3 flex items-center text-xs font-semibold text-brand-400 gap-1">
                <span>Explore</span>
                <ArrowRight className="w-3 h-3 group-hover:translate-x-1 transition-transform" />
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};
