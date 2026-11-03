import React from 'react';
import { Code2 } from 'lucide-react';
import { ModulePlaceholder } from './ModulePlaceholder';

export const CodingPage: React.FC = () => (
  <ModulePlaceholder
    title="DSA Coding Practice Sandbox"
    subtitle="Interactive coding environment with test case runner and problem taxonomy"
    phase="Phase 10 Engine"
    icon={<Code2 className="w-6 h-6" />}
    features={[
      'Curated DSA problems categorized by topic (Arrays, Trees, Graphs, DP) and difficulty.',
      'In-browser Monaco/CodeMirror code editor supporting Python, Java, C++, and JavaScript.',
      'Sandboxed test case runner with visible sample tests and hidden boundary test cases.',
      'Time and memory complexity benchmarking with submission history.',
    ]}
  />
);
