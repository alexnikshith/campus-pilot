import React from 'react';
import { ShoppingBag } from 'lucide-react';
import { ModulePlaceholder } from './ModulePlaceholder';

export const MarketplacePage: React.FC = () => (
  <ModulePlaceholder
    title="Campus Peer Marketplace (Pillar 3)"
    subtitle="Verified student-to-student exchange for textbooks, lab kits, calculators, and tutoring"
    phase="Phase 15 Pillar"
    icon={<ShoppingBag className="w-6 h-6" />}
    features={[
      'Strict single-campus trust boundary: students only see listings from their own college.',
      'Categories for Engineering Textbooks, Lab Kits & Electronics, Drafters & Calculators, and Tutoring.',
      'Verified student seller badges backed by official college email domain authentication.',
      'Real-time item status controls: Available, Reserved, Sold, or Archived.',
    ]}
  />
);
