import { AnimatePresence, motion } from 'framer-motion';
import {
  ArrowLeft,
  ArrowUpRight,
  BarChart3,
  Building2,
  CalendarDays,
  DollarSign,
  Grid2X2,
  List,
  MoreVertical,
  Plus,
  Search,
  UserRound,
  UserRoundPlus,
  Users,
  X,
} from 'lucide-react';
import { FormEvent, useEffect, useState } from 'react';
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import {
  createDepartment,
  DepartmentDetail,
  DepartmentMember,
  getDepartmentDetail,
  getManagedDepartments,
  ManagedDepartment,
} from '../lib/api';

function initials(name: string) {
  return name.split(' ').map((part) => part[0]).join('').slice(0, 2).toUpperCase();
}

function MemberAvatar({ member }: { member: DepartmentMember }) {
  return member.profile_photo ? (
    <img src={member.profile_photo} alt={member.name} className="h-9 w-9 rounded-full border-2 border-white object-cover" />
  ) : (
    <span className="flex h-9 w-9 items-center justify-center rounded-full border-2 border-white bg-indigo-100 text-xs font-bold text-indigo-700">{initials(member.name)}</span>
  );
}

function DepartmentCard({ department, onOpen, onAddMember }: { department: ManagedDepartment; onOpen: () => void; onAddMember: () => void }) {
  return (
    <motion.article layout initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div className="p-6">
        <div className="flex items-center justify-between">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600"><Building2 className="h-6 w-6" /></div>
          <div className="flex items-center gap-2"><button onClick={onAddMember} className="flex h-9 items-center gap-2 rounded-xl bg-indigo-600 px-4 text-xs font-bold text-white shadow-md shadow-indigo-100 transition hover:bg-indigo-700"><UserRoundPlus className="h-4 w-4" />Add Member</button><button title="Department actions" className="rounded-lg p-2 text-slate-400 transition hover:bg-slate-50"><MoreVertical className="h-5 w-5" /></button></div>
        </div>
        <h3 className="mt-6 text-xl font-bold text-slate-950">{department.name}</h3>
        <p className="mt-1 text-sm text-slate-500">Managed by <span className="font-semibold text-slate-700">{department.manager ?? 'Not assigned'}</span></p>
        <div className="mt-6 grid grid-cols-2 gap-4">
          <div className="rounded-xl bg-slate-50 p-4"><p className="flex items-center gap-2 text-xs font-bold uppercase text-slate-500"><Users className="h-4 w-4" />Employees</p><p className="mt-2 text-xl font-bold text-slate-950">{department.employee_count}</p></div>
          <div className="rounded-xl bg-slate-50 p-4"><p className="flex items-center gap-2 text-xs font-bold uppercase text-slate-500"><DollarSign className="h-4 w-4" />Budget</p><p className="mt-2 text-lg font-bold text-slate-950">Not set</p></div>
        </div>
      </div>
      <div className="flex items-center justify-between border-t border-slate-100 bg-slate-50 px-6 py-4">
        <div className="flex -space-x-2">{department.member_preview.map((member) => <MemberAvatar key={member.id} member={member} />)}{department.employee_count > 4 && <span className="flex h-9 w-9 items-center justify-center rounded-full border-2 border-white bg-slate-200 text-xs font-bold text-slate-600">+{department.employee_count - 4}</span>}{department.employee_count === 0 && <span className="text-xs font-semibold text-slate-400">No members</span>}</div>
        <button onClick={onOpen} className="flex items-center gap-1 text-sm font-bold text-indigo-600 transition hover:text-indigo-700">Details <ArrowUpRight className="h-4 w-4" /></button>
      </div>
    </motion.article>
  );
}

