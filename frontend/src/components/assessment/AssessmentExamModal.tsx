import React, { useState, useEffect, useCallback, useMemo } from 'react';
import {
  Clock,
  Flag,
  ChevronLeft,
  ChevronRight,
  Send,
  AlertTriangle,
  RotateCcw,
} from 'lucide-react';
import { Modal } from '../ui/Modal';
import { Button } from '../ui/Button';
import { Badge } from '../ui/Badge';
import { StartAttemptResponse, AnswerSubmission } from '../../types';

interface AssessmentExamModalProps {
  isOpen: boolean;
  attempt: StartAttemptResponse;
  onClose: () => void;
  onSubmit: (answers: AnswerSubmission[]) => Promise<void>;
  isSubmitting?: boolean;
}

export const AssessmentExamModal: React.FC<AssessmentExamModalProps> = ({
  isOpen,
  attempt,
  onClose,
  onSubmit,
  isSubmitting = false,
}) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, string>>({});
  const [flaggedIds, setFlaggedIds] = useState<Set<number>>(new Set());
  const [showConfirmSubmit, setShowConfirmSubmit] = useState(false);

  // Calculate initial time remaining from expires_at
  const initialSeconds = useMemo(() => {
    const expireTime = new Date(attempt.expires_at).getTime();
    const nowTime = Date.now();
    const remaining = Math.max(0, Math.floor((expireTime - nowTime) / 1000));
    return remaining > 0 ? remaining : attempt.duration_minutes * 60;
  }, [attempt.expires_at, attempt.duration_minutes]);

  const [timeLeft, setTimeLeft] = useState(initialSeconds);

  const handleFinalSubmit = useCallback(() => {
    const formattedAnswers: AnswerSubmission[] = attempt.questions.map((q) => ({
      question_id: q.id,
      selected_option: selectedAnswers[q.id] || null,
    }));
    onSubmit(formattedAnswers);
  }, [attempt.questions, selectedAnswers, onSubmit]);

  // Countdown timer effect
  useEffect(() => {
    if (!isOpen) return;

    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          handleFinalSubmit();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [isOpen, handleFinalSubmit]);

  if (!isOpen || !attempt.questions || attempt.questions.length === 0) {
    return null;
  }

  const currentQ = attempt.questions[currentIndex];
  const totalQuestions = attempt.questions.length;
  const answeredCount = Object.keys(selectedAnswers).filter((k) => !!selectedAnswers[Number(k)]).length;
  const isFlagged = flaggedIds.has(currentQ.id);

  const formatTimer = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleOptionSelect = (optionId: string) => {
    setSelectedAnswers((prev) => ({
      ...prev,
      [currentQ.id]: optionId,
    }));
  };

  const handleClearOption = () => {
    setSelectedAnswers((prev) => {
      const updated = { ...prev };
      delete updated[currentQ.id];
      return updated;
    });
  };

  const toggleFlag = () => {
    setFlaggedIds((prev) => {
      const updated = new Set(prev);
      if (updated.has(currentQ.id)) {
        updated.delete(currentQ.id);
      } else {
        updated.add(currentQ.id);
      }
      return updated;
    });
  };

  const getDifficultyBadge = (diff: string) => {
    switch (diff.toLowerCase()) {
      case 'easy':
        return <Badge variant="success">Easy</Badge>;
      case 'hard':
        return <Badge variant="danger">Hard</Badge>;
      default:
        return <Badge variant="warning">Medium</Badge>;
    }
  };

  return (
    <>
      <Modal
        isOpen={isOpen}
        onClose={() => setShowConfirmSubmit(true)}
        closeOnOverlayClick={false}
        size="2xl"
        title={
          <div className="flex flex-wrap items-center justify-between gap-3 w-full pr-8">
            <div className="flex items-center gap-3">
              <span className="font-bold text-white text-base md:text-lg">
                {attempt.assessment_title}
              </span>
              <Badge variant="brand">Active Session</Badge>
            </div>
            <div
              className={`flex items-center gap-2 px-3 py-1.5 rounded-xl border text-sm font-mono font-bold ${
                timeLeft < 60
                  ? 'bg-rose-500/20 text-rose-400 border-rose-500/30 animate-pulse'
                  : timeLeft < 300
                  ? 'bg-amber-500/20 text-amber-400 border-amber-500/30'
                  : 'bg-slate-800 text-brand-300 border-slate-700'
              }`}
            >
              <Clock className="w-4 h-4" />
              <span>{formatTimer(timeLeft)}</span>
            </div>
          </div>
        }
      >
        <div className="flex flex-col lg:flex-row gap-6 min-h-[500px]">
          {/* Main Question Panel */}
          <div className="flex-1 flex flex-col justify-between">
            <div>
              {/* Question Meta Row */}
              <div className="flex flex-wrap items-center justify-between gap-2 pb-4 border-b border-slate-800 mb-4">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-bold text-brand-400">
                    Question {currentIndex + 1} of {totalQuestions}
                  </span>
                  <span className="text-slate-600">•</span>
                  <span className="text-xs text-slate-300 bg-slate-800 px-2 py-0.5 rounded border border-slate-700">
                    {currentQ.subject}
                  </span>
                  <span className="text-xs text-slate-400">
                    ({currentQ.topic})
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  {getDifficultyBadge(currentQ.difficulty)}
                  <span className="text-xs text-slate-400">
                    {currentQ.marks} {currentQ.marks === 1 ? 'Mark' : 'Marks'}
                  </span>
                </div>
              </div>

              {/* Question Text */}
              <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800/80 mb-6">
                <p className="text-base text-slate-100 leading-relaxed font-medium">
                  {currentQ.question_text}
                </p>
              </div>

              {/* Options List */}
              <div className="space-y-3 mb-6">
                {currentQ.options.map((opt) => {
                  const isSelected = selectedAnswers[currentQ.id] === opt.id;
                  return (
                    <button
                      key={opt.id}
                      type="button"
                      onClick={() => handleOptionSelect(opt.id)}
                      className={`w-full text-left p-4 rounded-xl border transition-all duration-150 flex items-start gap-3 ${
                        isSelected
                          ? 'bg-brand-500/15 border-brand-500/50 text-white shadow-sm'
                          : 'bg-slate-900/80 border-slate-800 text-slate-300 hover:bg-slate-800/60 hover:border-slate-700'
                      }`}
                    >
                      <span
                        className={`w-7 h-7 rounded-lg flex items-center justify-center font-bold text-xs shrink-0 transition-colors ${
                          isSelected
                            ? 'bg-brand-500 text-white'
                            : 'bg-slate-800 text-slate-400 border border-slate-700'
                        }`}
                      >
                        {opt.id}
                      </span>
                      <span className="text-sm pt-0.5 leading-snug">{opt.text}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Bottom Actions Row */}
            <div className="pt-4 border-t border-slate-800 flex flex-wrap items-center justify-between gap-3">
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={toggleFlag}
                  className={`flex items-center gap-1.5 ${
                    isFlagged ? 'border-amber-500/60 text-amber-400 bg-amber-500/10' : ''
                  }`}
                >
                  <Flag className="w-4 h-4" />
                  <span>{isFlagged ? 'Flagged' : 'Flag for Review'}</span>
                </Button>

                {selectedAnswers[currentQ.id] && (
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleClearOption}
                    className="text-slate-400 hover:text-slate-200"
                  >
                    <RotateCcw className="w-3.5 h-3.5 mr-1" />
                    <span>Clear</span>
                  </Button>
                )}
              </div>

              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setCurrentIndex((prev) => Math.max(0, prev - 1))}
                  disabled={currentIndex === 0}
                >
                  <ChevronLeft className="w-4 h-4 mr-1" />
                  <span>Previous</span>
                </Button>

                {currentIndex < totalQuestions - 1 ? (
                  <Button
                    variant="primary"
                    size="sm"
                    onClick={() => setCurrentIndex((prev) => Math.min(totalQuestions - 1, prev + 1))}
                  >
                    <span>Next</span>
                    <ChevronRight className="w-4 h-4 ml-1" />
                  </Button>
                ) : (
                  <Button
                    variant="primary"
                    size="sm"
                    onClick={() => setShowConfirmSubmit(true)}
                    className="bg-emerald-600 hover:bg-emerald-500"
                  >
                    <span>Review & Submit</span>
                    <Send className="w-3.5 h-3.5 ml-1.5" />
                  </Button>
                )}
              </div>
            </div>
          </div>

          {/* Right Question Palette & Summary Sidebar */}
          <div className="w-full lg:w-64 border-t lg:border-t-0 lg:border-l border-slate-800 pt-4 lg:pt-0 lg:pl-6 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                  Question Palette
                </h4>
                <span className="text-xs text-brand-400 font-semibold">
                  {answeredCount}/{totalQuestions} Answered
                </span>
              </div>

              {/* Question Number Matrix */}
              <div className="grid grid-cols-5 gap-2 mb-6">
                {attempt.questions.map((q, idx) => {
                  const isAnswered = !!selectedAnswers[q.id];
                  const flagged = flaggedIds.has(q.id);
                  const isCurrent = idx === currentIndex;

                  let style = 'bg-slate-800 text-slate-400 border-slate-700/80';
                  if (flagged) {
                    style = 'bg-amber-500/20 text-amber-300 border-amber-500/50';
                  } else if (isAnswered) {
                    style = 'bg-brand-600/30 text-brand-300 border-brand-500/40';
                  }

                  if (isCurrent) {
                    style += ' ring-2 ring-brand-400 font-bold';
                  }

                  return (
                    <button
                      key={q.id}
                      type="button"
                      onClick={() => setCurrentIndex(idx)}
                      className={`h-9 rounded-lg text-xs font-medium border flex items-center justify-center transition-all ${style}`}
                    >
                      {idx + 1}
                    </button>
                  );
                })}
              </div>

              {/* Status Legend */}
              <div className="space-y-2 text-xs text-slate-400 bg-slate-950/40 p-3 rounded-xl border border-slate-800/80">
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded bg-brand-600/30 border border-brand-500/40"></span>
                  <span>Answered ({answeredCount})</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded bg-amber-500/20 border border-amber-500/50"></span>
                  <span>Flagged for review ({flaggedIds.size})</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded bg-slate-800 border border-slate-700"></span>
                  <span>Unanswered ({totalQuestions - answeredCount})</span>
                </div>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-slate-800">
              <Button
                variant="primary"
                className="w-full flex items-center justify-center gap-2 bg-emerald-600 hover:bg-emerald-500"
                onClick={() => setShowConfirmSubmit(true)}
                isLoading={isSubmitting}
              >
                <Send className="w-4 h-4" />
                <span>Submit Assessment</span>
              </Button>
            </div>
          </div>
        </div>
      </Modal>

      {/* Confirmation Dialog */}
      <Modal
        isOpen={showConfirmSubmit}
        onClose={() => setShowConfirmSubmit(false)}
        size="sm"
        title={
          <div className="flex items-center gap-2 text-white">
            <AlertTriangle className="w-5 h-5 text-amber-400" />
            <span>Confirm Submission</span>
          </div>
        }
        footer={
          <div className="flex items-center justify-end gap-2 w-full">
            <Button
              variant="outline"
              size="sm"
              onClick={() => {
                setShowConfirmSubmit(false);
                onClose();
              }}
              disabled={isSubmitting}
            >
              Exit Assessment
            </Button>
            <Button
              variant="primary"
              size="sm"
              className="bg-emerald-600 hover:bg-emerald-500"
              onClick={handleFinalSubmit}
              isLoading={isSubmitting}
            >
              Confirm & Submit
            </Button>
          </div>
        }
      >
        <div className="space-y-3 py-2">
          <p className="text-sm text-slate-300">
            Are you sure you want to finalize and submit your assessment attempt?
          </p>
          <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 text-xs text-slate-400 space-y-1">
            <div className="flex justify-between">
              <span>Total Questions:</span>
              <span className="font-semibold text-white">{totalQuestions}</span>
            </div>
            <div className="flex justify-between">
              <span>Answered:</span>
              <span className="font-semibold text-emerald-400">{answeredCount}</span>
            </div>
            <div className="flex justify-between">
              <span>Unanswered / Skipped:</span>
              <span className="font-semibold text-amber-400">{totalQuestions - answeredCount}</span>
            </div>
          </div>
          <p className="text-xs text-slate-400">
            Once submitted, your answers will be scored server-side and your diagnostic performance report will be generated.
          </p>
        </div>
      </Modal>
    </>
  );
};
