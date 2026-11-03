import React from 'react';
import { CalendarRange } from 'lucide-react';
import { ModulePlaceholder } from './ModulePlaceholder';

export const StudyPlanPage: React.FC = () => (
  <ModulePlaceholder
    title="Deterministic Study Plan"
    subtitle="Algorithmic daily roadmaps and tasks customized to your individual diagnostic gaps"
    phase="Phase 8 Engine"
    icon={<CalendarRange className="w-6 h-6" />}
    features={[
      '100% deterministic rule-based scheduling algorithm running with zero external AI dependence.',
      'Generates weekly learning roadmaps prioritized by lowest diagnostic scores.',
      'Daily checklist tasks with interactive completion toggles.',
      'Dynamic catch-up scheduling adapting to completed and overdue tasks.',
    ]}
  />
);
