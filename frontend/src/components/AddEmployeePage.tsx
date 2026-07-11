import {
  ArrowLeft,
  Briefcase,
  Calendar,
  CheckCircle2,
  ChevronRight,
  DollarSign,
  Mail,
  MapPin,
  Phone,
  Shield,
  Upload,
  User,
} from 'lucide-react';
import { AnimatePresence, motion } from 'framer-motion';
import { useEffect, useMemo, useState } from 'react';
import {
  CreateEmployeePayload,
  Department,
  EmployeeListItem,
  Position,
  createEmployee,
  getDepartments,
  getEmployees,
  getPositions,
} from '../lib/api';
import { cn } from '../lib/utils';

type AddEmployeePageProps = {
  onNavigate: (tab: string) => void;
};

const steps = [
  { label: 'Personal Info', icon: User },
  { label: 'Job Details', icon: Briefcase },
  { label: 'Contact & Address', icon: MapPin },
  { label: 'Management', icon: Shield },
];

const initialForm: CreateEmployeePayload = {
  first_name: '',
  last_name: '',
  work_email: '',
  phone: '',
  department_id: '',
  position_id: '',
  manager_id: '',
  hire_date: '',
  basic_salary: 85000,
  address: '',
  emergency_contact_name: '',
  emergency_contact_phone: '',
};

function FieldShell({
  icon: Icon,
  children,
  hasError = false,
}: {
  icon: typeof User;
  children: React.ReactNode;
  hasError?: boolean;
}) {
  return (
    <div
      className={cn(
        'flex h-14 items-center gap-3 rounded-2xl border px-4 text-slate-400 transition-all duration-200 focus-within:bg-white focus-within:shadow-lg',
        hasError
          ? 'border-rose-200 bg-rose-50 focus-within:border-rose-300 focus-within:shadow-rose-100'
          : 'border-transparent bg-slate-50 focus-within:border-indigo-200 focus-within:shadow-indigo-100',
      )}
    >
      <Icon className="h-5 w-5" />
      {children}
    </div>
  );
}

