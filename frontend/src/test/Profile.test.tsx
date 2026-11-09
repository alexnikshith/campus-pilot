import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { ProfileCompletenessBar } from '../components/profile/ProfileCompletenessBar';
import { OnboardingWizardModal } from '../components/profile/OnboardingWizardModal';
import { ToastProvider } from '../context/ToastContext';
import { ProfileCompletenessBreakdown } from '../types';

describe('Phase 6: Student Profile & Onboarding Engine', () => {
  const sampleCompleteness: ProfileCompletenessBreakdown = {
    total_percentage: 75,
    basic_info: 20,
    academic_info: 25,
    target_roles: 10,
    skills: 10,
    hostel_info: 10,
    missing_fields: ['Technical skills inventory (min 5)', 'Add a 2nd target role'],
    next_step_recommendation: 'Add at least 5 technical skills to unlock accurate study plan generation.',
  };

  describe('ProfileCompletenessBar Component', () => {
    it('renders overall completeness score and recommendation', () => {
      render(
        <ProfileCompletenessBar
          completeness={sampleCompleteness}
          onOpenWizard={vi.fn()}
        />
      );

      expect(screen.getByText('75%')).toBeInTheDocument();
      expect(screen.getByText('Placement Profile Completeness')).toBeInTheDocument();
      expect(
        screen.getByText('Add at least 5 technical skills to unlock accurate study plan generation.')
      ).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /Complete Wizard/i })).toBeInTheDocument();
    });

    it('renders all 5 dimension metric badges', () => {
      render(<ProfileCompletenessBar completeness={sampleCompleteness} />);

      expect(screen.getByText('Basic Info')).toBeInTheDocument();
      expect(screen.getByText('20/20')).toBeInTheDocument();

      expect(screen.getByText('Academic Details')).toBeInTheDocument();
      expect(screen.getByText('25/25')).toBeInTheDocument();

      expect(screen.getByText('Target Roles')).toBeInTheDocument();
      expect(screen.getAllByText('10/20')).toHaveLength(2);

      expect(screen.getByText('Skills Inventory')).toBeInTheDocument();
      expect(screen.getByText('Hostel & Living')).toBeInTheDocument();
    });

    it('fires onOpenWizard callback when Complete Wizard button is clicked', () => {
      const handleOpen = vi.fn();
      render(
        <ProfileCompletenessBar
          completeness={sampleCompleteness}
          onOpenWizard={handleOpen}
        />
      );

      const btn = screen.getByRole('button', { name: /Complete Wizard/i });
      fireEvent.click(btn);
      expect(handleOpen).toHaveBeenCalledTimes(1);
    });

    it('shows Fully Verified indicator when score is 100%', () => {
      const fullCompleteness: ProfileCompletenessBreakdown = {
        total_percentage: 100,
        basic_info: 20,
        academic_info: 25,
        target_roles: 20,
        skills: 20,
        hostel_info: 15,
        missing_fields: [],
        next_step_recommendation: 'Your student profile is 100% complete and fully verified!',
      };

      render(<ProfileCompletenessBar completeness={fullCompleteness} />);
      expect(screen.getByText('100%')).toBeInTheDocument();
      expect(screen.getAllByText(/Fully Verified/i).length).toBeGreaterThanOrEqual(1);
    });
  });

  describe('OnboardingWizardModal Component', () => {
    it('renders Step 1 with Degree, Branch, and CGPA inputs', () => {
      render(
        <ToastProvider>
          <OnboardingWizardModal
            isOpen={true}
            onClose={vi.fn()}
            onComplete={vi.fn()}
          />
        </ToastProvider>
      );

      expect(screen.getByText('Student Placement Onboarding Wizard')).toBeInTheDocument();
      expect(screen.getByText('Academic Background')).toBeInTheDocument();
      expect(screen.getByLabelText(/Cumulative CGPA/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /Continue/i })).toBeInTheDocument();
    });

    it('navigates to Step 2 when Continue is clicked', () => {
      render(
        <ToastProvider>
          <OnboardingWizardModal
            isOpen={true}
            onClose={vi.fn()}
            onComplete={vi.fn()}
          />
        </ToastProvider>
      );

      const continueBtn = screen.getByRole('button', { name: /Continue/i });
      fireEvent.click(continueBtn);

      // Now on Step 2
      expect(screen.getByText(/Target Engineering Roles/i)).toBeInTheDocument();
      expect(screen.getByText(/Weekly Placement Prep Commitment/i)).toBeInTheDocument();
    });

    it('triggers onClose when Cancel is clicked', () => {
      const handleClose = vi.fn();
      render(
        <ToastProvider>
          <OnboardingWizardModal
            isOpen={true}
            onClose={handleClose}
            onComplete={vi.fn()}
          />
        </ToastProvider>
      );

      const cancelBtn = screen.getByRole('button', { name: /Cancel/i });
      fireEvent.click(cancelBtn);
      expect(handleClose).toHaveBeenCalledTimes(1);
    });
  });
});