function AddDepartmentDialog({ onClose, onCreated }: { onClose: () => void; onCreated: () => void }) {
  const [name, setName] = useState('');
  const [code, setCode] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');
  const [isSaving, setIsSaving] = useState(false);

  const submit = async (event: FormEvent) => {
    event.preventDefault(); setError(''); setIsSaving(true);
    try { await createDepartment({ name, code, description }); onCreated(); }
    catch (requestError) { setError(requestError instanceof Error ? requestError.message : 'Unable to create department.'); }
    finally { setIsSaving(false); }
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onMouseDown={onClose} className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-5 backdrop-blur-sm">
      <motion.form onSubmit={submit} onMouseDown={(event) => event.stopPropagation()} initial={{ opacity: 0, y: 14, scale: 0.96 }} animate={{ opacity: 1, y: 0, scale: 1 }} exit={{ opacity: 0, y: 10, scale: 0.97 }} className="w-full max-w-lg rounded-2xl border border-slate-200 bg-white p-7 shadow-2xl">
        <div className="flex items-start justify-between"><div><h3 className="text-2xl font-bold text-slate-950">Add Department</h3><p className="mt-1 text-sm text-slate-500">Create a new company department.</p></div><button type="button" title="Close" onClick={onClose} className="rounded-lg p-2 text-slate-400 hover:bg-slate-100"><X className="h-5 w-5" /></button></div>
        <label className="mt-6 block text-sm font-bold text-slate-800">Department Name<input required maxLength={150} value={name} onChange={(event) => setName(event.target.value)} placeholder="e.g. Engineering" className="mt-2 h-12 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 font-normal outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100" /></label>
        <label className="mt-5 block text-sm font-bold text-slate-800">Department Code<input required maxLength={30} value={code} onChange={(event) => setCode(event.target.value.toUpperCase())} placeholder="e.g. ENG" className="mt-2 h-12 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 font-normal uppercase outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100" /></label>
        <label className="mt-5 block text-sm font-bold text-slate-800">Description <span className="font-medium text-slate-400">(optional)</span><textarea rows={4} value={description} onChange={(event) => setDescription(event.target.value)} className="mt-2 w-full resize-none rounded-xl border border-slate-200 bg-slate-50 p-4 font-normal outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100" /></label>
        {error && <p className="mt-4 rounded-xl bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">{error}</p>}
        <div className="mt-7 flex justify-end gap-3"><button type="button" onClick={onClose} className="h-11 px-5 text-sm font-bold text-slate-600">Cancel</button><button disabled={isSaving} className="h-11 rounded-xl bg-indigo-600 px-5 text-sm font-bold text-white disabled:bg-slate-300">{isSaving ? 'Creating...' : 'Create Department'}</button></div>
      </motion.form>
    </motion.div>
  );
}

function DepartmentDetailView({ departmentId, onNavigate }: { departmentId: number; onNavigate: (path: string) => void }) {
  const [department, setDepartment] = useState<DepartmentDetail | null>(null);
  const [error, setError] = useState('');
  useEffect(() => { getDepartmentDetail(departmentId).then(setDepartment).catch((requestError) => setError(requestError instanceof Error ? requestError.message : 'Unable to load department.')); }, [departmentId]);

  if (error) return <div className="rounded-2xl border border-red-200 bg-red-50 p-10 text-center font-semibold text-red-700">{error}</div>;
  if (!department) return <div className="rounded-2xl border border-slate-200 bg-white p-10 text-center font-semibold text-slate-500">Loading department...</div>;

  const chartData = department.performance.map((point) => ({ ...point, label: new Date(`${point.month}-01T00:00:00`).toLocaleDateString(undefined, { month: 'short' }) }));
  return (
    <div className="mx-auto max-w-7xl space-y-7">
      <div className="flex items-start gap-4"><button title="Back to departments" onClick={() => onNavigate('departments')} className="mt-1 rounded-lg p-2 text-slate-500 transition hover:bg-white hover:text-indigo-600"><ArrowLeft className="h-5 w-5" /></button><div><h2 className="text-3xl font-bold text-slate-950">{department.name}</h2><p className="mt-1 text-lg text-slate-500">Comprehensive overview of the department's metrics and team.</p></div></div>
      <div className="grid gap-5 md:grid-cols-3">
        <div className="flex items-center gap-4 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><span className="flex h-12 w-12 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600"><UserRound className="h-6 w-6" /></span><div><p className="text-sm text-slate-500">Department Manager</p><p className="mt-1 font-bold text-slate-950">{department.manager ?? 'Not assigned'}</p></div></div>
        <div className="flex items-center gap-4 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><span className="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600"><DollarSign className="h-6 w-6" /></span><div><p className="text-sm text-slate-500">Annual Budget</p><p className="mt-1 font-bold text-slate-950">{department.annual_budget === null ? 'Not set' : `$${department.annual_budget.toLocaleString()}`}</p></div></div>
        <div className="flex items-center gap-4 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><span className="flex h-12 w-12 items-center justify-center rounded-xl bg-amber-50 text-amber-600"><Users className="h-6 w-6" /></span><div><p className="text-sm text-slate-500">Total Employees</p><p className="mt-1 font-bold text-slate-950">{department.employee_count} Members</p></div></div>
      </div>
      <div className="grid items-start gap-7 xl:grid-cols-[minmax(0,2fr)_minmax(300px,1fr)]">
        <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm"><div className="flex items-center justify-between border-b border-slate-100 px-6 py-5"><h3 className="text-lg font-bold text-slate-950">Department Members</h3><button onClick={() => onNavigate('add-employee')} className="flex items-center gap-2 text-sm font-bold text-indigo-600"><UserRoundPlus className="h-4 w-4" />Add member</button></div><div className="overflow-x-auto"><table className="w-full min-w-[650px] text-left"><thead className="bg-slate-50 text-xs uppercase text-slate-500"><tr><th className="px-6 py-4">Employee</th><th className="px-6 py-4">Role</th><th className="px-6 py-4">Status</th><th className="px-6 py-4 text-right">Action</th></tr></thead><tbody className="divide-y divide-slate-100">{department.members.map((member) => <tr key={member.id}><td className="px-6 py-4"><div className="flex items-center gap-3"><MemberAvatar member={member} /><div><p className="font-bold text-slate-950">{member.name}</p><p className="text-xs text-slate-500">{member.email ?? 'No email'}</p></div></div></td><td className="px-6 py-4 text-sm text-slate-600">{member.position ?? 'Unassigned'}</td><td className="px-6 py-4"><span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-bold capitalize text-emerald-700">{member.status.replace('_', ' ')}</span></td><td className="px-6 py-4 text-right"><button title="Employee actions" className="rounded-lg p-2 text-slate-400 hover:bg-slate-50"><MoreVertical className="h-5 w-5" /></button></td></tr>)}{department.members.length === 0 && <tr><td colSpan={4} className="px-6 py-12 text-center text-sm font-semibold text-slate-500">No members in this department.</td></tr>}</tbody></table></div></section>
        <div className="space-y-6"><section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><div className="flex items-center justify-between"><h3 className="text-lg font-bold text-slate-950">Performance Trend</h3><BarChart3 className="h-5 w-5 text-indigo-600" /></div>{chartData.length ? <div className="mt-5 h-64"><ResponsiveContainer width="100%" height="100%"><BarChart data={chartData}><CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" /><XAxis dataKey="label" axisLine={false} tickLine={false} /><YAxis domain={[0, 5]} axisLine={false} tickLine={false} /><Tooltip /><Bar dataKey="score" fill="#4f46e5" radius={[5, 5, 0, 0]} maxBarSize={28} /></BarChart></ResponsiveContainer></div> : <div className="flex h-64 items-center justify-center text-center text-sm font-semibold text-slate-500">No completed performance reviews yet.</div>}<p className="mt-3 text-center text-xs text-slate-400">Average monthly performance score (out of 5.0)</p></section>
        <section className="rounded-2xl bg-indigo-600 p-6 text-white shadow-lg shadow-indigo-200"><div className="flex items-center gap-3"><CalendarDays className="h-5 w-5" /><h3 className="text-lg font-bold">Upcoming Events</h3></div><p className="mt-8 rounded-xl bg-white/10 px-4 py-6 text-center text-sm text-indigo-100">No department events scheduled.</p></section></div>
      </div>
    </div>
  );
}

