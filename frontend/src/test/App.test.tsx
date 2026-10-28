import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from '../App';

describe('PlacementPilot Frontend Setup', () => {
  it('renders the application brand and hero header', () => {
    render(<App />);
    const placementElements = screen.getAllByText(/Placement/i);
    expect(placementElements.length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText(/Phase 1 Initialized/i)).toBeInTheDocument();
  });

  it('renders Phase 1 verification modules', () => {
    render(<App />);
    expect(screen.getByText(/Frontend Stack Verified/i)).toBeInTheDocument();
    expect(screen.getByText(/Backend Environment/i)).toBeInTheDocument();
    expect(screen.getByText(/Modular Architecture/i)).toBeInTheDocument();
  });
});
