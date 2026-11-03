import React from 'react';
import { Briefcase } from 'lucide-react';
import { ModulePlaceholder } from './ModulePlaceholder';

export const OpportunitiesPage: React.FC = () => (
  <ModulePlaceholder
    title="Universal Opportunity Hub (Pillar 2)"
    subtitle="Verified internships, hackathons, coding contests, scholarships, and job tracking"
    phase="Phase 14 Pillar"
    icon={<Briefcase className="w-6 h-6" />}
    features={[
      'Curated opportunities categorized into Internships, Hackathons, Competitions, Research, and Scholarships.',
      'Campus TPO verification flags ensuring legitimate, non-spam job postings.',
      'Personal Kanban application pipeline tracking: Interested -> Applied -> Shortlisted -> Interview -> Offer.',
      'Deadline countdowns and eligibility filtering matching student branch and CGPA.',
    ]}
  />
);
