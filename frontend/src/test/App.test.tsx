import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import App from '../App';

describe('PlacementPilot Shell & Authentication Flow', () => {
  it('mounts the app and redirects unauthenticated users to the LoginPage', async () => {
    render(<App />);
    // Brand header check
    const brandTitles = await screen.findAllByText(/Placement/i);
    expect(brandTitles.length).toBeGreaterThanOrEqual(1);

    // Login page prompt checks
    expect(screen.getByText(/Sign in to your campus placement preparation/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/College Email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/^Password$/i)).toBeInTheDocument();
  });

  it('allows quick demo credential auto-fill for student and admin', async () => {
    render(<App />);

    const studentDemoBtn = await screen.findByRole('button', { name: /Student Demo/i });
    expect(studentDemoBtn).toBeInTheDocument();

    fireEvent.click(studentDemoBtn);

    const emailInput = screen.getByLabelText(/College Email/i) as HTMLInputElement;
    expect(emailInput.value).toBe('student@apex.edu');
  });

  it('renders link to create new student account', async () => {
    render(<App />);
    const registerLink = await screen.findByRole('link', { name: /create an account/i });
    expect(registerLink).toBeInTheDocument();
    expect(registerLink).toHaveAttribute('href', '/register');
  });
});
