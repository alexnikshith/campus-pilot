import React, { useState, useEffect, useCallback } from 'react';
import {
  ClipboardCheck,
  CheckCircle2,
  Clock,
  History,
  AlertCircle,
  TrendingUp,
  BookOpen,
  RefreshCw,
  Search,
} from 'lucide-react';
import { AssessmentCard } from '../components/assessment/AssessmentCard';
import { AssessmentExamModal } from '../components/assessment/AssessmentExamModal';
import { AssessmentResultModal } from '../components/assessment/AssessmentResultModal';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Skeleton } from '../components/ui/Skeleton';
import { useToast } from '../context/ToastContext';
import { assessmentService } from '../services/assessmentService';
import {
  AssessmentSummary,
  StartAttemptResponse,
  AttemptResult,
  AttemptHistoryItem,
  AssessmentOverviewStats,
  AnswerSubmission,
} from '../types';

export const AssessmentsPage: React.FC = () => {
  const { success: toastSuccess, error: toastError, info: toastInfo } = useToast();

  const [activeTab, setActiveTab] = useState<'catalog' | 'history'>('catalog');
  const [selectedType, setSelectedType] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');

  // Data states
  const [assessments, setAssessments] = useState<AssessmentSummary[]>([]);
  const [history, setHistory] = useState<AttemptHistoryItem[]>([]);
  const [stats, setStats] = useState<AssessmentOverviewStats | null>(null);

  // Loading states
  const [loading, setLoading] = useState(true);
  const [startingId, setStartingId] = useState<number | null>(null);
  const [submitting, setSubmitting] = useState(false);

  // Active exam / result modal states
  const [activeAttempt, setActiveAttempt] = useState<StartAttemptResponse | null>(null);
  const [activeResult, setActiveResult] = useState<AttemptResult | null>(null);
  const [loadingResultId, setLoadingResultId] = useState<number | null>(null);

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const [assessmentsData, historyData, statsData] = await Promise.all([
        assessmentService.getAssessments(selectedType !== 'all' ? selectedType : undefined),
        assessmentService.getHistory(),
        assessmentService.getStats(),
      ]);

      setAssessments(assessmentsData || []);
      setHistory(historyData || []);
      setStats(statsData || null);
    } catch {
      toastError('Failed to load placement assessments');
    } finally {
      setLoading(false);
    }
  }, [selectedType, toastError]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleStartAssessment = async (assessment: AssessmentSummary) => {
    setStartingId(assessment.id);
    try {
      const attempt = await assessmentService.startAssessment(assessment.id);
      setActiveAttempt(attempt);
      toastInfo(`Started timed session for ${assessment.title}`);
    } catch {
      toastError('Could not start assessment session. Please try again.');
    } finally {
      setStartingId(null);
    }
  };

  const handleSubmitAssessment = async (answers: AnswerSubmission[]) => {
    if (!activeAttempt) return;
    setSubmitting(true);
    try {
      const result = await assessmentService.submitAssessment(activeAttempt.attempt_id, answers);
      setActiveAttempt(null);
      setActiveResult(result);
      toastSuccess('Assessment submitted and evaluated successfully!');
      loadData(); // refresh history & stats
    } catch {
      toastError('Failed to submit assessment answers.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleViewScorecard = async (attemptId: number) => {
    setLoadingResultId(attemptId);
    try {
      const result = await assessmentService.getAttemptResults(attemptId);
      setActiveResult(result);
    } catch {
      toastError('Failed to load attempt scorecard');
    } finally {
      setLoadingResultId(null);
    }
  };

  const filteredAssessments = assessments.filter((a) => {
    if (!searchQuery.trim()) return true;
    const query = searchQuery.toLowerCase();
    return (
      a.title.toLowerCase().includes(query) ||
      a.description.toLowerCase().includes(query) ||
      (a.subjects && a.subjects.some((s) => s.toLowerCase().includes(query)))
    );
  });

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Header & Overview Stats Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="p-2 rounded-xl bg-brand-500/10 text-brand-400 border border-brand-500/20">
              <ClipboardCheck className="w-5 h-5" />
            </span>
            <h1 className="text-2xl font-bold text-white tracking-tight">
              Placement Readiness Assessments
            </h1>
          </div>
          <p className="text-sm text-slate-400">
            Comprehensive diagnostic evaluations and subject drills covering 6 core technical pillars.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={loadData}
            isLoading={loading}
            className="flex items-center gap-1.5"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Refresh</span>
          </Button>
        </div>
      </div>

      {/* Aggregate Metric Stats Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800">
          <div className="flex items-center justify-between text-xs font-medium text-slate-400 mb-1">
            <span>Tests Completed</span>
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          </div>
          <span className="text-2xl font-black text-white">
            {stats?.completed_attempts ?? 0}
          </span>
          <span className="text-[11px] text-slate-500 block mt-0.5">
            Evaluated attempts
          </span>
        </div>

        <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800">
          <div className="flex items-center justify-between text-xs font-medium text-slate-400 mb-1">
            <span>Average Readiness</span>
            <TrendingUp className="w-4 h-4 text-brand-400" />
          </div>
          <span className="text-2xl font-black text-brand-400">
            {stats?.average_score_percentage ? `${stats.average_score_percentage}%` : '0%'}
          </span>
          <span className="text-[11px] text-slate-500 block mt-0.5">
            Across technical pillars
          </span>
        </div>

        <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800">
          <div className="flex items-center justify-between text-xs font-medium text-slate-400 mb-1">
            <span>Strongest Subject</span>
            <BookOpen className="w-4 h-4 text-emerald-400" />
          </div>
          <span className="text-sm font-bold text-slate-200 truncate block mt-1">
            {stats?.best_subject || 'Take first test'}
          </span>
          <span className="text-[11px] text-slate-500 block mt-0.5">
            Highest mastery
          </span>
        </div>

        <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800">
          <div className="flex items-center justify-between text-xs font-medium text-slate-400 mb-1">
            <span>Priority Focus Area</span>
            <AlertCircle className="w-4 h-4 text-amber-400" />
          </div>
          <span className="text-sm font-bold text-amber-300 truncate block mt-1">
            {stats?.focus_area || 'None identified yet'}
          </span>
          <span className="text-[11px] text-slate-500 block mt-0.5">
            Recommended focus
          </span>
        </div>
      </div>

      {/* Primary Tab Navigation */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => setActiveTab('catalog')}
            className={`px-4 py-2 rounded-xl text-sm font-bold transition-all flex items-center gap-2 ${
              activeTab === 'catalog'
                ? 'bg-brand-500 text-white shadow-md'
                : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
            }`}
          >
            <ClipboardCheck className="w-4 h-4" />
            <span>Assessment Catalog ({assessments.length})</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('history')}
            className={`px-4 py-2 rounded-xl text-sm font-bold transition-all flex items-center gap-2 ${
              activeTab === 'history'
                ? 'bg-brand-500 text-white shadow-md'
                : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
            }`}
          >
            <History className="w-4 h-4" />
            <span>My Attempt History ({history.length})</span>
          </button>
        </div>

        {/* Search input in catalog tab */}
        {activeTab === 'catalog' && (
          <div className="flex items-center gap-3 w-full sm:w-auto">
            <div className="relative flex-1 sm:w-64">
              <Search className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search assessments, subjects..."
                className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
              />
            </div>

            <div className="flex items-center gap-1 text-xs">
              {['all', 'diagnostic', 'subject_mock'].map((t) => (
                <button
                  key={t}
                  type="button"
                  onClick={() => setSelectedType(t)}
                  className={`px-3 py-1 rounded-lg font-medium transition-colors ${
                    selectedType === t
                      ? 'bg-slate-800 text-brand-400 border border-slate-700'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {t === 'all' ? 'All' : t === 'diagnostic' ? 'Diagnostic' : 'Subject Mocks'}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Main Tab Content */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3].map((i) => (
            <div key={i} className="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-4">
              <Skeleton className="h-6 w-1/3" />
              <Skeleton className="h-5 w-3/4" />
              <Skeleton className="h-12 w-full" />
              <Skeleton className="h-10 w-full" />
            </div>
          ))}
        </div>
      ) : activeTab === 'catalog' ? (
        filteredAssessments.length === 0 ? (
          <div className="p-12 text-center rounded-2xl bg-slate-900/40 border border-slate-800/80">
            <ClipboardCheck className="w-10 h-10 text-slate-600 mx-auto mb-3" />
            <h3 className="text-base font-bold text-white mb-1">
              No assessments found
            </h3>
            <p className="text-xs text-slate-400 max-w-sm mx-auto mb-4">
              {searchQuery
                ? `No assessments matching "${searchQuery}". Try a different keyword.`
                : 'No active assessments available for the selected filter.'}
            </p>
            {searchQuery && (
              <Button variant="outline" size="sm" onClick={() => setSearchQuery('')}>
                Clear Filter
              </Button>
            )}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredAssessments.map((item) => (
              <AssessmentCard
                key={item.id}
                assessment={item}
                onStart={handleStartAssessment}
                isStarting={startingId === item.id}
              />
            ))}
          </div>
        )
      ) : (
        /* History View */
        history.length === 0 ? (
          <div className="p-12 text-center rounded-2xl bg-slate-900/40 border border-slate-800/80">
            <History className="w-10 h-10 text-slate-600 mx-auto mb-3" />
            <h3 className="text-base font-bold text-white mb-1">
              No assessment history yet
            </h3>
            <p className="text-xs text-slate-400 max-w-sm mx-auto mb-4">
              Start your first diagnostic assessment to generate your personalized placement readiness scorecard.
            </p>
            <Button variant="primary" size="sm" onClick={() => setActiveTab('catalog')}>
              Browse Assessments
            </Button>
          </div>
        ) : (
          <div className="overflow-x-auto rounded-2xl border border-slate-800 bg-slate-900">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950/60 text-slate-400 font-semibold border-b border-slate-800">
                <tr>
                  <th className="p-4">Assessment Title</th>
                  <th className="p-4">Date & Time</th>
                  <th className="p-4">Score</th>
                  <th className="p-4">Readiness %</th>
                  <th className="p-4">Result</th>
                  <th className="p-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/80 text-slate-300">
                {history.map((att) => (
                  <tr key={att.id} className="hover:bg-slate-850/50 transition-colors">
                    <td className="p-4 font-semibold text-white">
                      <div>{att.assessment_title}</div>
                      <span className="text-[10px] text-slate-500 uppercase tracking-wider">
                        {att.assessment_type.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="p-4 text-slate-400">
                      <div className="flex items-center gap-1.5">
                        <Clock className="w-3.5 h-3.5 text-slate-500" />
                        <span>{new Date(att.started_at).toLocaleString()}</span>
                      </div>
                    </td>
                    <td className="p-4 font-bold">
                      {att.total_score} / {att.maximum_score}
                    </td>
                    <td className="p-4 font-bold text-brand-400">
                      {att.percentage}%
                    </td>
                    <td className="p-4">
                      {att.status === 'completed' ? (
                        <Badge variant={att.passed ? 'success' : 'warning'}>
                          {att.passed ? 'Passed' : 'Needs Focus'}
                        </Badge>
                      ) : (
                        <Badge variant="outline">{att.status}</Badge>
                      )}
                    </td>
                    <td className="p-4 text-right">
                      {att.status === 'completed' ? (
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleViewScorecard(att.id)}
                          isLoading={loadingResultId === att.id}
                        >
                          View Scorecard
                        </Button>
                      ) : (
                        <span className="text-slate-500">In Progress</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )
      )}

      {/* Active Exam Modal */}
      {activeAttempt && (
        <AssessmentExamModal
          isOpen={true}
          attempt={activeAttempt}
          onClose={() => setActiveAttempt(null)}
          onSubmit={handleSubmitAssessment}
          isSubmitting={submitting}
        />
      )}

      {/* Scorecard Result Modal */}
      {activeResult && (
        <AssessmentResultModal
          isOpen={true}
          result={activeResult}
          onClose={() => setActiveResult(null)}
          onRetake={() => {
            const found = assessments.find((a) => a.id === activeResult.assessment_id);
            setActiveResult(null);
            if (found) {
              handleStartAssessment(found);
            }
          }}
        />
      )}
    </div>
  );
};
