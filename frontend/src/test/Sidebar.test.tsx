import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { Sidebar } from '../components/layout/Sidebar';
import { AuthProvider } from '../context/AuthContext';

describe('Sidebar Navigation Shell', () => {
  const renderSidebar = (isCollapsed = false) => {
    const handleToggle = vi.fn();
    render(
      <BrowserRouter>
        <AuthProvider>
          <Sidebar isCollapsed={isCollapsed} onToggleCollapse={handleToggle} />
        </AuthProvider>
      </BrowserRouter>
    );
    return { handleToggle };
  };

  it('renders Placement Preparation links', () => {
    renderSidebar(false);
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Diagnostic Assessments')).toBeInTheDocument();
    expect(screen.getByText('Deterministic Study Plan')).toBeInTheDocument();
    expect(screen.getByText('DSA Coding Practice')).toBeInTheDocument();
    expect(screen.getByText('Resume ATS Analysis')).toBeInTheDocument();
    expect(screen.getByText('Mock Interviews')).toBeInTheDocument();
  });

  it('renders all 5 Campus Super-App Pillar links', () => {
    renderSidebar(false);
    expect(screen.getByText('AI Study Assistant')).toBeInTheDocument();
    expect(screen.getByText('Opportunity Hub')).toBeInTheDocument();
    expect(screen.getByText('Campus Marketplace')).toBeInTheDocument();
    expect(screen.getByText('Campus Community')).toBeInTheDocument();
    expect(screen.getByText('Hostel & Facilities')).toBeInTheDocument();
  });

  it('triggers collapse toggle when button clicked', () => {
    const { handleToggle } = renderSidebar(false);
    const toggleBtn = screen.getByRole('button', { name: /collapse sidebar/i });
    fireEvent.click(toggleBtn);
    expect(handleToggle).toHaveBeenCalledTimes(1);
  });
});

