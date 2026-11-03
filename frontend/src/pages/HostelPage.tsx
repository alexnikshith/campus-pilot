import React from 'react';
import { Wrench } from 'lucide-react';
import { ModulePlaceholder } from './ModulePlaceholder';

export const HostelPage: React.FC = () => (
  <ModulePlaceholder
    title="Hostel & Facility Services (Pillar 5)"
    subtitle="Maintenance grievance reporting, room repairs tracking, and campus staff updates"
    phase="Phase 17 Pillar"
    icon={<Wrench className="w-6 h-6" />}
    features={[
      'Report facility issues: water coolers, electricity, WiFi outage, washroom repairs, furniture.',
      'Auto-populated hostel block and room number linked directly to student academic profile.',
      'Lifecycle tracking: Submitted -> Acknowledged -> In Progress -> Resolved.',
      'Campus staff notes and resolution feedback audit trail.',
    ]}
  />
);
