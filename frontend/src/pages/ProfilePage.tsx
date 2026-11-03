import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import apiClient from '../lib/api';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, Button, Input, Badge, Modal } from '../components/ui';
import { User, Building2, BookOpen, Home, Lock, Save } from 'lucide-react';

export const ProfilePage: React.FC = () => {
  const { user, updateUser } = useAuth();
  const { success: toastSuccess, error: toastError } = useToast();

  const [fullName, setFullName] = useState(user?.full_name || '');
  const [phoneNumber, setPhoneNumber] = useState(user?.phone_number || '');
  const [bio, setBio] = useState(user?.bio || '');
  const [isSaving, setIsSaving] = useState(false);

  // Password change modal state
  const [isPasswordModalOpen, setIsPasswordModalOpen] = useState(false);
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isChangingPassword, setIsChangingPassword] = useState(false);

  const handleSaveProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    try {
      const response = await apiClient.put('/auth/me', {
        full_name: fullName,
        phone_number: phoneNumber,
        bio: bio,
      });
      if (response.data && response.data.data) {
        updateUser(response.data.data);
      }
      toastSuccess('Profile updated successfully!');
    } catch (err: any) {
      toastError(err.message || 'Failed to update profile.');
    } finally {
      setIsSaving(false);
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      toastError('New passwords do not match');
      return;
    }
    if (newPassword.length < 8) {
      toastError('Password must be at least 8 characters');
      return;
    }

    setIsChangingPassword(true);
    try {
      await apiClient.post('/auth/change-password', {
        current_password: currentPassword,
        new_password: newPassword,
      });
      toastSuccess('Password rotated successfully!');
      setIsPasswordModalOpen(false);
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch (err: any) {
      toastError(err.message || 'Failed to change password.');
    } finally {
      setIsChangingPassword(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto animate-in fade-in duration-300">
      {/* 1. Header Card */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-brand-900/40 via-slate-900 to-indigo-950/40 border border-slate-800 shadow-xl backdrop-blur-md">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-brand-600 to-indigo-600 flex items-center justify-center font-bold text-2xl text-white shadow-xl shadow-brand-500/25 shrink-0">
            {user?.full_name ? user.full_name.charAt(0).toUpperCase() : 'U'}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
                {user?.full_name || 'Campus Student'}
              </h1>
              <Badge variant="brand" className="capitalize">
                {user?.role || 'Student'}
              </Badge>
            </div>
            <p className="text-xs sm:text-sm text-slate-400 mt-1">{user?.email}</p>
            <p className="text-xs text-brand-400 font-medium flex items-center gap-1.5 mt-1">
              <Building2 className="w-3.5 h-3.5" />
              <span>{user?.campus_name || 'Apex Institute of Technology'}</span>
            </p>
          </div>
        </div>

        <Button
          variant="outline"
          size="sm"
          leftIcon={<Lock className="w-4 h-4" />}
          onClick={() => setIsPasswordModalOpen(true)}
        >
          Change Password
        </Button>
      </div>

      {/* 2. Editable Profile Form */}
      <form onSubmit={handleSaveProfile}>
        <Card>
          <CardHeader>
            <CardTitle className="text-base flex items-center gap-2">
              <User className="w-4 h-4 text-brand-400" />
              <span>Personal Details</span>
            </CardTitle>
            <CardDescription>Update your public campus profile information</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <Input
                label="Full Name"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                required
              />

              <Input
                label="Phone Number"
                placeholder="+91 9876543210"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
              />
            </div>

            <div className="space-y-1.5">
              <label className="block text-xs font-semibold text-slate-300 tracking-wide uppercase">
                Student Bio
              </label>
              <textarea
                rows={3}
                value={bio}
                onChange={(e) => setBio(e.target.value)}
                placeholder="Aspiring backend engineer passionate about distributed systems and cloud platforms..."
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700/80 text-sm text-slate-100 placeholder:text-slate-500 shadow-inner focus:outline-none focus:ring-2 focus:ring-brand-500"
              />
            </div>

            <div className="flex justify-end pt-2">
              <Button
                type="submit"
                variant="primary"
                isLoading={isSaving}
                leftIcon={<Save className="w-4 h-4" />}
              >
                Save Profile
              </Button>
            </div>
          </CardContent>
        </Card>
      </form>

      {/* 3. Academic Details (Read-only verified) */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <BookOpen className="w-4 h-4 text-indigo-400" />
            <span>Academic Affiliation (Verified)</span>
          </CardTitle>
          <CardDescription>Official institution academic metadata</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-sm">
            <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
              <span className="text-xs text-slate-400 block font-medium">Department</span>
              <span className="font-semibold text-white mt-1 block">
                {user?.profile?.department || 'Computer Science and Engineering'}
              </span>
            </div>

            <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
              <span className="text-xs text-slate-400 block font-medium">Academic Year</span>
              <span className="font-semibold text-white mt-1 block">
                Year {user?.profile?.academic_year || 3} (Pre-Final Year)
              </span>
            </div>

            <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
              <span className="text-xs text-slate-400 block font-medium">Hostel Room</span>
              <span className="font-semibold text-white mt-1 block flex items-center gap-1.5">
                <Home className="w-4 h-4 text-brand-400 inline" />
                {user?.profile?.hostel_block || 'Aryabhatta Block'} - {user?.profile?.room_number || '304'}
              </span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Password Change Modal */}
      <Modal
        isOpen={isPasswordModalOpen}
        onClose={() => setIsPasswordModalOpen(false)}
        title="Change Password"
        description="Verify your current password and choose a strong new password"
      >
        <form onSubmit={handleChangePassword} className="space-y-4">
          <Input
            label="Current Password"
            type="password"
            value={currentPassword}
            onChange={(e) => setCurrentPassword(e.target.value)}
            required
          />

          <Input
            label="New Password"
            type="password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            helperText="Minimum 8 characters with uppercase, lowercase, and digit."
            required
          />

          <Input
            label="Confirm New Password"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />

          <div className="flex justify-end gap-3 pt-3">
            <Button
              type="button"
              variant="outline"
              onClick={() => setIsPasswordModalOpen(false)}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="primary"
              isLoading={isChangingPassword}
            >
              Update Password
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
