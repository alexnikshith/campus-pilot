import React from 'react';
import { Sparkles, CheckCircle2, Database, Layers } from 'lucide-react';

export const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/60 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-400 flex items-center justify-center shadow-lg shadow-brand-500/20">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <span className="text-xl font-bold tracking-tight text-white">Placement<span className="text-brand-400">Pilot</span></span>
              <span className="hidden sm:inline-block ml-2 px-2 py-0.5 text-xs font-medium bg-brand-500/10 text-brand-400 rounded-full border border-brand-500/20">Phase 1 Initialized</span>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <a
              href="http://localhost:8000/docs"
              target="_blank"
              rel="noreferrer"
              className="text-xs sm:text-sm font-medium text-slate-300 hover:text-white transition-colors"
            >
              API Swagger
            </a>
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              System Ready
            </span>
          </div>
        </div>
      </header>

      {/* Main Hero Container */}
      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 flex flex-col justify-center">
        <div className="text-center max-w-3xl mx-auto space-y-6">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-slate-800/80 border border-slate-700 text-xs font-medium text-slate-300">
            <span className="w-2 h-2 rounded-full bg-brand-400"></span>
            <span>AI-Powered Placement Preparation Platform</span>
          </div>
          
          <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight text-white leading-tight">
            Elevate Your Engineering <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-400 to-indigo-300">Campus Placement</span> Journey
          </h1>

          <p className="text-base sm:text-lg text-slate-400 leading-relaxed">
            Personalized assessments, deterministic study plans, real coding practice, resume analysis, and intelligent mock interviews built for ambitious engineering graduates.
          </p>
        </div>

        {/* Phase 1 Verification Grid */}
        <div className="mt-14 grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto w-full">
          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 shadow-xl backdrop-blur-sm space-y-3">
            <div className="w-10 h-10 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5" />
            </div>
            <h2 className="text-lg font-semibold text-white">Frontend Stack Verified</h2>
            <p className="text-sm text-slate-400">
              React 18, TypeScript, Tailwind CSS, Vite, Lucide Icons, and Vitest testing suite configured and compiled.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 shadow-xl backdrop-blur-sm space-y-3">
            <div className="w-10 h-10 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center">
              <Database className="w-5 h-5" />
            </div>
            <h2 className="text-lg font-semibold text-white">Backend Environment</h2>
            <p className="text-sm text-slate-400">
              FastAPI, SQLAlchemy 2.x, Alembic, Pydantic, Argon2 password hashing, and Pytest installed in dedicated virtualenv.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 shadow-xl backdrop-blur-sm space-y-3">
            <div className="w-10 h-10 rounded-lg bg-brand-500/10 text-brand-400 flex items-center justify-center">
              <Layers className="w-5 h-5" />
            </div>
            <h2 className="text-lg font-semibold text-white">Modular Architecture</h2>
            <p className="text-sm text-slate-400">
              19 development phases mapped with deterministic fallback logic, isolated mock interviews, and zero secrets committed.
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 py-6 text-center text-xs text-slate-500">
        PlacementPilot &copy; 2026. Built with safety, rigor, and engineering excellence.
      </footer>
    </div>
  );
};

export default App;
