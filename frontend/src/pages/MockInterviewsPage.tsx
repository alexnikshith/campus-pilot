import React from 'react';
import { Video } from 'lucide-react';
import { ModulePlaceholder } from './ModulePlaceholder';

export const MockInterviewsPage: React.FC = () => (
  <ModulePlaceholder
    title="Mock Interview Simulator"
    subtitle="Simulate technical and behavioral interview rounds with structured rubrics"
    phase="Phase 12 Engine"
    icon={<Video className="w-6 h-6" />}
    features={[
      'Technical, System Design, and HR behavioral interview categories.',
      'Full offline practice mode working with deterministic structured grading rubrics.',
      'Optional LLM feedback evaluation for answer clarity, technical accuracy, and depth.',
      'Performance audit history tracking improvement trends across interview attempts.',
    ]}
  />
);
