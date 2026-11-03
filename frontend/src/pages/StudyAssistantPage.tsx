import React from 'react';
import { Sparkles } from 'lucide-react';
import { ModulePlaceholder } from './ModulePlaceholder';

export const StudyAssistantPage: React.FC = () => (
  <ModulePlaceholder
    title="AI Study Assistant (Pillar 1)"
    subtitle="Upload lecture PDFs for local extraction, summaries, flashcards, and grounded MCQs"
    phase="Phase 13 Pillar"
    icon={<Sparkles className="w-6 h-6" />}
    features={[
      'Upload college lecture PDFs and syllabus documents with local text extraction.',
      'Deterministic extractive summaries and conceptual flashcard deck generation.',
      'Leitner spaced-repetition flashcard mastery tracker (levels 0-5).',
      'Lecture-grounded MCQ generator with answers rooted strictly in uploaded course material.',
    ]}
  />
);