export default function AddEmployeePage({ onNavigate }: AddEmployeePageProps) {
  const [step, setStep] = useState(0);
  const [form, setForm] = useState<CreateEmployeePayload>(initialForm);
  const [photoPreview, setPhotoPreview] = useState('');
  const [departments, setDepartments] = useState<Department[]>([]);
  const [positions, setPositions] = useState<Position[]>([]);
  const [managers, setManagers] = useState<EmployeeListItem[]>([]);
  const [error, setError] = useState('');
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    void getDepartments().then(setDepartments).catch(() => setDepartments([]));
    void getEmployees({ per_page: 100 }).then((result) => setManagers(result.items)).catch(() => setManagers([]));
  }, []);

  useEffect(() => {
    setForm((current) => ({ ...current, position_id: '' }));
    void getPositions(form.department_id).then(setPositions).catch(() => setPositions([]));
  }, [form.department_id]);

  const selectedDepartment = departments.find((department) => department.id === Number(form.department_id));
  const selectedPosition = positions.find((position) => position.id === Number(form.position_id));

  const fullName = useMemo(
    () => `${form.first_name} ${form.last_name}`.trim() || '-',
    [form.first_name, form.last_name],
  );

  const updateField = (field: keyof CreateEmployeePayload, value: string | number) => {
    setForm((current) => ({ ...current, [field]: value }));
    setFieldErrors((current) => {
      const next = { ...current };
      delete next[field];
      return next;
    });
    setError('');
  };

  const handlePhotoChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setPhotoPreview(URL.createObjectURL(file));
  };

  const validateStep = (targetStep = step) => {
    const errors: Record<string, string> = {};

    if (targetStep === 0) {
      if (!form.first_name.trim()) errors.first_name = 'First name is required.';
      if (!form.last_name.trim()) errors.last_name = 'Last name is required.';
      if (!form.work_email.trim()) errors.work_email = 'Email address is required.';
      if (form.work_email && !form.work_email.includes('@')) errors.work_email = 'Enter a valid email address.';
    }

    if (targetStep === 1) {
      if (!form.department_id) errors.department_id = 'Department is required.';
      if (!form.position_id) errors.position_id = 'Role is required.';
      if (!form.hire_date) errors.hire_date = 'Joining date is required.';
      if (Number(form.basic_salary) < 0) errors.basic_salary = 'Salary cannot be negative.';
    }

    if (targetStep === 2) {
      if (!form.address?.trim()) errors.address = 'Full address is required.';
      if (!form.emergency_contact_name?.trim()) errors.emergency_contact_name = 'Emergency contact is required.';
      if (!form.emergency_contact_phone?.trim()) errors.emergency_contact_phone = 'Emergency phone is required.';
    }

    setFieldErrors(errors);
    if (Object.keys(errors).length > 0) {
      setError('Please complete the required fields before continuing.');
      return false;
    }

    return true;
  };

  const nextStep = () => {
    if (!validateStep()) return;
    setError('');
    setStep((current) => Math.min(current + 1, steps.length - 1));
  };

  const previousStep = () => {
    setError('');
    setStep((current) => Math.max(current - 1, 0));
  };

  const saveEmployee = async () => {
    if (![0, 1, 2].every((stepIndex) => validateStep(stepIndex))) return;
    setIsSaving(true);
    setError('');

    try {
      await createEmployee(form);
      onNavigate('employees');
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to save employee.');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="mx-auto max-w-5xl space-y-8">
      <div className="flex items-start gap-6">
        <button
          onClick={() => onNavigate('employees')}
          className="mt-3 rounded-xl p-2 text-slate-500 transition hover:bg-slate-100 hover:text-slate-900"
        >
          <ArrowLeft className="h-6 w-6" />
        </button>
        <div>
          <h2 className="text-3xl font-bold text-slate-950">Add New Employee</h2>
          <p className="mt-2 text-lg text-slate-500">Fill in the details to onboard a new team member.</p>
        </div>
      </div>

      <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="grid gap-4 md:grid-cols-4">
          {steps.map((item, index) => {
            const Icon = item.icon;
            const isActive = index <= step;
            return (
              <div key={item.label} className="flex items-center gap-4">
                <div className="flex flex-1 flex-col items-center">
                  <motion.div
                    animate={{ scale: isActive ? 1 : 0.94 }}
                    className={cn('flex h-12 w-12 items-center justify-center rounded-xl transition-colors', isActive ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-200' : 'bg-slate-100 text-slate-400')}
                    transition={{ duration: 0.2 }}
                  >
                    <Icon className="h-6 w-6" />
                  </motion.div>
                  <span className={cn('mt-3 text-xs font-bold uppercase tracking-wide', isActive ? 'text-indigo-600' : 'text-slate-400')}>
                    {item.label}
                  </span>
                </div>
                {index < steps.length - 1 && (
                  <div className="hidden h-px flex-1 overflow-hidden bg-slate-200 md:block">
                    <motion.div
                      animate={{ scaleX: index < step ? 1 : 0 }}
                      className="h-full origin-left bg-indigo-600"
                      transition={{ duration: 0.25 }}
                    />
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </section>

      <section className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
        <AnimatePresence mode="wait">
          {step === 0 && (
          <motion.div
            animate={{ opacity: 1, x: 0 }}
            className="space-y-8"
            exit={{ opacity: 0, x: -24 }}
            initial={{ opacity: 0, x: 24 }}
            key="personal"
            transition={{ duration: 0.2 }}
          >
            <label className="mx-auto flex h-32 w-32 cursor-pointer flex-col items-center justify-center overflow-hidden rounded-full border-2 border-dashed border-slate-200 bg-slate-50 text-center text-slate-400 transition hover:border-indigo-300 hover:bg-indigo-50 hover:text-indigo-600">
              {photoPreview ? (
                <img alt="Employee preview" className="h-full w-full object-cover" src={photoPreview} />
              ) : (
                <>
                  <Upload className="h-8 w-8 shrink-0" />
                  <span className="mt-2 max-w-[78px] text-[9px] font-bold uppercase leading-tight">
                    Upload Photo
                  </span>
                  <span className="mt-0.5 text-[8px] font-bold uppercase leading-tight text-slate-300">
                    Optional
                  </span>
                </>
              )}
              <input accept="image/*" className="hidden" onChange={handlePhotoChange} type="file" />
            </label>
            <div className="grid gap-6 md:grid-cols-2">
              <label>
                <span className="text-sm font-bold text-slate-800">First Name</span>
                <FieldShell hasError={Boolean(fieldErrors.first_name)} icon={User}>
                  <input className="h-full flex-1 bg-transparent outline-none" onChange={(event) => updateField('first_name', event.target.value)} placeholder="e.g. John" value={form.first_name} />
                </FieldShell>
                {fieldErrors.first_name && <p className="mt-2 text-xs font-semibold text-rose-600">{fieldErrors.first_name}</p>}
              </label>
              <label>
                <span className="text-sm font-bold text-slate-800">Last Name</span>
                <FieldShell hasError={Boolean(fieldErrors.last_name)} icon={User}>
                  <input className="h-full flex-1 bg-transparent outline-none" onChange={(event) => updateField('last_name', event.target.value)} placeholder="e.g. Doe" value={form.last_name} />
                </FieldShell>
                {fieldErrors.last_name && <p className="mt-2 text-xs font-semibold text-rose-600">{fieldErrors.last_name}</p>}
              </label>
              <label>
                <span className="text-sm font-bold text-slate-800">Email Address</span>
                <FieldShell hasError={Boolean(fieldErrors.work_email)} icon={Mail}>
                  <input className="h-full flex-1 bg-transparent outline-none" onChange={(event) => updateField('work_email', event.target.value)} placeholder="john.doe@company.com" type="email" value={form.work_email} />
                </FieldShell>
                {fieldErrors.work_email && <p className="mt-2 text-xs font-semibold text-rose-600">{fieldErrors.work_email}</p>}
              </label>
              <label>
                <span className="text-sm font-bold text-slate-800">Phone Number <span className="font-medium text-slate-400">(optional)</span></span>
                <FieldShell icon={Phone}>
                  <input className="h-full flex-1 bg-transparent outline-none" onChange={(event) => updateField('phone', event.target.value)} placeholder="+1 (555) 000-0000" value={form.phone} />
                </FieldShell>
              </label>
            </div>
          </motion.div>
        )}

        {step === 1 && (
          <motion.div
            animate={{ opacity: 1, x: 0 }}
            className="grid gap-7 md:grid-cols-2"
            exit={{ opacity: 0, x: -24 }}
            initial={{ opacity: 0, x: 24 }}
            key="job"
            transition={{ duration: 0.2 }}
          >
            <label>
              <span className="text-sm font-bold text-slate-800">Department</span>
              <FieldShell hasError={Boolean(fieldErrors.department_id)} icon={Shield}>
                <select className="h-full flex-1 bg-transparent outline-none" onChange={(event) => updateField('department_id', Number(event.target.value) || '')} value={form.department_id}>
                  <option value="">Select Department</option>
                  {departments.map((department) => <option key={department.id} value={department.id}>{department.name}</option>)}
                </select>
              </FieldShell>
              {fieldErrors.department_id && <p className="mt-2 text-xs font-semibold text-rose-600">{fieldErrors.department_id}</p>}
            </label>
            <label>
              <span className="text-sm font-bold text-slate-800">Role / Designation</span>
              <FieldShell hasError={Boolean(fieldErrors.position_id)} icon={Briefcase}>
                <select className="h-full flex-1 bg-transparent outline-none" onChange={(event) => updateField('position_id', Number(event.target.value) || '')} value={form.position_id}>
                  <option value="">Select Role</option>
                  {positions.map((position) => <option key={position.id} value={position.id}>{position.title}</option>)}
                </select>
              </FieldShell>
              {fieldErrors.position_id && <p className="mt-2 text-xs font-semibold text-rose-600">{fieldErrors.position_id}</p>}
            </label>
            <label>
              <span className="text-sm font-bold text-slate-800">Annual Salary</span>
              <FieldShell hasError={Boolean(fieldErrors.basic_salary)} icon={DollarSign}>
                <input className="h-full flex-1 bg-transparent outline-none" onChange={(event) => updateField('basic_salary', Number(event.target.value))} type="number" value={form.basic_salary} />
              </FieldShell>
              {fieldErrors.basic_salary && <p className="mt-2 text-xs font-semibold text-rose-600">{fieldErrors.basic_salary}</p>}
            </label>
            <label>
              <span className="text-sm font-bold text-slate-800">Joining Date</span>
              <FieldShell hasError={Boolean(fieldErrors.hire_date)} icon={Calendar}>
                <input className="h-full flex-1 bg-transparent outline-none" onChange={(event) => updateField('hire_date', event.target.value)} type="date" value={form.hire_date} />
              </FieldShell>
              {fieldErrors.hire_date && <p className="mt-2 text-xs font-semibold text-rose-600">{fieldErrors.hire_date}</p>}
            </label>
          </motion.div>
        )}

        {step === 2 && (
          <motion.div
            animate={{ opacity: 1, x: 0 }}
            className="grid gap-7 md:grid-cols-2"
            exit={{ opacity: 0, x: -24 }}
            initial={{ opacity: 0, x: 24 }}
            key="contact"
            transition={{ duration: 0.2 }}
          >
            <label className="md:col-span-2">
              <span className="text-sm font-bold text-slate-800">Full Address</span>
              <FieldShell hasError={Boolean(fieldErrors.address)} icon={MapPin}>
                <input className="h-full flex-1 bg-transparent outline-none" onChange={(event) => updateField('address', event.target.value)} placeholder="123 Business Ave, Suite 100" value={form.address} />
              </FieldShell>
              {fieldErrors.address && <p className="mt-2 text-xs font-semibold text-rose-600">{fieldErrors.address}</p>}
            </label>
            <label>
              <span className="text-sm font-bold text-slate-800">City <span className="font-medium text-slate-400">(optional)</span></span>
              <FieldShell icon={MapPin}>
                <input className="h-full flex-1 bg-transparent outline-none" placeholder="e.g. San Francisco" />
              </FieldShell>
            </label>
            <label>
              <span className="text-sm font-bold text-slate-800">Country <span className="font-medium text-slate-400">(optional)</span></span>
              <FieldShell icon={MapPin}>
                <input className="h-full flex-1 bg-transparent outline-none" placeholder="e.g. USA" />
              </FieldShell>
            </label>
            <label>
              <span className="text-sm font-bold text-slate-800">Emergency Contact Name</span>
              <FieldShell hasError={Boolean(fieldErrors.emergency_contact_name)} icon={User}>
                <input className="h-full flex-1 bg-transparent outline-none" onChange={(event) => updateField('emergency_contact_name', event.target.value)} placeholder="Emergency Contact Name" value={form.emergency_contact_name} />
              </FieldShell>
              {fieldErrors.emergency_contact_name && <p className="mt-2 text-xs font-semibold text-rose-600">{fieldErrors.emergency_contact_name}</p>}
            </label>
            <label>
              <span className="text-sm font-bold text-slate-800">Emergency Phone</span>
              <FieldShell hasError={Boolean(fieldErrors.emergency_contact_phone)} icon={Phone}>
                <input className="h-full flex-1 bg-transparent outline-none" onChange={(event) => updateField('emergency_contact_phone', event.target.value)} placeholder="Emergency Phone Number" value={form.emergency_contact_phone} />
              </FieldShell>
              {fieldErrors.emergency_contact_phone && <p className="mt-2 text-xs font-semibold text-rose-600">{fieldErrors.emergency_contact_phone}</p>}
            </label>
          </motion.div>
        )}

        {step === 3 && (
          <motion.div
            animate={{ opacity: 1, x: 0 }}
            className="space-y-7"
            exit={{ opacity: 0, x: -24 }}
            initial={{ opacity: 0, x: 24 }}
            key="management"
            transition={{ duration: 0.2 }}
          >
            <div className="rounded-2xl border border-indigo-100 bg-indigo-50 p-6">
              <div className="flex items-center gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-white text-indigo-600 shadow-sm">
                  <Shield className="h-6 w-6" />
                </div>
                <div>
                  <h3 className="font-bold text-indigo-950">Management Assignment</h3>
                  <p className="mt-1 text-sm text-indigo-600">Assign a reporting manager to oversee this employee's performance and approvals.</p>
                </div>
              </div>
            </div>
            <label>
              <span className="text-sm font-bold text-slate-800">Reporting Manager <span className="font-medium text-slate-400">(optional)</span></span>
              <FieldShell icon={User}>
                <select className="h-full flex-1 bg-transparent outline-none" onChange={(event) => updateField('manager_id', Number(event.target.value) || '')} value={form.manager_id}>
                  <option value="">Select Manager</option>
                  {managers.map((manager) => <option key={manager.id} value={manager.id}>{manager.name}</option>)}
                </select>
              </FieldShell>
            </label>
            <div className="border-t border-slate-100 pt-5">
              <h3 className="text-sm font-bold uppercase tracking-wide text-slate-900">Review Summary</h3>
              <div className="mt-4 grid gap-4 md:grid-cols-2">
                <div className="rounded-2xl bg-slate-50 p-5">
                  <p className="text-xs font-bold uppercase tracking-wide text-slate-400">Full Name</p>
                  <p className="mt-2 font-semibold text-slate-900">{fullName}</p>
                </div>
                <div className="rounded-2xl bg-slate-50 p-5">
                  <p className="text-xs font-bold uppercase tracking-wide text-slate-400">Role & Dept</p>
                  <p className="mt-2 font-semibold text-slate-900">{selectedPosition?.title ?? '-'} / {selectedDepartment?.name ?? '-'}</p>
                </div>
              </div>
            </div>
          </motion.div>
        )}
        </AnimatePresence>

        {error && <div className="mt-6 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">{error}</div>}
      </section>

      <section className="flex items-center justify-between rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <button className="font-bold text-slate-600 disabled:text-slate-300" disabled={step === 0} onClick={previousStep}>
          Previous Step
        </button>
        {step < steps.length - 1 ? (
          <button className="flex h-12 items-center gap-3 rounded-xl bg-indigo-600 px-8 font-bold text-white shadow-lg shadow-indigo-200 transition hover:bg-indigo-700 active:scale-[0.98]" onClick={nextStep}>
            Next Step
            <ChevronRight className="h-5 w-5" />
          </button>
        ) : (
          <button className="flex h-12 items-center gap-3 rounded-xl bg-emerald-600 px-8 font-bold text-white shadow-lg shadow-emerald-200 disabled:bg-emerald-400" disabled={isSaving} onClick={saveEmployee}>
            {isSaving ? 'Saving...' : 'Save Employee'}
            <CheckCircle2 className="h-5 w-5" />
          </button>
        )}
      </section>
    </div>
  );
}
