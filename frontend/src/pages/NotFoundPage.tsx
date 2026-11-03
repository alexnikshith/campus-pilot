import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Compass, ArrowLeft } from 'lucide-react';
import { Button, Card, CardContent } from '../components/ui';

export const NotFoundPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-[80vh] flex items-center justify-center p-4">
      <Card className="max-w-md w-full text-center border-slate-800 bg-slate-900/90 shadow-2xl">
        <CardContent className="pt-8 pb-8 space-y-4">
          <div className="w-16 h-16 rounded-2xl bg-brand-500/10 border border-brand-500/20 text-brand-400 flex items-center justify-center mx-auto">
            <Compass className="w-8 h-8 animate-spin-slow" />
          </div>
          <h2 className="text-3xl font-extrabold text-white">404</h2>
          <h3 className="text-base font-semibold text-slate-200">Page Not Found</h3>
          <p className="text-xs text-slate-400">
            The page you are looking for does not exist or has been moved within the campus portal.
          </p>
          <div className="pt-2">
            <Button
              variant="primary"
              size="sm"
              leftIcon={<ArrowLeft className="w-4 h-4" />}
              onClick={() => navigate('/dashboard')}
            >
              Back to Dashboard
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
