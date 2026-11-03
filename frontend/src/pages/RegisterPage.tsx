import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { GraduationCap, Mail, Lock, User, Building2, ArrowRight } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import { Button, Input, Card, CardContent } from '../components/ui';

export const RegisterPage: React.FC = () => {
  const { register: registerUser } = useAuth();
  const { error: toastError, success: toastSuccess } = useToast();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    password: '',
    campusName: 'Apex Institute of Technology',
    department: 'Computer Science and Engineering',
    academicYear: 3,
  });

  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validate = (): boolean => {
    const errs: Record<string, string> = {};
    if (!formData.fullName.trim()) errs.fullName = 'Full name is required';
    if (!formData.email.trim()) {
      errs.email = 'Email address is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errs.email = 'Please enter a valid email address';
    }
    if (!formData.password) {
      errs.password = 'Password is required';
    } else if (formData.password.length < 8) {
      errs.password = 'Password must be at least 8 characters long';
    } else if (
      !/[A-Z]/.test(formData.password) ||
      !/[a-z]/.test(formData.password) ||
      !/[0-9]/.test(formData.password)
    ) {
      errs.password = 'Must contain uppercase, lowercase, and numeric characters';
    }
    if (!formData.campusName.trim()) errs.campusName = 'Campus name is required';

    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    setIsLoading(true);
    try {
      await registerUser({
        full_name: formData.fullName,
        email: formData.email,
        password: formData.password,
        campus_name: formData.campusName,
        department: formData.department,
        academic_year: Number(formData.academicYear),
      });

      toastSuccess('Registration successful! Welcome to PlacementPilot.');
      navigate('/dashboard', { replace: true });
    } catch (err: any) {
      toastError(err.message || 'Registration failed. Please check your information.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col justify-center py-12 sm:px-6 lg:px-8 relative overflow-hidden font-sans">
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-brand-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="sm:mx-auto sm:w-full sm:max-w-lg z-10 text-center space-y-2">
        <div className="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-gradient-to-tr from-brand-600 to-indigo-500 shadow-xl shadow-brand-500/25 mb-2">
          <GraduationCap className="w-6 h-6 text-white" />
        </div>
        <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          Join Your <span className="text-brand-400">Campus Cohort</span>
        </h2>
        <p className="text-xs sm:text-sm text-slate-400">
          Create your student account with single-campus trust scope
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-lg z-10 px-4 sm:px-0">
        <Card className="border-slate-800/80 bg-slate-900/80 backdrop-blur-xl shadow-2xl">
          <CardContent className="pt-6">
            <form onSubmit={handleSubmit} className="space-y-4">
              <Input
                label="Full Name"
                placeholder="Nikshith Gurram"
                value={formData.fullName}
                onChange={(e) => {
                  setFormData({ ...formData, fullName: e.target.value });
                  if (errors.fullName) setErrors({ ...errors, fullName: '' });
                }}
                error={errors.fullName}
                leftIcon={<User className="w-4 h-4" />}
                required
              />

              <Input
                label="College Email"
                type="email"
                placeholder="nikshith@apex.edu"
                value={formData.email}
                onChange={(e) => {
                  setFormData({ ...formData, email: e.target.value });
                  if (errors.email) setErrors({ ...errors, email: '' });
                }}
                error={errors.email}
                leftIcon={<Mail className="w-4 h-4" />}
                required
              />

              <Input
                label="Password"
                type="password"
                placeholder="Min 8 chars, 1 uppercase, 1 number"
                value={formData.password}
                onChange={(e) => {
                  setFormData({ ...formData, password: e.target.value });
                  if (errors.password) setErrors({ ...errors, password: '' });
                }}
                error={errors.password}
                helperText="Must be at least 8 characters with upper, lower, and digit."
                leftIcon={<Lock className="w-4 h-4" />}
                required
              />

              <Input
                label="Campus Name"
                placeholder="Apex Institute of Technology"
                value={formData.campusName}
                onChange={(e) => {
                  setFormData({ ...formData, campusName: e.target.value });
                  if (errors.campusName) setErrors({ ...errors, campusName: '' });
                }}
                error={errors.campusName}
                leftIcon={<Building2 className="w-4 h-4" />}
                required
              />

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <label className="block text-xs font-semibold text-slate-300 tracking-wide uppercase">
                    Department
                  </label>
                  <div className="relative">
                    <select
                      value={formData.department}
                      onChange={(e) => setFormData({ ...formData, department: e.target.value })}
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700/80 text-sm text-slate-100 shadow-inner focus:outline-none focus:ring-2 focus:ring-brand-500"
                    >
                      <option value="Computer Science and Engineering">Computer Science (CSE)</option>
                      <option value="Information Technology">Information Technology (IT)</option>
                      <option value="Electronics and Communication">Electronics & Comm (ECE)</option>
                      <option value="Electrical and Electronics">Electrical & Electronics (EEE)</option>
                      <option value="Mechanical Engineering">Mechanical Engineering</option>
                    </select>
                  </div>
                </div>

                <div className="space-y-1.5">
                  <label className="block text-xs font-semibold text-slate-300 tracking-wide uppercase">
                    Academic Year
                  </label>
                  <select
                    value={formData.academicYear}
                    onChange={(e) => setFormData({ ...formData, academicYear: Number(e.target.value) })}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700/80 text-sm text-slate-100 shadow-inner focus:outline-none focus:ring-2 focus:ring-brand-500"
                  >
                    <option value={1}>1st Year (Freshman)</option>
                    <option value={2}>2nd Year (Sophomore)</option>
                    <option value={3}>3rd Year (Pre-Final Year)</option>
                    <option value={4}>4th Year (Final Year / Placement)</option>
                  </select>
                </div>
              </div>

              <Button
                type="submit"
                variant="primary"
                className="w-full mt-4"
                isLoading={isLoading}
                rightIcon={<ArrowRight className="w-4 h-4" />}
              >
                Create Account & Join
              </Button>
            </form>
          </CardContent>
        </Card>

        <p className="mt-6 text-center text-xs text-slate-400">
          Already registered?{' '}
          <Link to="/login" className="font-semibold text-brand-400 hover:text-brand-300 transition-colors">
            Sign in here
          </Link>
        </p>
      </div>
    </div>
  );
};
