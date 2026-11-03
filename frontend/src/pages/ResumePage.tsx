import React from 'react';
import { FileText } from 'lucide-react';
import { ModulePlaceholder } from './ModulePlaceholder';

export const ResumePage: React.FC = () => (
  <ModulePlaceholder
    title="ATS Resume Analysis Engine"
    subtitle="Secure PDF parsing, keyword extraction, and deterministic placement scoring"
    phase="Phase 11 Engine"
    icon={<FileText className="w-6 h-6" />}
    features={[
      'Secure PDF file parser with magic byte validation and 5MB upload limit.',
      'Deterministic keyword matching comparing extracted skills against target engineering roles.',
      'ATS scoring rubric evaluating contact information, education, experience, and project structure.',
      'Specific recommendations for missing technical keywords and formatting improvements.',
    ]}
  />
);
