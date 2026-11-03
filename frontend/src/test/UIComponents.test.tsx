import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Button, Card, CardHeader, CardTitle, CardContent, CardFooter, Badge, Modal, Tabs } from '../components/ui';

describe('UI Primitives - Design System', () => {
  describe('Button Component', () => {
    it('renders with children and handles clicks', () => {
      const handleClick = vi.fn();
      render(<Button onClick={handleClick}>Click Me</Button>);
      const btn = screen.getByRole('button', { name: /click me/i });
      expect(btn).toBeInTheDocument();
      fireEvent.click(btn);
      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('shows loading spinner and disables button when isLoading is true', () => {
      const handleClick = vi.fn();
      render(<Button isLoading onClick={handleClick}>Submit</Button>);
      const btn = screen.getByRole('button');
      expect(btn).toBeDisabled();
      expect(screen.getByTestId('button-spinner')).toBeInTheDocument();
      fireEvent.click(btn);
      expect(handleClick).not.toHaveBeenCalled();
    });

    it('applies danger and outline variant styling', () => {
      const { rerender } = render(<Button variant="danger">Delete</Button>);
      expect(screen.getByRole('button')).toHaveClass('bg-rose-600');

      rerender(<Button variant="outline">Cancel</Button>);
      expect(screen.getByRole('button')).toHaveClass('border-slate-700');
    });
  });

  describe('Card Component', () => {
    it('renders card header, title, content, and footer', () => {
      render(
        <Card>
          <CardHeader>
            <CardTitle>Assessment Module</CardTitle>
          </CardHeader>
          <CardContent>Diagnostic questions ready</CardContent>
          <CardFooter>Footer info</CardFooter>
        </Card>
      );

      expect(screen.getByText('Assessment Module')).toBeInTheDocument();
      expect(screen.getByText('Diagnostic questions ready')).toBeInTheDocument();
      expect(screen.getByText('Footer info')).toBeInTheDocument();
    });
  });

  describe('Badge Component', () => {
    it('renders text and dot indicator', () => {
      render(<Badge variant="brand" dot>Single-Campus</Badge>);
      expect(screen.getByText('Single-Campus')).toBeInTheDocument();
    });
  });

  describe('Modal Component', () => {
    it('renders when isOpen is true and fires onClose on close button click', () => {
      const handleClose = vi.fn();
      render(
        <Modal isOpen={true} onClose={handleClose} title="Test Modal">
          <p>Modal body content</p>
        </Modal>
      );

      expect(screen.getByText('Test Modal')).toBeInTheDocument();
      expect(screen.getByText('Modal body content')).toBeInTheDocument();

      const closeBtn = screen.getByRole('button', { name: /close modal/i });
      fireEvent.click(closeBtn);
      expect(handleClose).toHaveBeenCalledTimes(1);
    });

    it('does not render when isOpen is false', () => {
      render(
        <Modal isOpen={false} onClose={() => {}} title="Hidden">
          <p>Hidden content</p>
        </Modal>
      );

      expect(screen.queryByText('Hidden')).not.toBeInTheDocument();
    });
  });

  describe('Tabs Component', () => {
    it('switches tabs on click', () => {
      const handleChange = vi.fn();
      const tabs = [
        { id: 'tab1', label: 'Technical' },
        { id: 'tab2', label: 'Behavioral' },
      ];

      render(<Tabs tabs={tabs} activeTab="tab1" onChange={handleChange} />);
      expect(screen.getByText('Technical')).toBeInTheDocument();

      fireEvent.click(screen.getByText('Behavioral'));
      expect(handleChange).toHaveBeenCalledWith('tab2');
    });
  });
});