export default function DepartmentsPage({ departmentId, onNavigate }: { departmentId?: number; onNavigate: (path: string) => void }) {
  const [departments, setDepartments] = useState<ManagedDepartment[]>([]);
  const [search, setSearch] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [showCreate, setShowCreate] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    if (departmentId) return;
    const timer = window.setTimeout(() => { setIsLoading(true); setError(''); getManagedDepartments(search).then(setDepartments).catch((requestError) => setError(requestError instanceof Error ? requestError.message : 'Unable to load departments.')).finally(() => setIsLoading(false)); }, 250);
    return () => window.clearTimeout(timer);
  }, [departmentId, search, refreshKey]);

  if (departmentId) return <DepartmentDetailView departmentId={departmentId} onNavigate={onNavigate} />;
  return (
    <div className="mx-auto max-w-7xl space-y-7">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"><div><h2 className="text-3xl font-bold text-slate-950">Department Management</h2><p className="mt-2 text-lg text-slate-500">Organize your company structure and teams.</p></div><button onClick={() => setShowCreate(true)} className="flex h-12 items-center justify-center gap-2 rounded-xl bg-indigo-600 px-5 font-bold text-white shadow-lg shadow-indigo-200 transition hover:bg-indigo-700"><Plus className="h-5 w-5" />Add Department</button></div>
      <div className="flex items-center gap-4 rounded-3xl bg-white p-3"><label className="flex h-14 flex-1 items-center gap-3 rounded-2xl bg-slate-50 px-5 text-slate-400"><Search className="h-5 w-5" /><input type="search" value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search departments or managers..." className="h-full flex-1 bg-transparent text-sm font-medium text-slate-700 outline-none" /></label><div className="hidden rounded-2xl bg-slate-50 p-1 sm:flex"><button title="Grid view" className="flex h-11 w-11 items-center justify-center rounded-xl bg-white text-indigo-600 shadow-sm"><Grid2X2 className="h-5 w-5" /></button><button title="List view" className="flex h-11 w-11 items-center justify-center rounded-xl text-slate-400"><List className="h-5 w-5" /></button></div></div>
      {isLoading ? <div className="rounded-2xl border border-slate-200 bg-white p-10 text-center font-semibold text-slate-500">Loading departments...</div> : error ? <div className="rounded-2xl border border-red-200 bg-red-50 p-10 text-center font-semibold text-red-700">{error}</div> : departments.length === 0 ? <div className="rounded-2xl border border-slate-200 bg-white p-10 text-center font-semibold text-slate-500">No departments found.</div> : <motion.div layout className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">{departments.map((department) => <DepartmentCard key={department.id} department={department} onOpen={() => onNavigate(`departments/${department.id}`)} onAddMember={() => onNavigate('add-employee')} />)}</motion.div>}
      <AnimatePresence>{showCreate && <AddDepartmentDialog onClose={() => setShowCreate(false)} onCreated={() => { setShowCreate(false); setRefreshKey((value) => value + 1); }} />}</AnimatePresence>
    </div>
  );
}
