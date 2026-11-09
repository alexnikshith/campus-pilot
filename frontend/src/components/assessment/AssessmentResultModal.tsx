import React, { useState } from 'react';
import {
  CheckCircle2,
  XCircle,
  AlertCircle,
  Clock,
  Target,
  BookOpen,
  Award,
  ChevronDown,
  ChevronUp,
} from 'lucide-react';
import { Modal } from '../ui/Modal';
import { Button } from '../ui/Button';
import { Badge } from '../ui/Badge';
import { AttemptResult } from '../../types';

interface AssessmentResultModalProps {
  isOpen: boolean;
  result: AttemptResult | null;
  onClose: () => void;
  onRetake?: () => void;
}

export const AssessmentResultModal: React.FC<AssessmentResultModalProps> = ({
  isOpen,
  result,
  onClose,
  onRetake,
}) => {
  const [filterType, setFilterType] = useState<'all' | 'incorrect' | 'correct'>('all');
  const [expandedQuestionIds, setExpandedQuestionIds] = useState<Set<number>>(new Set());

  if (!isOpen || !result) return null;

  const toggleExpand = (id: number) => {
    setExpandedQuestionIds((prev) => {
      const updated = new Set(prev);
      if (updated.has(id)) {
        updated.delete(id);
      } else {
        updated.add(id);
      }
      return updated;
    });
  };

  const expandAll = () => {
    setExpandedQuestionIds(new Set(result.answers.map((a) => a.id)));
  };

  const collapseAll = () => {
    setExpandedQuestionIds(new Set());
  };

  const filteredQuestions = result.answers.filter((q) => {
    if (filterType === 'correct') return q.is_correct === true;
    if (filterType === 'incorrect') return q.is_correct !== true;
    return true;
  });

  const correctCount = result.answers.filter((q) => q.is_correct === true).length;
  const incorrectCount = result.answers.length - correctCount;

  const formatSeconds = (sec: number | null) => {
    if (!sec) return 'N/A';
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return `${m}m ${s}s`;
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      size="2xl"
      title={
        <div className="flex items-center gap-3 pr-8">
          <Award className="w-6 h-6 text-brand-400" />
          <div>
            <h3 className="text-lg font-bold text-white leading-tight">
              Placement Readiness Scorecard
            </h3>
            <p className="text-xs text-slate-400">{result.assessment_title}</p>
          </div>
        </div>
      }
      footer={
        <div className="flex items-center justify-between w-full">
          <Button variant="outline" size="sm" onClick={onClose}>
            Close Scorecard
          </Button>
          {onRetake && (
            <Button variant="primary" size="sm" onClick={onRetake}>
              Retake Assessment
            </Button>
          )}
        </div>
      }
    >
      <div className="space-y-6 pb-2">
        {/* Score & Verdict Banner */}
        <div
          className={`p-6 rounded-2xl border flex flex-col md:flex-row items-center justify-between gap-6 ${
            result.passed
              ? 'bg-emerald-950/20 border-emerald-500/30 text-emerald-400'
              : 'bg-amber-950/20 border-amber-500/30 text-amber-400'
          }`}
        >
          <div className="flex items-center gap-4">
            <div
              className={`w-16 h-16 rounded-2xl flex items-center justify-center shrink-0 border ${
                result.passed
                  ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
                  : 'bg-amber-500/10 border-amber-500/30 text-amber-400'
              }`}
            >
              {result.passed ? (
                <CheckCircle2 className="w-10 h-10" />
              ) : (
                <AlertCircle className="w-10 h-10" />
              )}
            </div>
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xl font-bold text-white">
                  {result.passed ? 'Assessment Passed' : 'Target Threshold Not Met'}
                </span>
                <Badge variant={result.passed ? 'success' : 'warning'}>
                  {result.passed ? 'Proficient' : 'Needs Reinforcement'}
                </Badge>
              </div>
              <p className="text-xs text-slate-400">
                Passing Requirement: {result.pass_percentage}% • Tested on{' '}
                {new Date(result.started_at).toLocaleDateString()}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-6 divide-x divide-slate-800">
            <div className="text-center px-3">
              <span className="text-xs text-slate-400 uppercase tracking-wider block font-medium">
                Overall Score
              </span>
              <span className="text-2xl font-black text-white">
                {result.total_score}
                <span className="text-sm font-normal text-slate-400">
                  /{result.maximum_score}
                </span>
              </span>
            </div>

            <div className="text-center pl-6">
              <span className="text-xs text-slate-400 uppercase tracking-wider block font-medium">
                Readiness %
              </span>
              <span className="text-2xl font-black text-brand-400">
                {result.percentage}%
              </span>
            </div>

            <div className="text-center pl-6">
              <span className="text-xs text-slate-400 uppercase tracking-wider block font-medium">
                Time Spent
              </span>
              <span className="text-sm font-semibold text-slate-300 flex items-center gap-1 justify-center mt-1">
                <Clock className="w-3.5 h-3.5 text-slate-500" />
                {formatSeconds(result.duration_seconds_taken)}
              </span>
            </div>
          </div>
        </div>

        {/* 6-Subject Diagnostic Breakdown */}
        {result.subject_breakdown && Object.keys(result.subject_breakdown).length > 0 && (
          <div>
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-sm font-bold text-white flex items-center gap-2">
                <Target className="w-4 h-4 text-brand-400" />
                <span>Foundational Subjects Diagnostic Breakdown</span>
              </h4>
              <span className="text-xs text-slate-400">
                Evaluation across placement syllabus
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {Object.entries(result.subject_breakdown).map(([subject, detail]) => {
                let badgeVariant: 'success' | 'warning' | 'danger' = 'success';
                let barColor = 'bg-emerald-500';

                if (detail.status === 'needs_focus' || detail.percentage < 50) {
                  badgeVariant = 'danger';
                  barColor = 'bg-rose-500';
                } else if (detail.status === 'competent' || detail.percentage < 75) {
                  badgeVariant = 'warning';
                  barColor = 'bg-amber-500';
                }

                return (
                  <div
                    key={subject}
                    className="p-3.5 bg-slate-950/60 rounded-xl border border-slate-800/80 flex flex-col justify-between"
                  >
                    <div>
                      <div className="flex items-center justify-between gap-2 mb-2">
                        <span className="text-xs font-bold text-slate-200">
                          {subject}
                        </span>
                        <Badge variant={badgeVariant} className="text-[10px] capitalize">
                          {detail.status.replace('_', ' ')}
                        </Badge>
                      </div>

                      {/* Progress Bar */}
                      <div className="flex items-center gap-3 mb-2">
                        <div className="flex-1 bg-slate-800 h-2 rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full ${barColor} transition-all duration-300`}
                            style={{ width: `${Math.min(100, detail.percentage)}%` }}
                          />
                        </div>
                        <span className="text-xs font-semibold text-slate-300 min-w-[3rem] text-right">
                          {detail.percentage}%
                        </span>
                      </div>
                    </div>

                    {detail.topics_needing_work && detail.topics_needing_work.length > 0 && (
                      <div className="text-[11px] text-rose-400/90 bg-rose-950/30 p-1.5 rounded-lg border border-rose-900/40 mt-1">
                        <span className="font-medium text-rose-300">Focus Topics: </span>
                        {detail.topics_needing_work.join(', ')}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Strengths & Strategic Recommendations */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 bg-slate-900/60 rounded-xl border border-slate-800">
            <h5 className="text-xs font-bold uppercase tracking-wider text-emerald-400 mb-2 flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>Demonstrated Strengths</span>
            </h5>
            {result.strengths && result.strengths.length > 0 ? (
              <ul className="space-y-1.5">
                {result.strengths.map((str) => (
                  <li key={str} className="text-xs text-slate-300 flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                    <span>{str}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-xs text-slate-400">
                Complete more subject sprints to establish your top strengths.
              </p>
            )}
          </div>

          <div className="p-4 bg-slate-900/60 rounded-xl border border-slate-800">
            <h5 className="text-xs font-bold uppercase tracking-wider text-amber-400 mb-2 flex items-center gap-1.5">
              <AlertCircle className="w-3.5 h-3.5" />
              <span>Recommended Action Items</span>
            </h5>
            {result.recommendations && result.recommendations.length > 0 ? (
              <ul className="space-y-1.5">
                {result.recommendations.map((rec, i) => (
                  <li key={i} className="text-xs text-slate-300 flex items-start gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-amber-400 mt-1.5 shrink-0" />
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-xs text-slate-400">
                Consistent performance across all modules!
              </p>
            )}
          </div>
        </div>

        {/* Detailed Question Review */}
        <div>
          <div className="flex flex-wrap items-center justify-between gap-3 mb-3">
            <div className="flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-brand-400" />
              <h4 className="text-sm font-bold text-white">
                Detailed Question-by-Question Review
              </h4>
            </div>

            <div className="flex items-center gap-2">
              <div className="flex items-center bg-slate-900 p-0.5 rounded-lg border border-slate-800 text-xs">
                <button
                  type="button"
                  onClick={() => setFilterType('all')}
                  className={`px-2.5 py-1 rounded-md font-medium transition-colors ${
                    filterType === 'all'
                      ? 'bg-slate-800 text-white'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  All ({result.answers.length})
                </button>
                <button
                  type="button"
                  onClick={() => setFilterType('incorrect')}
                  className={`px-2.5 py-1 rounded-md font-medium transition-colors ${
                    filterType === 'incorrect'
                      ? 'bg-rose-500/20 text-rose-300'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  Wrong ({incorrectCount})
                </button>
                <button
                  type="button"
                  onClick={() => setFilterType('correct')}
                  className={`px-2.5 py-1 rounded-md font-medium transition-colors ${
                    filterType === 'correct'
                      ? 'bg-emerald-500/20 text-emerald-300'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  Correct ({correctCount})
                </button>
              </div>

              <div className="flex items-center gap-1 text-xs">
                <button
                  type="button"
                  onClick={expandAll}
                  className="px-2 py-1 text-slate-400 hover:text-white"
                >
                  Expand All
                </button>
                <span className="text-slate-700">|</span>
                <button
                  type="button"
                  onClick={collapseAll}
                  className="px-2 py-1 text-slate-400 hover:text-white"
                >
                  Collapse All
                </button>
              </div>
            </div>
          </div>

          {/* Question Review Cards */}
          <div className="space-y-3">
            {filteredQuestions.map((q, idx) => {
              const isExpanded = expandedQuestionIds.has(q.id);
              const isCorrect = q.is_correct === true;

              return (
                <div
                  key={q.id}
                  className={`rounded-xl border transition-all ${
                    isCorrect
                      ? 'bg-slate-900/50 border-slate-800'
                      : 'bg-rose-950/10 border-rose-900/30'
                  }`}
                >
                  {/* Question Header Accordion Trigger */}
                  <div
                    onClick={() => toggleExpand(q.id)}
                    className="p-4 flex items-center justify-between gap-3 cursor-pointer select-none"
                  >
                    <div className="flex items-center gap-3">
                      <div
                        className={`w-6 h-6 rounded-lg flex items-center justify-center shrink-0 text-xs font-bold ${
                          isCorrect
                            ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                            : 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                        }`}
                      >
                        {isCorrect ? <CheckCircle2 className="w-3.5 h-3.5" /> : <XCircle className="w-3.5 h-3.5" />}
                      </div>
                      <span className="text-xs font-bold text-slate-300">
                        Q{idx + 1}. {q.subject}
                      </span>
                      <span className="text-xs text-slate-500 hidden sm:inline">
                        • {q.topic}
                      </span>
                    </div>

                    <div className="flex items-center gap-3">
                      <span
                        className={`text-xs font-bold ${
                          isCorrect ? 'text-emerald-400' : 'text-rose-400'
                        }`}
                      >
                        +{q.marks_awarded} / {q.marks} Mark
                      </span>
                      {isExpanded ? (
                        <ChevronUp className="w-4 h-4 text-slate-400" />
                      ) : (
                        <ChevronDown className="w-4 h-4 text-slate-400" />
                      )}
                    </div>
                  </div>

                  {/* Expanded Content */}
                  {isExpanded && (
                    <div className="px-4 pb-4 pt-1 border-t border-slate-800/60 space-y-3">
                      <p className="text-sm text-slate-200 font-medium leading-relaxed">
                        {q.question_text}
                      </p>

                      {/* Options */}
                      <div className="space-y-1.5">
                        {q.options.map((opt) => {
                          const isSelectedByUser = q.selected_option === opt.id;
                          const isTheCorrectOption = q.correct_option === opt.id;

                          let optStyle = 'bg-slate-900/60 border-slate-800/80 text-slate-400';
                          if (isTheCorrectOption) {
                            optStyle = 'bg-emerald-500/15 border-emerald-500/50 text-emerald-200';
                          } else if (isSelectedByUser && !isCorrect) {
                            optStyle = 'bg-rose-500/15 border-rose-500/50 text-rose-200';
                          }

                          return (
                            <div
                              key={opt.id}
                              className={`p-2.5 rounded-lg border text-xs flex items-center justify-between gap-3 ${optStyle}`}
                            >
                              <div className="flex items-center gap-2.5">
                                <span className="font-bold w-5 h-5 rounded flex items-center justify-center bg-slate-800 text-slate-300 text-[10px]">
                                  {opt.id}
                                </span>
                                <span>{opt.text}</span>
                              </div>
                              <div className="flex items-center gap-2">
                                {isTheCorrectOption && (
                                  <span className="text-[10px] font-bold text-emerald-400 flex items-center gap-1">
                                    <CheckCircle2 className="w-3 h-3" /> Correct Answer
                                  </span>
                                )}
                                {isSelectedByUser && !isTheCorrectOption && (
                                  <span className="text-[10px] font-bold text-rose-400 flex items-center gap-1">
                                    <XCircle className="w-3 h-3" /> Your Choice
                                  </span>
                                )}
                              </div>
                            </div>
                          );
                        })}
                      </div>

                      {/* Technical Explanation Box */}
                      <div className="p-3 bg-brand-950/20 border border-brand-500/20 rounded-xl text-xs text-brand-200/90 leading-relaxed">
                        <span className="font-bold text-brand-400 block mb-1">
                          Technical Explanation:
                        </span>
                        {q.explanation}
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </Modal>
  );
};
