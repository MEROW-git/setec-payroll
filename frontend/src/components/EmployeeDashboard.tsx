import {
  BadgeDollarSign,
  Briefcase,
  Calendar,
  Clock,
  CreditCard,
  FileText,
  GraduationCap,
  HeartPulse,
  Contact,
  Star,
  User,
  Users,
} from 'lucide-react';
import { cn } from '../lib/utils';

type EmployeeDashboardProps = {
  userName: string;
};

const metricCards = [
  { title: 'Leave Balance', value: '18 Days', note: 'Out of 24', icon: Calendar, color: 'bg-emerald-500', noteColor: 'text-emerald-600' },
  { title: 'Attendance', value: '98.5%', note: 'Excellent', icon: Clock, color: 'bg-blue-500', noteColor: 'text-blue-600' },
  { title: 'Current Salary', value: '$85,000', note: 'Annual', icon: BadgeDollarSign, color: 'bg-violet-500', noteColor: 'text-violet-600' },
  { title: 'Performance', value: '4.8/5.0', note: 'Outstanding', icon: Star, color: 'bg-orange-500', noteColor: 'text-orange-600' },
];

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
];

export default function EmployeeDashboard({ userName }: EmployeeDashboardProps) {
  const initials = userName
    .split(' ')
    .map((part) => part[0])
    .join('')
    .slice(0, 2)
    .toUpperCase() || 'EU';

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-slate-950">My Dashboard</h2>
        <p className="mt-2 text-lg text-slate-500">Welcome back! Here's your personal overview.</p>
      </div>

      <section className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <div className="flex flex-col gap-6 md:flex-row md:items-center">
          <div className="flex h-24 w-24 shrink-0 items-center justify-center rounded-full bg-indigo-600 text-3xl font-bold text-white shadow-xl shadow-indigo-200">
            {initials}
          </div>
          <div className="flex-1">
            <div className="flex flex-wrap items-center gap-3">
              <h3 className="text-3xl font-bold text-slate-950">{userName || 'Employee User'}</h3>
              <span className="rounded-full bg-indigo-600 px-4 py-1 text-xs font-bold text-white">Active Employee</span>
            </div>
            <div className="mt-5 grid gap-4 text-sm font-medium text-slate-500 md:grid-cols-4">
              <span>Product Designer</span>
              <span>Design</span>
              <span>Joined: Jan 15, 2022</span>
              <span>Employee ID: EMP-00EM001</span>
            </div>
          </div>
        </div>
      </section>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        {metricCards.map((card) => {
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
    </div>
  );
}
