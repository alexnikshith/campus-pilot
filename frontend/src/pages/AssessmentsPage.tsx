import React from 'react';
import { ClipboardCheck } from 'lucide-react';
import { ModulePlaceholder } from './ModulePlaceholder';

export const AssessmentsPage: React.FC = () => (
  <ModulePlaceholder
    title="Diagnostic Readiness Assessments"
    subtitle="Evaluate your readiness across 6 foundational engineering placement subjects"
    phase="Phase 7 Engine"
    icon={<ClipboardCheck className="w-6 h-6" />}
    features={[
      '6 Core Technical Subjects: Data Structures, Algorithms, DBMS, Operating Systems, Computer Networks, Aptitude.',
      'Timed assessment attempts with server-side scoring verification.',
      'Question bank filtering with hidden correct answers for cheat-proof testing.',
      'Granular weakness diagnostic report used to feed the deterministic study planner.',
    ]}
  />
);
