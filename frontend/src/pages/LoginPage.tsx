import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { GraduationCap, Mail, Lock, ArrowRight } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import { Button, Input, Card, CardContent } from '../components/ui';

export const LoginPage: React.FC = () => {
  const { login } = useAuth();
  const { error: toastError, success: toastSuccess } = useToast();
  const navigate = useNavigate();
  const location = useLocation();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [formErrors, setFormErrors] = useState<{ email?: string; password?: string }>({});

  const from = (location.state as any)?.from?.pathname || '/dashboard';

  const validate = (): boolean => {
    const errors: { email?: string; password?: string } = {};
    if (!email) {
      errors.email = 'Email address is required';
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      errors.email = 'Please enter a valid email address';
    }
    if (!password) {
      errors.password = 'Password is required';
    }
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    setIsLoading(true);
    try {
      await login({ email, password });
      toastSuccess('Signed in successfully! Welcome back.');
      navigate(from, { replace: true });
    } catch (err: any) {
      toastError(err.message || 'Invalid email or password. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemoFill = (demoRole: 'student' | 'admin') => {
    if (demoRole === 'student') {
      setEmail('student@apex.edu');
      setPassword('Placement@2026!');
    } else {
      setEmail('admin@apex.edu');
      setPassword('AdminMaster@2026!');
    }
    setFormErrors({});
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col justify-center py-12 sm:px-6 lg:px-8 relative overflow-hidden font-sans">
      {/* Subtle ambient lighting */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-brand-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="sm:mx-auto sm:w-full sm:max-w-md z-10 text-center space-y-2">
        <div className="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-gradient-to-tr from-brand-600 to-indigo-500 shadow-xl shadow-brand-500/25 mb-2">
          <GraduationCap className="w-6 h-6 text-white" />
        </div>
        <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          Placement<span className="text-brand-400">Pilot</span>
        </h2>
        <p className="text-xs sm:text-sm text-slate-400">
          Sign in to your campus placement preparation & ecosystem portal
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md z-10 px-4 sm:px-0">
        <Card className="border-slate-800/80 bg-slate-900/80 backdrop-blur-xl shadow-2xl">
          <CardContent className="pt-6">
            <form onSubmit={handleSubmit} className="space-y-4">
              <Input
                label="College Email"
                type="email"
                placeholder="student@apex.edu"
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value);
                  if (formErrors.email) setFormErrors((prev) => ({ ...prev, email: undefined }));
                }}
                error={formErrors.email}
                leftIcon={<Mail className="w-4 h-4" />}
                autoComplete="email"
              />

              <Input
                label="Password"
                type="password"
                placeholder="••••••••••••"
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value);
                  if (formErrors.password) setFormErrors((prev) => ({ ...prev, password: undefined }));
                }}
                error={formErrors.password}
                leftIcon={<Lock className="w-4 h-4" />}
                autoComplete="current-password"
              />

              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-400">Forgot credentials? Contact campus TPO.</span>
              </div>

              <Button
                type="submit"
                variant="primary"
                className="w-full"
                isLoading={isLoading}
                rightIcon={<ArrowRight className="w-4 h-4" />}
              >
                Sign In
              </Button>
            </form>

            {/* Demo Credential Quick-Fill */}
            <div className="mt-6 pt-5 border-t border-slate-800 text-center space-y-2">
              <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                Quick Demo Fill
              </p>
              <div className="flex justify-center gap-2">
                <button
                  type="button"
                  onClick={() => handleDemoFill('student')}
                  className="px-2.5 py-1 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
                >
                  Student Demo
                </button>
                <button
                  type="button"
                  onClick={() => handleDemoFill('admin')}
                  className="px-2.5 py-1 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
                >
                  Admin Demo
                </button>
              </div>
            </div>
          </CardContent>
        </Card>

        <p className="mt-6 text-center text-xs text-slate-400">
          New student on campus?{' '}
          <Link to="/register" className="font-semibold text-brand-400 hover:text-brand-300 transition-colors">
            Create an account
          </Link>
        </p>
      </div>
    </div>
  );
};
