import React from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, Badge, Button } from '../components/ui';
import { ArrowLeft, Construction } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface ModulePlaceholderProps {
  title: string;
  subtitle: string;
  phase: string;
  icon: React.ReactNode;
  features: string[];
  ctaLabel?: string;
  ctaAction?: () => void;
}

export const ModulePlaceholder: React.FC<ModulePlaceholderProps> = ({
  title,
  subtitle,
  phase,
  icon,
  features,
  ctaLabel = 'Return to Dashboard',
  ctaAction,
}) => {
  const navigate = useNavigate();

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl backdrop-blur-md">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-brand-600 to-indigo-500 flex items-center justify-center text-white shadow-lg shadow-brand-500/20 shrink-0">
            {icon}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl sm:text-2xl font-bold text-white tracking-tight">{title}</h1>
              <Badge variant="brand">{phase}</Badge>
            </div>
            <p className="text-xs sm:text-sm text-slate-400 mt-1">{subtitle}</p>
          </div>
        </div>

        <Button
          variant="outline"
          size="sm"
          leftIcon={<ArrowLeft className="w-4 h-4" />}
          onClick={ctaAction || (() => navigate('/dashboard'))}
        >
          {ctaLabel}
        </Button>
      </div>

      {/* Feature Architecture Overview */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2 text-brand-400 text-xs font-semibold uppercase tracking-wider">
            <Construction className="w-4 h-4" />
            <span>Architecture & Specifications In-Scope</span>
          </div>
          <CardTitle className="text-lg">Module Roadmap Capabilities</CardTitle>
          <CardDescription>
            This module builds on top of the Phase 2 database models and Phase 4 authentication.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {features.map((feature, idx) => (
              <div
                key={idx}
                className="flex items-start gap-3 p-4 rounded-xl bg-slate-950/60 border border-slate-800/80"
              >
                <div className="w-6 h-6 rounded-lg bg-brand-500/10 text-brand-400 flex items-center justify-center text-xs font-bold shrink-0 mt-0.5">
                  {idx + 1}
                </div>
                <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">{feature}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
