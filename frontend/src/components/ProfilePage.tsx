import {
  Briefcase,
  Calendar,
  Contact,
  CreditCard,
  FileText,
  GraduationCap,
  HeartPulse,
  Shield,
  Star,
  User,
  Users,
} from 'lucide-react';
import { AuthUser } from '../lib/api';
import { cn } from '../lib/utils';

type ProfilePageProps = {
  user: AuthUser | null;
};

const quickActions = [
  { label: 'Employee Info', icon: User, color: 'bg-blue-500' },
  { label: 'Status', icon: HeartPulse, color: 'bg-emerald-500' },
  { label: 'Bank Info', icon: CreditCard, color: 'bg-violet-500' },
  { label: 'Family', icon: Users, color: 'bg-pink-500' },
  { label: 'Education', icon: GraduationCap, color: 'bg-indigo-500' },
  { label: 'Employment', icon: Briefcase, color: 'bg-orange-500' },
  { label: 'Contact', icon: Contact, color: 'bg-teal-500' },
  { label: 'Supervisor', icon: User, color: 'bg-sky-500' },
  { label: 'Document & Passport', icon: FileText, color: 'bg-rose-500' },
  { label: 'Payroll', icon: CreditCard, color: 'bg-green-600' },
  { label: 'Performance', icon: Star, color: 'bg-indigo-600' },
  { label: 'Security', icon: Shield, color: 'bg-slate-900' },
];

function initialsFor(name: string) {
  return name
    .split(' ')
    .map((part) => part[0])
    .join('')
    .slice(0, 2)
    .toUpperCase();
}

function EmptyPanel({ title }: { title: string }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <h3 className="text-xl font-bold text-slate-950">{title}</h3>
      <div className="mt-6 rounded-2xl border border-dashed border-slate-200 p-8 text-center text-sm font-semibold text-slate-400">
        No data yet.
      </div>
    </div>
  );
}

export default function ProfilePage({ user }: ProfilePageProps) {
  const displayName = user?.name ?? 'User';
  const role = user?.role ?? 'User';
  const initials = initialsFor(displayName) || 'US';

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <div className="flex items-center gap-3 text-sm font-medium text-slate-500">
        <span>Employees</span>
        <span>/</span>
        <span>Employee Profile</span>
        <span>/</span>
        <span className="font-bold text-indigo-600">{displayName}</span>
      </div>

      <section className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <div className="flex flex-col gap-6 md:flex-row md:items-center">
          <div className="flex h-24 w-24 shrink-0 items-center justify-center rounded-full bg-indigo-600 text-3xl font-bold text-white shadow-xl shadow-indigo-200">
            {initials}
          </div>
          <div className="flex-1">
            <div className="flex flex-wrap items-center gap-3">
              <h2 className="text-3xl font-bold text-slate-950">{displayName}</h2>
              <span className="rounded-full bg-indigo-600 px-4 py-1 text-xs font-bold text-white">Active User</span>
            </div>
            <div className="mt-5 grid gap-4 text-sm font-medium text-slate-500 md:grid-cols-4">
              <span>{role}</span>
              <span>{user?.email ?? 'No email'}</span>
              <span>Joined: Not available</span>
              <span>User ID: {user?.id ?? '-'}</span>
            </div>
          </div>
        </div>
      </section>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        {[
          { title: 'Leave Balance', value: 'No data', note: 'Connect leave records', icon: Calendar, color: 'bg-emerald-500', noteColor: 'text-slate-400' },
          { title: 'Attendance', value: 'No data', note: 'Connect attendance', icon: HeartPulse, color: 'bg-blue-500', noteColor: 'text-slate-400' },
          { title: 'Current Salary', value: 'No data', note: 'Connect payroll', icon: CreditCard, color: 'bg-violet-500', noteColor: 'text-slate-400' },
          { title: 'Performance', value: 'No data', note: 'Connect reviews', icon: Star, color: 'bg-orange-500', noteColor: 'text-slate-400' },
        ].map((card) => {
          const Icon = card.icon;
          return (
            <div key={card.title} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs font-bold uppercase tracking-wide text-slate-400">{card.title}</p>
                  <h3 className="mt-2 text-2xl font-bold text-slate-950">{card.value}</h3>
                  <p className={cn('mt-1 text-xs font-bold', card.noteColor)}>{card.note}</p>
                </div>
                <div className={cn('flex h-12 w-12 items-center justify-center rounded-xl text-white', card.color)}>
                  <Icon className="h-6 w-6" />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <section className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <h3 className="text-xl font-bold text-slate-950">Quick Actions</h3>
        <div className="mt-7 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
          {quickActions.map((action) => {
            const Icon = action.icon;
            return (
              <button
                key={action.label}
                className="flex min-h-28 flex-col items-center justify-center rounded-2xl border border-slate-100 bg-white p-4 transition hover:-translate-y-1 hover:border-indigo-100 hover:shadow-md"
              >
                <div className={cn('mb-3 flex h-12 w-12 items-center justify-center rounded-xl text-white', action.color)}>
                  <Icon className="h-6 w-6" />
                </div>
                <span className="text-center text-xs font-bold text-slate-700">{action.label}</span>
              </button>
            );
          })}
        </div>
      </section>

      <div className="grid gap-6 lg:grid-cols-2">
        <EmptyPanel title="Recent Activities" />
        <EmptyPanel title="Notifications & Reminders" />
      </div>

      <EmptyPanel title="Upcoming Events & Schedule" />
    </div>
  );
}
