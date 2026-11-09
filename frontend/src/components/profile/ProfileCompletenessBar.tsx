import React from 'react';
import { ProfileCompletenessBreakdown } from '../../types';
import { Card, CardContent, Button } from '../ui';
import { CheckCircle2, AlertCircle, Sparkles, ArrowRight } from 'lucide-react';
import { cn } from '../../lib/utils';

interface ProfileCompletenessBarProps {
  completeness: ProfileCompletenessBreakdown;
  onOpenWizard?: () => void;
  className?: string;
}

export const ProfileCompletenessBar: React.FC<ProfileCompletenessBarProps> = ({
  completeness,
  onOpenWizard,
  className,
}) => {
  const percentage = completeness.total_percentage;

  const getColor = (pct: number) => {
    if (pct >= 85) return 'from-emerald-500 to-teal-400 text-emerald-400 border-emerald-500/30';
    if (pct >= 50) return 'from-amber-500 to-orange-400 text-amber-400 border-amber-500/30';
    return 'from-rose-500 to-pink-500 text-rose-400 border-rose-500/30';
  };

  const dimensions = [
    { label: 'Basic Info', score: completeness.basic_info, max: 20 },
    { label: 'Academic Details', score: completeness.academic_info, max: 25 },
    { label: 'Target Roles', score: completeness.target_roles, max: 20 },
    { label: 'Skills Inventory', score: completeness.skills, max: 20 },
    { label: 'Hostel & Living', score: completeness.hostel_info, max: 15 },
  ];

  return (
    <Card className={cn('border-slate-800 bg-slate-900/90 shadow-xl overflow-hidden', className)}>
      <CardContent className="p-6 space-y-4">
        {/* Top Header Row */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center font-bold text-lg text-brand-400 shrink-0">
              {percentage}%
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-base font-bold text-white tracking-tight">
                  Placement Profile Completeness
                </h3>
                {percentage === 100 ? (
                  <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
                    <CheckCircle2 className="w-3 h-3" /> Fully Verified
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded-full border border-amber-500/20">
                    <AlertCircle className="w-3 h-3" /> Incomplete
                  </span>
                )}
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                {completeness.next_step_recommendation}
              </p>
            </div>
          </div>

          {percentage < 100 && onOpenWizard && (
            <Button
              variant="primary"
              size="sm"
              onClick={onOpenWizard}
              leftIcon={<Sparkles className="w-3.5 h-3.5" />}
              rightIcon={<ArrowRight className="w-3.5 h-3.5" />}
            >
              Complete Wizard
            </Button>
          )}
        </div>

        {/* Global Progress Bar */}
        <div className="w-full bg-slate-800/80 rounded-full h-2.5 overflow-hidden">
          <div
            className={cn('h-full rounded-full transition-all duration-500 bg-gradient-to-r', getColor(percentage))}
            style={{ width: `${percentage}%` }}
          />
        </div>

        {/* 5-Dimension Mini Progress Badges */}
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 pt-1">
          {dimensions.map((dim) => {
            const dimPct = Math.round((dim.score / dim.max) * 100);
            return (
              <div
                key={dim.label}
                className="p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/80 space-y-1"
              >
                <div className="flex justify-between items-center text-[10px]">
                  <span className="text-slate-400 truncate">{dim.label}</span>
                  <span className="font-semibold text-slate-300">
                    {dim.score}/{dim.max}
                  </span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                  <div
                    className={cn(
                      'h-full rounded-full',
                      dimPct === 100 ? 'bg-emerald-400' : dimPct > 0 ? 'bg-brand-400' : 'bg-slate-700'
                    )}
                    style={{ width: `${dimPct}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
};

