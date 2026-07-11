import {
  BadgeCheck,
  Briefcase,
  Calendar,
  Contact,
  CreditCard,
  FileText,
  GraduationCap,
  HeartPulse,
  Mail,
  MapPin,
  Phone,
  Printer,
  Shield,
  Star,
  User,
  Users,
  X,
} from 'lucide-react';
import { AuthUser } from '../lib/api';
import { getProfileOverview, ProfileOverview } from '../lib/api';
import { cn } from '../lib/utils';
import { useEffect, useState } from 'react';

type ProfilePageProps = {
  user: AuthUser | null;
  onNavigate: (path:string)=>void;
};

const quickActions = [
  { label: 'Employee Info', icon: User, color: 'bg-blue-500', path: 'profile/information' },
  { label: 'Status', icon: HeartPulse, color: 'bg-emerald-500', path: 'profile/status' },
  { label: 'Bank Info', icon: CreditCard, color: 'bg-violet-500', path: 'profile/bank' },
  { label: 'Family', icon: Users, color: 'bg-pink-500', path: 'profile/family' },
  { label: 'Education', icon: GraduationCap, color: 'bg-indigo-500', path: 'profile/education' },
  { label: 'Employment', icon: Briefcase, color: 'bg-orange-500', path: 'profile/employment' },
  { label: 'Contact', icon: Contact, color: 'bg-teal-500', path: 'profile/contact' },
  { label: 'Supervisor', icon: User, color: 'bg-sky-500', path: 'profile/supervisor' },
  { label: 'Document & Passport', icon: FileText, color: 'bg-rose-500', path: 'profile/documents' },
  { label: 'Payroll', icon: CreditCard, color: 'bg-green-600', path: 'profile/payroll' },
  { label: 'Performance', icon: Star, color: 'bg-indigo-600', path: 'profile/performance' },
  { label: 'Security', icon: Shield, color: 'bg-slate-900', path: 'settings' },
  { label: 'Employee ID', icon: BadgeCheck, color: 'bg-slate-950', path: 'employee-id' },
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

export default function ProfilePage({ user, onNavigate }: ProfilePageProps) {
  const [profile,setProfile]=useState<ProfileOverview|null>(null);const[loading,setLoading]=useState(true);const[error,setError]=useState('');
  const [showEmployeeId,setShowEmployeeId]=useState(false);
  useEffect(()=>{getProfileOverview().then(setProfile).catch(e=>setError(e instanceof Error?e.message:'Unable to load profile.')).finally(()=>setLoading(false));},[]);
  useEffect(()=>{if(!showEmployeeId)return;const close=(event:KeyboardEvent)=>{if(event.key==='Escape')setShowEmployeeId(false)};document.addEventListener('keydown',close);document.body.style.overflow='hidden';return()=>{document.removeEventListener('keydown',close);document.body.style.overflow=''}},[showEmployeeId]);
  const displayName = profile?.employee?.name ?? profile?.account.name ?? user?.name ?? 'User';
  const role = profile?.employee?.position ?? profile?.account.role ?? user?.role ?? 'User';
  const initials = initialsFor(displayName) || 'US';
  const employee=profile?.employee;const stats=profile?.stats;
  const money=(value:number)=>new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0}).format(value);

  if(loading)return <div className="p-20 text-center text-slate-500">Loading profile...</div>;
  if(error)return <div className="rounded-2xl bg-red-50 p-8 text-center text-red-700">{error}</div>;

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
              <span className="rounded-full bg-indigo-600 px-4 py-1 text-xs font-bold text-white">{employee?`${employee.status} Employee`:'Active Account'}</span>
            </div>
            <div className="mt-5 grid gap-4 text-sm font-medium text-slate-500 md:grid-cols-4">
              <span>{role}</span>
              <span>{employee?.department??profile?.account.email??user?.email??'No email'}</span>
              <span>Joined: {employee?.hire_date??profile?.account.created_at.slice(0,10)??'Not available'}</span>
              <span>{employee?`Employee ID: ${employee.employee_code}`:`User ID: ${profile?.account.id??user?.id??'-'}`}</span>
            </div>
          </div>
        </div>
      </section>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        {[
          { title: 'Leave Balance', value: stats?.leave_balance!=null?`${stats.leave_balance} Days`:'Not linked', note: employee?'Annual leave remaining':'Employee record required', icon: Calendar, color: 'bg-emerald-500', noteColor: 'text-slate-400' },
          { title: 'Attendance', value: stats?.attendance!=null?`${stats.attendance}%`:'Not linked', note: employee?'Current month':'Employee record required', icon: HeartPulse, color: 'bg-blue-500', noteColor: 'text-slate-400' },
          { title: 'Current Salary', value: stats?.salary!=null?money(stats.salary):'Restricted', note: employee?'Latest payroll or base salary':'Employee record required', icon: CreditCard, color: 'bg-violet-500', noteColor: 'text-slate-400' },
          { title: 'Performance', value: stats?.performance!=null?`${stats.performance}/5`:'No review', note: employee?'Latest completed review':'Employee record required', icon: Star, color: 'bg-orange-500', noteColor: 'text-slate-400' },
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
                onClick={()=>action.path==='employee-id'?setShowEmployeeId(true):onNavigate(action.path)}
                title={`Open ${action.label}`}
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

      {showEmployeeId&&(
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 p-4 backdrop-blur-sm" onMouseDown={(event)=>{if(event.target===event.currentTarget)setShowEmployeeId(false)}}>
          <section role="dialog" aria-modal="true" aria-labelledby="employee-id-title" className="employee-id-modal max-h-[94vh] w-full max-w-4xl overflow-y-auto rounded-3xl bg-slate-50 shadow-2xl">
            <header className="flex items-center justify-between gap-4 border-b border-slate-200 bg-white px-6 py-5 sm:px-8">
              <div className="flex min-w-0 items-center gap-4">
                <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-indigo-600 text-white"><BadgeCheck className="h-6 w-6"/></span>
                <div><h2 id="employee-id-title" className="text-xl font-bold text-slate-950">Official Employee ID</h2><p className="text-sm text-slate-500">Print-ready identity card</p></div>
              </div>
              <div className="flex items-center gap-2">
                <button onClick={()=>window.print()} className="employee-id-print flex h-10 items-center gap-2 rounded-lg bg-indigo-600 px-4 text-sm font-bold text-white shadow-lg shadow-indigo-200"><Printer className="h-4 w-4"/>Print ID Card</button>
                <button onClick={()=>setShowEmployeeId(false)} aria-label="Close employee ID" className="flex h-10 w-10 items-center justify-center rounded-lg text-slate-400 hover:bg-slate-100 hover:text-slate-700"><X className="h-5 w-5"/></button>
              </div>
            </header>
            <div className="employee-id-print-area grid gap-8 p-7 sm:p-10 md:grid-cols-2">
              <article className="relative mx-auto flex aspect-[0.64] w-full max-w-[350px] flex-col overflow-hidden rounded-[28px] bg-white shadow-xl">
                <div className="flex h-[36%] flex-col items-center bg-indigo-600 px-6 pt-8 text-white">
                  <BadgeCheck className="h-9 w-9"/><p className="mt-5 text-lg font-black uppercase tracking-widest">Siegecode HRM</p><p className="text-[10px] font-bold uppercase tracking-widest text-indigo-100">Human Resource Division</p>
                </div>
                <div className="absolute left-1/2 top-[27%] flex h-32 w-32 -translate-x-1/2 items-center justify-center rounded-2xl border-8 border-white bg-indigo-100 text-4xl font-black text-indigo-600 shadow-lg">{initials}</div>
                <div className="flex flex-1 flex-col px-8 pb-0 pt-24 text-center">
                  <h3 className="text-2xl font-black uppercase text-slate-900">{displayName}</h3><p className="mt-1 font-bold text-indigo-600">{role}</p>
                  <div className="mt-8 grid grid-cols-2 gap-3 text-left"><div className="rounded-xl bg-slate-50 p-3"><p className="text-[10px] font-bold uppercase text-slate-400">ID Number</p><p className="font-black text-slate-900">{employee?.employee_code??`USR-${profile?.account.id}`}</p></div><div className="rounded-xl bg-slate-50 p-3"><p className="text-[10px] font-bold uppercase text-slate-400">Status</p><p className="font-black text-emerald-600">{employee?.status??'Active'}</p></div></div>
                  <div className="-mx-8 mt-auto bg-slate-950 px-8 py-7 text-left text-white"><p className="text-xs font-black uppercase tracking-wide">Official Badge</p><p className="mt-1 text-[9px] uppercase text-slate-400">Valid while account is active</p></div>
                </div>
              </article>
              <article className="mx-auto flex aspect-[0.64] w-full max-w-[350px] flex-col rounded-[28px] bg-slate-950 p-8 text-slate-300 shadow-xl">
                <div><p className="flex items-center gap-2 text-xs font-black uppercase tracking-widest text-indigo-400"><Shield className="h-4 w-4"/>Security Information</p><p className="mt-5 text-sm leading-6 text-slate-400">This card identifies an authorized Siegecode HRM account holder. If found, return it to the issuing organization.</p></div>
                <div className="mt-9 space-y-5">
                  <div className="flex gap-3"><Phone className="mt-1 h-5 w-5 shrink-0 text-indigo-400"/><div><p className="text-[10px] font-bold uppercase tracking-widest text-slate-500">Emergency Contact</p><p className="font-bold text-white">{employee?.emergency_contact_phone??'Not provided'}</p></div></div>
                  <div className="flex gap-3"><Mail className="mt-1 h-5 w-5 shrink-0 text-indigo-400"/><div className="min-w-0"><p className="text-[10px] font-bold uppercase tracking-widest text-slate-500">Office Email</p><p className="break-all font-bold text-white">{employee?.email??profile?.account.email}</p></div></div>
                  <div className="flex gap-3"><MapPin className="mt-1 h-5 w-5 shrink-0 text-indigo-400"/><div><p className="text-[10px] font-bold uppercase tracking-widest text-slate-500">Department</p><p className="font-bold text-white">{employee?.department??'Account administration'}</p></div></div>
                </div>
                <div className="mt-auto border-t border-slate-800 pt-7 text-center"><p className="font-black italic tracking-wider text-indigo-400">SIEGECODE HRM</p><p className="mt-1 text-[9px] uppercase tracking-widest text-slate-600">Verified workforce identity</p></div>
              </article>
            </div>
          </section>
        </div>
      )}
    </div>
  );
}
