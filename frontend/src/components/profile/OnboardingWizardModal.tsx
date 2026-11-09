import React, { useState, useEffect } from 'react';
import { Modal, Button, Input } from '../ui';
import { TaxonomyResponse, OnboardingPayload } from '../../types';
import profileService from '../../services/profileService';
import { useToast } from '../../context/ToastContext';
import {
  GraduationCap,
  Target,
  Code2,
  Building2,
  Check,
  Plus,
  X,
  ArrowRight,
  ArrowLeft,
  Sparkles,
} from 'lucide-react';

interface OnboardingWizardModalProps {
  isOpen: boolean;
  onClose: () => void;
  onComplete: () => void;
  initialData?: Partial<OnboardingPayload>;
}

export const OnboardingWizardModal: React.FC<OnboardingWizardModalProps> = ({
  isOpen,
  onClose,
  onComplete,
  initialData,
}) => {
  const { success: toastSuccess, error: toastError } = useToast();

  const [currentStep, setCurrentStep] = useState<number>(1);
  const [taxonomy, setTaxonomy] = useState<TaxonomyResponse | null>(null);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [customSkillInput, setCustomSkillInput] = useState<string>('');

  // Form state
  const [formData, setFormData] = useState<OnboardingPayload>({
    degree: initialData?.degree || 'B.Tech',
    branch: initialData?.branch || 'Computer Science and Engineering',
    graduation_year: initialData?.graduation_year || 2026,
    cgpa: initialData?.cgpa ?? 8.5,
    target_roles: initialData?.target_roles || ['Software Development Engineer (SDE)'],
    skills: initialData?.skills || ['Python', 'Data Structures & Algorithms', 'PostgreSQL'],
    preferred_locations: initialData?.preferred_locations || ['Bangalore', 'Hyderabad'],
    prep_hours_week: initialData?.prep_hours_week || 15,
    hostel_block: initialData?.hostel_block || 'Aryabhatta Block',
    room_number: initialData?.room_number || '304',
    phone_number: initialData?.phone_number || '',
    bio: initialData?.bio || '',
  });

  useEffect(() => {
    if (isOpen) {
      profileService
        .getTaxonomy()
        .then(setTaxonomy)
        .catch(() => {
          // Fallback taxonomy if network fails
        });
    }
  }, [isOpen]);

  const toggleTargetRole = (role: string) => {
    setFormData((prev) => {
      const exists = prev.target_roles.includes(role);
      const updated = exists
        ? prev.target_roles.filter((r) => r !== role)
        : [...prev.target_roles, role];
      return { ...prev, target_roles: updated };
    });
  };

  const toggleSkill = (skill: string) => {
    setFormData((prev) => {
      const exists = prev.skills.includes(skill);
      const updated = exists
        ? prev.skills.filter((s) => s !== skill)
        : [...prev.skills, skill];
      return { ...prev, skills: updated };
    });
  };

  const addCustomSkill = (e: React.FormEvent) => {
    e.preventDefault();
    const clean = customSkillInput.trim();
    if (clean && !formData.skills.includes(clean)) {
      setFormData((prev) => ({ ...prev, skills: [...prev.skills, clean] }));
      setCustomSkillInput('');
    }
  };

  const toggleLocation = (loc: string) => {
    setFormData((prev) => {
      const current = prev.preferred_locations || [];
      const exists = current.includes(loc);
      const updated = exists ? current.filter((l) => l !== loc) : [...current, loc];
      return { ...prev, preferred_locations: updated };
    });
  };

  const validateStep = (step: number): boolean => {
    if (step === 1) {
      if (!formData.degree || !formData.branch) {
        toastError('Please select your degree and engineering branch.');
        return false;
      }
      if (formData.cgpa !== null && formData.cgpa !== undefined) {
        const val = Number(formData.cgpa);
        if (isNaN(val) || val < 0 || val > 10) {
          toastError('CGPA must be between 0.00 and 10.00.');
          return false;
        }
      }
    } else if (step === 2) {
      if (formData.target_roles.length === 0) {
        toastError('Please select at least one target placement role.');
        return false;
      }
    } else if (step === 3) {
      if (formData.skills.length === 0) {
        toastError('Please add at least one technical skill.');
        return false;
      }
    }
    return true;
  };

  const handleNext = () => {
    if (validateStep(currentStep)) {
      setCurrentStep((prev) => Math.min(4, prev + 1));
    }
  };

  const handleBack = () => {
    setCurrentStep((prev) => Math.max(1, prev - 1));
  };

  const handleSubmit = async () => {
    if (!validateStep(4)) return;

    setIsSubmitting(true);
    try {
      await profileService.completeOnboarding(formData);
      toastSuccess('Student profile verified and saved successfully!');
      onComplete();
      onClose();
    } catch (err: any) {
      toastError(err.message || 'Failed to save student profile.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const steps = [
    { num: 1, label: 'Academics', icon: GraduationCap },
    { num: 2, label: 'Target Roles', icon: Target },
    { num: 3, label: 'Skills', icon: Code2 },
    { num: 4, label: 'Campus & Living', icon: Building2 },
  ];

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      size="lg"
      title="Student Placement Onboarding Wizard"
      description="Setup your verified academic credentials and placement preferences."
    >
      <div className="space-y-6">
        {/* Step Indicator Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          {steps.map((st) => {
            const isDone = st.num < currentStep;
            const isCurr = st.num === currentStep;
            return (
              <div key={st.num} className="flex items-center gap-2">
                <div
                  className={`w-8 h-8 rounded-xl flex items-center justify-center text-xs font-bold transition-all ${
                    isDone
                      ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                      : isCurr
                      ? 'bg-brand-600 text-white shadow-lg shadow-brand-500/25 ring-2 ring-brand-400/50'
                      : 'bg-slate-800 text-slate-400'
                  }`}
                >
                  {isDone ? <Check className="w-4 h-4" /> : st.num}
                </div>
                <span
                  className={`hidden sm:inline text-xs font-semibold ${
                    isCurr ? 'text-white' : 'text-slate-400'
                  }`}
                >
                  {st.label}
                </span>
              </div>
            );
          })}
        </div>

        {/* STEP 1: Academic Credentials */}
        {currentStep === 1 && (
          <div className="space-y-4 animate-in fade-in duration-200">
            <h4 className="text-sm font-bold text-white flex items-center gap-2">
              <GraduationCap className="w-4 h-4 text-brand-400" />
              <span>Academic Background</span>
            </h4>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="block text-xs font-semibold text-slate-300 uppercase">
                  Degree
                </label>
                <select
                  value={formData.degree}
                  onChange={(e) => setFormData({ ...formData, degree: e.target.value })}
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
                  value={formData.graduation_year}
                  onChange={(e) =>
                    setFormData({ ...formData, graduation_year: Number(e.target.value) })
                  }
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700/80 text-sm text-slate-100 focus:outline-none focus:ring-2 focus:ring-brand-500"
                >
                  {[2024, 2025, 2026, 2027, 2028].map((yr) => (
                    <option key={yr} value={yr}>
                      Class of {yr}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="space-y-1.5">
              <label className="block text-xs font-semibold text-slate-300 uppercase">
                Engineering Branch / Department
              </label>
              <select
                value={formData.branch}
                onChange={(e) => setFormData({ ...formData, branch: e.target.value })}
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
                value={formData.cgpa !== null && formData.cgpa !== undefined ? formData.cgpa : ''}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    cgpa: e.target.value ? Number(e.target.value) : null,
                  })
                }
                helperText="Used for automated campus placement eligibility filtering."
              />
            </div>
          </div>
        )}

        {/* STEP 2: Placement Targets */}
        {currentStep === 2 && (
          <div className="space-y-4 animate-in fade-in duration-200">
            <h4 className="text-sm font-bold text-white flex items-center gap-2">
              <Target className="w-4 h-4 text-brand-400" />
              <span>Target Engineering Roles (Select at least 1)</span>
            </h4>

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
                  'QA / Test Automation Engineer',
                ]
              ).map((role) => {
                const selected = formData.target_roles.includes(role);
                return (
                  <button
                    key={role}
                    type="button"
                    onClick={() => toggleTargetRole(role)}
                    className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all select-none cursor-pointer border ${
                      selected
                        ? 'bg-brand-600 text-white border-brand-500 shadow-md shadow-brand-500/20'
                        : 'bg-slate-900 text-slate-300 border-slate-700/80 hover:border-slate-600 hover:bg-slate-800'
                    }`}
                  >
                    {selected && <Check className="w-3.5 h-3.5 inline mr-1" />}
                    {role}
                  </button>
                );
              })}
            </div>

            <div className="pt-3 space-y-2">
              <label className="block text-xs font-semibold text-slate-300 uppercase">
                Weekly Placement Prep Commitment: {formData.prep_hours_week} hours/week
              </label>
              <input
                type="range"
                min="5"
                max="40"
                step="5"
                value={formData.prep_hours_week}
                onChange={(e) =>
                  setFormData({ ...formData, prep_hours_week: Number(e.target.value) })
                }
                className="w-full accent-brand-500 cursor-pointer"
              />
              <div className="flex justify-between text-[11px] text-slate-400">
                <span>5 hrs (Casual)</span>
                <span>15-20 hrs (Recommended)</span>
                <span>40 hrs (Intensive)</span>
              </div>
            </div>
          </div>
        )}

        {/* STEP 3: Skills Inventory */}
        {currentStep === 3 && (
          <div className="space-y-4 animate-in fade-in duration-200">
            <h4 className="text-sm font-bold text-white flex items-center gap-2">
              <Code2 className="w-4 h-4 text-brand-400" />
              <span>Technical Skills Inventory (Selected: {formData.skills.length})</span>
            </h4>

            {/* Custom Skill Input */}
            <form onSubmit={addCustomSkill} className="flex gap-2">
              <Input
                placeholder="Add custom skill (e.g. Redis, Rust, GraphQL)..."
                value={customSkillInput}
                onChange={(e) => setCustomSkillInput(e.target.value)}
              />
              <Button type="submit" variant="secondary" size="md" leftIcon={<Plus className="w-4 h-4" />}>
                Add
              </Button>
            </form>

            {/* Active Selected Skills Chips */}
            <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 min-h-[48px] flex flex-wrap gap-1.5 items-center">
              {formData.skills.length === 0 ? (
                <span className="text-xs text-slate-500">No skills selected yet. Tap chips below to add.</span>
              ) : (
                formData.skills.map((skill) => (
                  <span
                    key={skill}
                    className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold bg-brand-500/15 text-brand-300 border border-brand-500/30"
                  >
                    <span>{skill}</span>
                    <button
                      type="button"
                      onClick={() => toggleSkill(skill)}
                      className="text-brand-400 hover:text-white"
                      aria-label={`Remove ${skill}`}
                    >
                      <X className="w-3 h-3" />
                    </button>
                  </span>
                ))
              )}
            </div>

            {/* Taxonomy Categorized Skill Chips */}
            <div className="space-y-3 max-h-48 overflow-y-auto pr-1">
              {(taxonomy?.skills_by_category || []).map((cat) => (
                <div key={cat.category} className="space-y-1.5">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block">
                    {cat.category}
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {cat.items.map((skill) => {
                      const selected = formData.skills.includes(skill);
                      return (
                        <button
                          key={skill}
                          type="button"
                          onClick={() => toggleSkill(skill)}
                          className={`px-2.5 py-1 rounded-lg text-xs font-medium transition-all select-none cursor-pointer border ${
                            selected
                              ? 'bg-brand-600 text-white border-brand-500 shadow-sm'
                              : 'bg-slate-900 text-slate-300 border-slate-700/60 hover:bg-slate-800'
                          }`}
                        >
                          {selected ? <Check className="w-3 h-3 inline mr-1" /> : <Plus className="w-3 h-3 inline mr-1 text-slate-400" />}
                          {skill}
                        </button>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* STEP 4: Campus & Living Details */}
        {currentStep === 4 && (
          <div className="space-y-4 animate-in fade-in duration-200">
            <h4 className="text-sm font-bold text-white flex items-center gap-2">
              <Building2 className="w-4 h-4 text-brand-400" />
              <span>Campus Hostel & Preferences</span>
            </h4>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="block text-xs font-semibold text-slate-300 uppercase">
                  Hostel Block
                </label>
                <select
                  value={formData.hostel_block || ''}
                  onChange={(e) => setFormData({ ...formData, hostel_block: e.target.value })}
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
                  ).map((block) => (
                    <option key={block} value={block}>
                      {block}
                    </option>
                  ))}
                </select>
              </div>

              <Input
                label="Room Number"
                placeholder="e.g. 304"
                value={formData.room_number || ''}
                onChange={(e) => setFormData({ ...formData, room_number: e.target.value })}
              />
            </div>

            {/* Preferred Locations */}
            <div className="space-y-1.5 pt-1">
              <label className="block text-xs font-semibold text-slate-300 uppercase">
                Preferred Job Locations
              </label>
              <div className="flex flex-wrap gap-1.5">
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
                  const selected = (formData.preferred_locations || []).includes(loc);
                  return (
                    <button
                      key={loc}
                      type="button"
                      onClick={() => toggleLocation(loc)}
                      className={`px-2.5 py-1 rounded-lg text-xs font-medium transition-all select-none cursor-pointer border ${
                        selected
                          ? 'bg-brand-600 text-white border-brand-500'
                          : 'bg-slate-900 text-slate-300 border-slate-700/60 hover:bg-slate-800'
                      }`}
                    >
                      {loc}
                    </button>
                  );
                })}
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-1">
              <Input
                label="Contact Phone Number"
                placeholder="+91 9876543210"
                value={formData.phone_number || ''}
                onChange={(e) => setFormData({ ...formData, phone_number: e.target.value })}
              />
              <Input
                label="Short Bio / Headline"
                placeholder="Aspiring backend engineer..."
                value={formData.bio || ''}
                onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
              />
            </div>
          </div>
        )}

        {/* Footer Navigation Buttons */}
        <div className="flex items-center justify-between pt-4 border-t border-slate-800">
          <Button
            type="button"
            variant="ghost"
            size="sm"
            onClick={currentStep === 1 ? onClose : handleBack}
            leftIcon={currentStep > 1 ? <ArrowLeft className="w-4 h-4" /> : undefined}
          >
            {currentStep === 1 ? 'Cancel' : 'Back'}
          </Button>

          {currentStep < 4 ? (
            <Button
              type="button"
              variant="primary"
              size="sm"
              onClick={handleNext}
              rightIcon={<ArrowRight className="w-4 h-4" />}
            >
              Continue
            </Button>
          ) : (
            <Button
              type="button"
              variant="primary"
              size="sm"
              onClick={handleSubmit}
              isLoading={isSubmitting}
              leftIcon={<Sparkles className="w-4 h-4" />}
            >
              Complete Onboarding
            </Button>
          )}
        </div>
      </div>
    </Modal>
  );
};
