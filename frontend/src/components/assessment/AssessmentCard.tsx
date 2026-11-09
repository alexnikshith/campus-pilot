import React from 'react';
import { Clock, HelpCircle, Target, ArrowRight, BookOpen } from 'lucide-react';
import { Card, CardContent } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { Button } from '../ui/Button';
import { AssessmentSummary } from '../../types';

interface AssessmentCardProps {
  assessment: AssessmentSummary;
  onStart: (assessment: AssessmentSummary) => void;
  isStarting?: boolean;
}

export const AssessmentCard: React.FC<AssessmentCardProps> = ({
  assessment,
  onStart,
  isStarting = false,
}) => {
  const getTypeBadge = (type: string) => {
    switch (type) {
      case 'diagnostic':
        return <Badge variant="brand">Diagnostic Baseline</Badge>;
      case 'subject_mock':
        return <Badge variant="warning">Subject Mock Drill</Badge>;
      case 'company_mock':
        return <Badge variant="success">Company Simulation</Badge>;
      default:
        return <Badge variant="default">Readiness Assessment</Badge>;
    }
  };

  return (
    <Card className="flex flex-col justify-between hover:border-slate-700 transition-all duration-200">
      <CardContent className="p-6 flex flex-col h-full justify-between">
        <div>
          <div className="flex items-center justify-between gap-3 mb-3">
            {getTypeBadge(assessment.assessment_type)}
            <span className="text-xs text-slate-400 flex items-center gap-1">
              <Clock className="w-3.5 h-3.5 text-slate-500" />
              {assessment.duration_minutes} mins
            </span>
          </div>

          <h3 className="text-lg font-bold text-white mb-2 leading-snug">
            {assessment.title}
          </h3>

          <p className="text-sm text-slate-400 mb-4 line-clamp-2">
            {assessment.description}
          </p>

          <div className="grid grid-cols-2 gap-2 p-3 bg-slate-950/50 rounded-xl border border-slate-800/80 mb-4">
            <div className="flex items-center gap-2 text-xs text-slate-300">
              <HelpCircle className="w-3.5 h-3.5 text-brand-400" />
              <span>{assessment.total_questions} Questions</span>
            </div>
            <div className="flex items-center gap-2 text-xs text-slate-300">
              <Target className="w-3.5 h-3.5 text-emerald-400" />
              <span>{assessment.pass_percentage}% to Pass</span>
            </div>
          </div>

          {assessment.subjects && assessment.subjects.length > 0 && (
            <div className="mb-4">
              <div className="text-xs font-medium text-slate-500 mb-1.5 flex items-center gap-1">
                <BookOpen className="w-3 h-3" />
                <span>Core Subjects Covered</span>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {assessment.subjects.map((subj) => (
                  <span
                    key={subj}
                    className="inline-block px-2 py-0.5 rounded text-[11px] font-medium bg-slate-800/70 text-slate-300 border border-slate-700/50"
                  >
                    {subj}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="pt-2 border-t border-slate-800/80 mt-auto">
          <Button
            variant="primary"
            className="w-full flex items-center justify-center gap-2"
            isLoading={isStarting}
            onClick={() => onStart(assessment)}
          >
            <span>Start Assessment</span>
            <ArrowRight className="w-4 h-4" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};
