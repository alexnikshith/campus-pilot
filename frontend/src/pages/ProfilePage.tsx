import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import profileService from '../services/profileService';
import apiClient from '../lib/api';
import { StudentProfileData, TaxonomyResponse } from '../types';
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  Button,
  Input,
  Badge,
  Modal,
  Tabs,
  Skeleton,
} from '../components/ui';
import { ProfileCompletenessBar } from '../components/profile/ProfileCompletenessBar';
import { OnboardingWizardModal } from '../components/profile/OnboardingWizardModal';
import {
  User,
  Building2,
  BookOpen,
  Home,
  Lock,
  Save,
  Sparkles,
  Target,
  Award,
  Plus,
  X,
} from 'lucide-react';

export const ProfilePage: React.FC = () => {
  const { user, updateUser } = useAuth();
  const { success: toastSuccess, error: toastError } = useToast();

  const [profile, setProfile] = useState<StudentProfileData | null>(null);
  const [taxonomy, setTaxonomy] = useState<TaxonomyResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [activeTab, setActiveTab] = useState<string>('academics');
  const [isWizardOpen, setIsWizardOpen] = useState<boolean>(false);

  // Editable Form State
  const [degree, setDegree] = useState<string>('B.Tech');
  const [branch, setBranch] = useState<string>('Computer Science and Engineering');
  const [graduationYear, setGraduationYear] = useState<number>(2026);
  const [cgpa, setCgpa] = useState<string>('8.50');
  const [skills, setSkills] = useState<string[]>([]);
  const [targetRoles, setTargetRoles] = useState<string[]>([]);
  const [prepHours, setPrepHours] = useState<number>(15);
  const [hostelBlock, setHostelBlock] = useState<string>('Aryabhatta Block');
  const [roomNumber, setRoomNumber] = useState<string>('304');
  const [preferredLocations, setPreferredLocations] = useState<string[]>([]);
  const [newSkillInput, setNewSkillInput] = useState<string>('');
  const [isSaving, setIsSaving] = useState<boolean>(false);

  // User Contact Info
  const [fullName, setFullName] = useState(user?.full_name || '');
  const [phoneNumber, setPhoneNumber] = useState(user?.phone_number || '');
  const [bio, setBio] = useState(user?.bio || '');

  // Password change modal state
  const [isPasswordModalOpen, setIsPasswordModalOpen] = useState(false);
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isChangingPassword, setIsChangingPassword] = useState(false);

  const loadProfile = useCallback(async () => {
    setIsLoading(true);
    try {
      const [profileData, taxData] = await Promise.all([
        profileService.getProfile(),
        profileService.getTaxonomy(),
      ]);
      setProfile(profileData);
      setTaxonomy(taxData);

      // Hydrate state
      setDegree(profileData.degree || 'B.Tech');
      setBranch(profileData.branch || 'Computer Science and Engineering');
      setGraduationYear(profileData.graduation_year || 2026);
      setCgpa(profileData.cgpa !== null ? String(profileData.cgpa) : '');
      setSkills(profileData.skills || []);
      setTargetRoles(profileData.target_roles || []);
      setPrepHours(profileData.prep_hours_week || 15);
      setHostelBlock(profileData.hostel_block || 'Aryabhatta Block');
      setRoomNumber(profileData.room_number || '');
      setPreferredLocations(profileData.preferred_locations || []);
      setFullName(profileData.user.full_name || '');
      setPhoneNumber(profileData.user.phone_number || '');
      setBio(profileData.user.bio || '');
    } catch {
      toastError('Could not load academic profile details.');
    } finally {
      setIsLoading(false);
    }
  }, [toastError]);

  useEffect(() => {
    loadProfile();
  }, [loadProfile]);

  const handleSaveProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    try {
      const cgpaNum = cgpa ? Number(cgpa) : null;
      if (cgpaNum !== null && (isNaN(cgpaNum) || cgpaNum < 0 || cgpaNum > 10)) {
        toastError('CGPA must be a valid number between 0.00 and 10.00.');
        setIsSaving(false);
        return;
      }

      const updated = await profileService.updateProfile({
        degree,
        branch,
        graduation_year: graduationYear,
        cgpa: cgpaNum,
        skills,
        target_roles: targetRoles,
        prep_hours_week: prepHours,
        hostel_block: hostelBlock,
        room_number: roomNumber,
        preferred_locations: preferredLocations,
        phone_number: phoneNumber,
        bio,
      });

      setProfile(updated);
      updateUser({
        full_name: fullName,
        phone_number: phoneNumber,
        bio,
      });

      toastSuccess('Academic profile and preferences updated successfully!');
    } catch (err: any) {
      toastError(err.message || 'Failed to update student profile.');
    } finally {
      setIsSaving(false);
    }
  };

  const addSkill = (e: React.FormEvent) => {
    e.preventDefault();
    const clean = newSkillInput.trim();
    if (clean && !skills.includes(clean)) {
      setSkills((prev) => [...prev, clean]);
      setNewSkillInput('');
    }
  };

  const removeSkill = (skillToRemove: string) => {
    setSkills((prev) => prev.filter((s) => s !== skillToRemove));
  };

  const toggleTargetRole = (role: string) => {
    setTargetRoles((prev) =>
      prev.includes(role) ? prev.filter((r) => r !== role) : [...prev, role]
    );
  };

  const toggleLocation = (loc: string) => {
    setPreferredLocations((prev) =>
      prev.includes(loc) ? prev.filter((l) => l !== loc) : [...prev, loc]
    );
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

  const tabs = [
    { id: 'academics', label: 'Academics & CGPA', icon: <BookOpen className="w-4 h-4" /> },
    { id: 'placement', label: 'Placement & Skills', icon: <Target className="w-4 h-4" />, badge: skills.length },
    { id: 'living', label: 'Campus & Hostel', icon: <Home className="w-4 h-4" /> },
    { id: 'account', label: 'Account & Security', icon: <User className="w-4 h-4" /> },
  ];

  return (
    <div className="space-y-6 max-w-5xl mx-auto animate-in fade-in duration-300">
      {/* 1. Header Card */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-6 rounded-3xl bg-gradient-to-r from-brand-900/50 via-slate-900 to-indigo-950/50 border border-slate-800 shadow-2xl backdrop-blur-md">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-brand-600 to-indigo-600 flex items-center justify-center font-bold text-2xl text-white shadow-xl shadow-brand-500/25 shrink-0">
            {profile?.user.full_name ? profile.user.full_name.charAt(0).toUpperCase() : 'U'}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
                {profile?.user.full_name || 'Campus Student'}
              </h1>
              <Badge variant="brand" className="capitalize">
                {profile?.user.role || 'Student'}
              </Badge>
              {profile?.cgpa && (
                <Badge variant="success">
                  <Award className="w-3 h-3 mr-1 inline" />
                  CGPA {profile.cgpa}
                </Badge>
              )}
            </div>
            <p className="text-xs sm:text-sm text-slate-400 mt-0.5">{profile?.user.email}</p>
            <p className="text-xs text-brand-400 font-medium flex items-center gap-1.5 mt-1">
              <Building2 className="w-3.5 h-3.5" />
              <span>{profile?.user.campus_name || 'Apex Institute of Technology'}</span>
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant="primary"
            size="sm"
            onClick={() => setIsWizardOpen(true)}
            leftIcon={<Sparkles className="w-4 h-4" />}
          >
            Launch Onboarding Wizard
          </Button>
          <Button
            variant="outline"
            size="sm"
            leftIcon={<Lock className="w-4 h-4" />}
            onClick={() => setIsPasswordModalOpen(true)}
          >
            Password
          </Button>
        </div>
      </div>

      {/* 2. Profile Completeness Bar */}
      {profile && (
        <ProfileCompletenessBar
          completeness={profile.completeness}
          onOpenWizard={() => setIsWizardOpen(true)}
        />
      )}

      {/* 3. Tab Switcher */}
      <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} />

      {/* 4. Tab Content Body */}
      {isLoading ? (
        <div className="space-y-4">
          <Skeleton className="h-64 w-full rounded-2xl" />
        </div>
      ) : (
        <form onSubmit={handleSaveProfile} className="space-y-6">
          {/* TAB 1: ACADEMICS */}
          {activeTab === 'academics' && (
            <Card className="animate-in fade-in duration-150">
              <CardHeader>
                <CardTitle className="text-base flex items-center gap-2">
                  <BookOpen className="w-4 h-4 text-brand-400" />
                  <span>Academic Credentials & Performance</span>
                </CardTitle>
                <CardDescription>
                  Keep your academic information accurate for placement eligibility criteria.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <label className="block text-xs font-semibold text-slate-300 uppercase">
                      Degree
                    </label>
                    <select
                      value={degree}
                      onChange={(e) => setDegree(e.target.value)}
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700/80 text-sm text-slate-100 focus:outline-none focus:ring-2 focus:ring-brand-500"
                    >
                      {(taxonomy?.degrees || ['B.Tech', 'B.E.', 'M.Tech', 'BCA', 'MCA']).map((deg) => (
                        <option key={deg} value={deg}>
                          {deg}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="space-y-1.5">
                    <label className="block text-xs font-semibold text-slate-300 uppercase">
                      Graduation Year
                    </label>
                    <select
                      value={graduationYear}
                      onChange={(e) => setGraduationYear(Number(e.target.value))}
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700/80 text-sm text-slate-100 focus:outline-none focus:ring-2 focus:ring-brand-500"
                    >
                      {[2024, 2025, 2026, 2027, 2028, 2029].map((yr) => (
                        <option key={yr} value={yr}>
                          Class of {yr}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="space-y-1.5">
                  <label className="block text-xs font-semibold text-slate-300 uppercase">
                    Engineering Department / Branch
                  </label>
                  <select
                    value={branch}
                    onChange={(e) => setBranch(e.target.value)}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700/80 text-sm text-slate-100 focus:outline-none focus:ring-2 focus:ring-brand-500"
                  >
                    {(
                      taxonomy?.branches || [
                        'Computer Science and Engineering',
                        'Information Technology',
                        'Artificial Intelligence and Data Science',
                        'Electronics and Communication Engineering',
                        'Electrical and Electronics Engineering',
                        'Mechanical Engineering',
                      ]
                    ).map((br) => (
                      <option key={br} value={br}>
                        {br}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="w-full sm:w-1/2">
                  <Input
                    label="Cumulative CGPA (out of 10.00)"
                    type="number"
                    step="0.01"
                    min="0"
                    max="10"
                    placeholder="8.50"
                    value={cgpa}
                    onChange={(e) => setCgpa(e.target.value)}
                    helperText="Crucial for company placement cutoffs and shortlisting algorithms."
                  />
                </div>
              </CardContent>
            </Card>
          )}

          {/* TAB 2: PLACEMENT & SKILLS */}
          {activeTab === 'placement' && (
            <Card className="animate-in fade-in duration-150">
              <CardHeader>
                <CardTitle className="text-base flex items-center gap-2">
                  <Target className="w-4 h-4 text-brand-400" />
                  <span>Target Roles & Technical Skills</span>
                </CardTitle>
                <CardDescription>
                  Tailor your diagnostic study roadmaps by selecting your target roles and capabilities.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Target Roles Multi-Select */}
                <div className="space-y-2">
                  <label className="block text-xs font-semibold text-slate-300 uppercase">
                    Desired Placement Roles
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {(
                      taxonomy?.target_roles || [
                        'Software Development Engineer (SDE)',
                        'Backend Developer',
                        'Frontend Developer',
                        'Full-Stack Developer',
                        'Data Analyst / Data Engineer',
                        'AI / ML Engineer',
                        'Cloud & DevOps Engineer',
                      ]
                    ).map((role) => {
                      const isSelected = targetRoles.includes(role);
                      return (
                        <button
                          key={role}
                          type="button"
                          onClick={() => toggleTargetRole(role)}
                          className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all select-none cursor-pointer border ${
                            isSelected
                              ? 'bg-brand-600 text-white border-brand-500 shadow-md shadow-brand-500/20'
                              : 'bg-slate-900 text-slate-300 border-slate-700/80 hover:bg-slate-800'
                          }`}
                        >
                          {isSelected && '✓ '}
                          {role}
                        </button>
                      );
                    })}
                  </div>
                </div>

                {/* Skills Inventory */}
                <div className="space-y-3">
                  <label className="block text-xs font-semibold text-slate-300 uppercase">
                    Technical Skills Inventory ({skills.length} active)
                  </label>

                  <div className="flex gap-2">
                    <Input
                      placeholder="Add custom skill (e.g. Docker, GraphQL, Kubernetes)..."
                      value={newSkillInput}
                      onChange={(e) => setNewSkillInput(e.target.value)}
                    />
                    <Button type="button" variant="secondary" size="md" onClick={addSkill}>
                      <Plus className="w-4 h-4" />
                    </Button>
                  </div>

                  <div className="p-3 rounded-2xl bg-slate-950/60 border border-slate-800/80 min-h-[52px] flex flex-wrap gap-1.5 items-center">
                    {skills.length === 0 ? (
                      <span className="text-xs text-slate-500">No skills added yet.</span>
                    ) : (
                      skills.map((skill) => (
                        <span
                          key={skill}
                          className="inline-flex items-center gap-1.5 px-3 py-1 rounded-xl text-xs font-semibold bg-brand-500/15 text-brand-300 border border-brand-500/30"
                        >
                          <span>{skill}</span>
                          <button
                            type="button"
                            onClick={() => removeSkill(skill)}
                            className="text-brand-400 hover:text-white"
                            aria-label={`Remove ${skill}`}
                          >
                            <X className="w-3 h-3" />
                          </button>
                        </span>
                      ))
                    )}
                  </div>
                </div>

                {/* Weekly Prep Commitment */}
                <div className="space-y-2 pt-2">
                  <label className="block text-xs font-semibold text-slate-300 uppercase flex items-center justify-between">
                    <span>Weekly Placement Prep Goal</span>
                    <span className="text-brand-400 font-bold">{prepHours} Hours / Week</span>
                  </label>
                  <input
                    type="range"
                    min="5"
                    max="40"
                    step="5"
                    value={prepHours}
                    onChange={(e) => setPrepHours(Number(e.target.value))}
                    className="w-full accent-brand-500 cursor-pointer"
                  />
                  <div className="flex justify-between text-[11px] text-slate-400">
                    <span>5 hrs (Casual)</span>
                    <span>15-20 hrs (Target)</span>
                    <span>40 hrs (Intensive)</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* TAB 3: LIVING & CAMPUS */}
          {activeTab === 'living' && (
            <Card className="animate-in fade-in duration-150">
              <CardHeader>
                <CardTitle className="text-base flex items-center gap-2">
                  <Home className="w-4 h-4 text-brand-400" />
                  <span>Campus Residency & Job Location Preferences</span>
                </CardTitle>
                <CardDescription>
                  Hostel room details ensure seamless facility grievance routing and single-campus peer exchange.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <label className="block text-xs font-semibold text-slate-300 uppercase">
                      Hostel Block
                    </label>
                    <select
                      value={hostelBlock}
                      onChange={(e) => setHostelBlock(e.target.value)}
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700/80 text-sm text-slate-100 focus:outline-none focus:ring-2 focus:ring-brand-500"
                    >
                      {(
                        taxonomy?.hostel_blocks || [
                          'Aryabhatta Block',
                          'Bhaskara Block',
                          'Visvesvaraya Block',
                          'Ramanujan Block',
                          'Kalam Block',
                          'Gargi Hall (Girls)',
                          'Maitreyi Hall (Girls)',
                          'Day Scholar / Off-Campus',
                        ]
                      ).map((b) => (
                        <option key={b} value={b}>
                          {b}
                        </option>
                      ))}
                    </select>
                  </div>

                  <Input
                    label="Hostel Room Number"
                    placeholder="304"
                    value={roomNumber}
                    onChange={(e) => setRoomNumber(e.target.value)}
                  />
                </div>

                <div className="space-y-1.5 pt-2">
                  <label className="block text-xs font-semibold text-slate-300 uppercase">
                    Preferred Placement Locations
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {(
                      taxonomy?.preferred_locations || [
                        'Bangalore',
                        'Hyderabad',
                        'Pune',
                        'Delhi NCR / Gurgaon',
                        'Mumbai',
                        'Chennai',
                        'Remote',
                      ]
                    ).map((loc) => {
                      const isSelected = preferredLocations.includes(loc);
                      return (
                        <button
                          key={loc}
                          type="button"
                          onClick={() => toggleLocation(loc)}
                          className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all select-none cursor-pointer border ${
                            isSelected
                              ? 'bg-brand-600 text-white border-brand-500'
                              : 'bg-slate-900 text-slate-300 border-slate-700/80 hover:bg-slate-800'
                          }`}
                        >
                          {isSelected && '✓ '}
                          {loc}
                        </button>
                      );
                    })}
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* TAB 4: ACCOUNT & SECURITY */}
          {activeTab === 'account' && (
            <Card className="animate-in fade-in duration-150">
              <CardHeader>
                <CardTitle className="text-base flex items-center gap-2">
                  <User className="w-4 h-4 text-brand-400" />
                  <span>Personal Contact Information</span>
                </CardTitle>
                <CardDescription>
                  Update your contact details and public headline visible across campus clubs and matchmaking.
                </CardDescription>
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
                  <label className="block text-xs font-semibold text-slate-300 uppercase">
                    Student Headline / Bio
                  </label>
                  <textarea
                    rows={3}
                    value={bio}
                    onChange={(e) => setBio(e.target.value)}
                    placeholder="Aspiring backend engineer passionate about high-concurrency systems..."
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700/80 text-sm text-slate-100 placeholder:text-slate-500 shadow-inner focus:outline-none focus:ring-2 focus:ring-brand-500"
                  />
                </div>
              </CardContent>
            </Card>
          )}

          {/* Sticky Bottom Save Action */}
          <div className="flex items-center justify-end gap-3 pt-2">
            <Button
              type="submit"
              variant="primary"
              isLoading={isSaving}
              leftIcon={<Save className="w-4 h-4" />}
            >
              Save Profile Changes
            </Button>
          </div>
        </form>
      )}

      {/* Onboarding Wizard Modal */}
      {profile && (
        <OnboardingWizardModal
          isOpen={isWizardOpen}
          onClose={() => setIsWizardOpen(false)}
          onComplete={loadProfile}
          initialData={{
            degree: profile.degree,
            branch: profile.branch,
            graduation_year: profile.graduation_year,
            cgpa: profile.cgpa,
            skills: profile.skills,
            target_roles: profile.target_roles,
            prep_hours_week: profile.prep_hours_week,
            hostel_block: profile.hostel_block,
            room_number: profile.room_number,
            preferred_locations: profile.preferred_locations,
            phone_number: profile.user.phone_number,
            bio: profile.user.bio,
          }}
        />
      )}

      {/* Password Change Modal */}
      <Modal
        isOpen={isPasswordModalOpen}
        onClose={() => setIsPasswordModalOpen(false)}
        title="Change Account Password"
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
