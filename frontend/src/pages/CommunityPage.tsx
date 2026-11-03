import React from 'react';
import { Users } from 'lucide-react';
import { ModulePlaceholder } from './ModulePlaceholder';

export const CommunityPage: React.FC = () => (
  <ModulePlaceholder
    title="Campus Technical Community (Pillar 4)"
    subtitle="College technical clubs, project showcase feed, and hackathon teammate matchmaking"
    phase="Phase 16 Pillar"
    icon={<Users className="w-6 h-6" />}
    features={[
      'Campus club directory (Coding Club, Robotics, GDSC, IEEE, E-Cell) with join requests.',
      'Teammate matchmaking for Smart India Hackathon and college project teams by tech stack.',
      'Student project idea showcase with upvoting, feedback, and peer collaboration requests.',
      'Campus tech events calendar with RSVP tracking.',
    ]}
  />
);
