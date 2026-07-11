import { AnimatePresence, motion } from 'framer-motion';
import {
  AlertCircle,
  Briefcase,
  Grid2X2,
  List,
  MoreVertical,
  Plus,
  Search,
  Shield,
  SlidersHorizontal,
  UserRoundPlus,
  Users,
  X,
} from 'lucide-react';
import { FormEvent, useEffect, useState } from 'react';
import {
  assignPosition,
  createPosition,
  Department,
  EmployeeListItem,
  getDepartments,
  getEmployees,
  getManagedPositions,
  ManagedPosition,
  PositionManagementResult,
} from '../lib/api';
import { cn } from '../lib/utils';

const emptyResult: PositionManagementResult = {
  items: [],
  stats: { total: 0, assigned: 0, unassigned: 0 },
};

function RoleCard({ role, onAssign }: { role: ManagedPosition; onAssign: (role: ManagedPosition) => void }) {
  return (
    <motion.article
      layout
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex min-h-[310px] flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm"
    >
      <div className="flex-1 p-6">
        <div className="flex items-start justify-between">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600">
            <Shield className="h-6 w-6" />
          </div>
          <button title="Role actions" className="rounded-lg p-1 text-slate-400 transition hover:bg-slate-50 hover:text-slate-700">
            <MoreVertical className="h-5 w-5" />
          </button>
        </div>
        <h3 className="mt-5 text-xl font-bold text-slate-950">{role.title}</h3>
        <p className="mt-1 text-xs font-bold uppercase text-indigo-600">{role.department ?? 'No department'}</p>
        <p className="mt-4 min-h-12 text-sm leading-6 text-slate-500">
          {role.description || 'No role description has been added yet.'}
        </p>
        {role.permissions.length > 0 && <div className="mt-4 flex flex-wrap gap-2">{role.permissions.slice(0, 3).map((permission) => <span key={permission} className="rounded-md bg-slate-100 px-2 py-1 text-[10px] font-bold uppercase text-slate-600">{permission}</span>)}</div>}
        <div className="mt-5 flex items-center justify-between text-sm text-slate-500">
          <span>Employees</span>
          <span className="font-bold text-slate-950">{role.employee_count}</span>
        </div>
      </div>
      <div className="border-t border-slate-100 bg-slate-50 p-4">
        <button onClick={() => onAssign(role)} className="flex h-10 w-full items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white text-sm font-bold text-slate-700 transition hover:border-indigo-200 hover:text-indigo-600">
          <UserRoundPlus className="h-4 w-4" />
          Assign Role
        </button>
      </div>
    </motion.article>
  );
}

function employeeInitials(name: string) {
  return name.split(' ').map((part) => part[0]).join('').slice(0, 2).toUpperCase();
}

type AssignRoleDialogProps = {
  role: ManagedPosition;
  onClose: () => void;
  onAssigned: () => void;
};

function AssignRoleDialog({ role, onClose, onAssigned }: AssignRoleDialogProps) {
  const [employees, setEmployees] = useState<EmployeeListItem[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [search, setSearch] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const timer = window.setTimeout(() => {
      setIsLoading(true);
      setError('');
      getEmployees({ search, per_page: 100 })
        .then((data) => setEmployees(data.items))
        .catch((requestError) => setError(requestError instanceof Error ? requestError.message : 'Unable to load employees.'))
        .finally(() => setIsLoading(false));
    }, 200);
    return () => window.clearTimeout(timer);
  }, [search]);

  const confirmAssignment = async () => {
    if (!selectedId) return;
    setIsSaving(true);
    setError('');
    try {
      await assignPosition(role.id, selectedId);
      onAssigned();
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to assign role.');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <motion.div
      className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/45 p-5 backdrop-blur-sm"
      initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onMouseDown={onClose}
    >
      <motion.section
        role="dialog" aria-modal="true" aria-label={`Assign ${role.title}`}
        onMouseDown={(event) => event.stopPropagation()}
        initial={{ opacity: 0, scale: 0.96, y: 16 }} animate={{ opacity: 1, scale: 1, y: 0 }} exit={{ opacity: 0, scale: 0.97, y: 12 }}
        className="flex max-h-[min(720px,90vh)] w-full max-w-lg flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-2xl"
      >
        <header className="flex items-start justify-between border-b border-slate-100 px-6 py-5">
          <div className="flex gap-3">
            <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600"><UserRoundPlus className="h-5 w-5" /></div>
            <div><h3 className="text-xl font-bold text-slate-950">Assign Role</h3><p className="mt-1 text-sm text-slate-500">Assigning <span className="font-bold text-indigo-600">{role.title}</span> to an employee.</p></div>
          </div>
          <button type="button" title="Close" onClick={onClose} className="rounded-lg p-2 text-slate-400 transition hover:bg-slate-100 hover:text-slate-700"><X className="h-5 w-5" /></button>
        </header>

        <div className="flex min-h-0 flex-1 flex-col px-6 py-5">
          <label className="flex h-12 shrink-0 items-center gap-3 rounded-xl bg-slate-50 px-4 text-slate-400">
            <Search className="h-5 w-5" />
            <input autoFocus type="search" value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search employees..." className="h-full flex-1 bg-transparent text-sm text-slate-700 outline-none placeholder:text-slate-400" />
          </label>
          <div className="mt-5 min-h-[220px] space-y-2 overflow-y-auto pr-1">
            {isLoading ? <p className="py-12 text-center text-sm font-semibold text-slate-500">Loading employees...</p> : employees.length === 0 ? <p className="py-12 text-center text-sm font-semibold text-slate-500">No employees found.</p> : employees.map((employee) => {
              const selected = selectedId === employee.id;
              return (
                <button key={employee.id} type="button" onClick={() => setSelectedId(employee.id)} className={cn('flex w-full items-center gap-3 rounded-xl border p-3 text-left transition', selected ? 'border-indigo-300 bg-indigo-50/60 ring-1 ring-indigo-100' : 'border-slate-200 bg-slate-50 hover:border-indigo-200')}>
                  {employee.profile_photo ? <img src={employee.profile_photo} alt="" className="h-11 w-11 rounded-lg object-cover" /> : <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-indigo-100 text-sm font-bold text-indigo-700">{employeeInitials(employee.name)}</span>}
                  <span className="min-w-0 flex-1"><span className="block truncate text-sm font-bold text-slate-900">{employee.name}</span><span className="block truncate text-xs text-slate-500">{employee.position ?? 'No role'} • {employee.department ?? 'No department'}</span></span>
                  <span className={cn('h-5 w-5 shrink-0 rounded-full border-2', selected ? 'border-[6px] border-indigo-500 bg-white' : 'border-slate-300')} />
                </button>
              );
            })}
          </div>
          {error && <p className="mt-3 rounded-xl bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">{error}</p>}
          <div className="mt-5 flex gap-3 rounded-xl border border-amber-200 bg-amber-50 p-4 text-amber-700"><AlertCircle className="mt-0.5 h-5 w-5 shrink-0" /><p className="text-sm leading-5">Assigning this role will update the employee's job title and department immediately.</p></div>
        </div>
        <footer className="grid grid-cols-2 gap-3 border-t border-slate-100 p-6"><button type="button" onClick={onClose} className="h-12 rounded-xl border border-slate-200 text-sm font-bold text-slate-600 transition hover:bg-slate-50">Cancel</button><button type="button" onClick={confirmAssignment} disabled={!selectedId || isSaving} className="h-12 rounded-xl bg-indigo-600 text-sm font-bold text-white shadow-lg shadow-indigo-100 transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:bg-slate-300 disabled:shadow-none">{isSaving ? 'Assigning...' : 'Confirm Assignment'}</button></footer>
      </motion.section>
    </motion.div>
  );
}

type AddRoleDialogProps = {
  departments: Department[];
  onClose: () => void;
  onCreated: () => void;
};

function AddRoleDialog({ departments, onClose, onCreated }: AddRoleDialogProps) {
  const [title, setTitle] = useState('');
  const [departmentId, setDepartmentId] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');
  const [isSaving, setIsSaving] = useState(false);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError('');
    setIsSaving(true);
    try {
      await createPosition({ title, department_id: Number(departmentId), description });
      onCreated();
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to create role.');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <motion.div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/35 p-5 backdrop-blur-sm" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onMouseDown={onClose}>
      <motion.form onSubmit={handleSubmit} onMouseDown={(event) => event.stopPropagation()} initial={{ opacity: 0, scale: 0.96, y: 14 }} animate={{ opacity: 1, scale: 1, y: 0 }} exit={{ opacity: 0, scale: 0.97, y: 10 }} className="w-full max-w-lg rounded-2xl border border-slate-200 bg-white p-7 shadow-2xl">
        <div className="flex items-start justify-between">
          <div><h3 className="text-2xl font-bold text-slate-950">Add New Role</h3><p className="mt-1 text-sm text-slate-500">Create a job designation for a department.</p></div>
          <button type="button" title="Close" onClick={onClose} className="rounded-lg p-2 text-slate-400 transition hover:bg-slate-100 hover:text-slate-700"><X className="h-5 w-5" /></button>
        </div>
        <label className="mt-6 block text-sm font-bold text-slate-800">Role Title<input required maxLength={150} value={title} onChange={(event) => setTitle(event.target.value)} placeholder="e.g. Senior Product Designer" className="mt-2 h-12 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 font-normal outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100" /></label>
        <label className="mt-5 block text-sm font-bold text-slate-800">Department<select required value={departmentId} onChange={(event) => setDepartmentId(event.target.value)} className="mt-2 h-12 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 font-normal outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100"><option value="">Select department</option>{departments.map((department) => <option key={department.id} value={department.id}>{department.name}</option>)}</select></label>
        <label className="mt-5 block text-sm font-bold text-slate-800">Description <span className="font-medium text-slate-400">(optional)</span><textarea value={description} onChange={(event) => setDescription(event.target.value)} placeholder="Describe this role's responsibilities" rows={4} className="mt-2 w-full resize-none rounded-xl border border-slate-200 bg-slate-50 p-4 font-normal outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100" /></label>
        {error && <p className="mt-4 rounded-xl bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">{error}</p>}
        <div className="mt-7 flex justify-end gap-3"><button type="button" onClick={onClose} className="h-11 rounded-xl px-5 text-sm font-bold text-slate-600 transition hover:bg-slate-100">Cancel</button><button disabled={isSaving || departments.length === 0} className="h-11 rounded-xl bg-indigo-600 px-5 text-sm font-bold text-white shadow-lg shadow-indigo-200 transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:bg-slate-300">{isSaving ? 'Creating...' : 'Create Role'}</button></div>
      </motion.form>
    </motion.div>
  );
}

export default function RolesPage({ onNavigate }: { onNavigate: (path: string) => void }) {
  const [result, setResult] = useState(emptyResult);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [search, setSearch] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [showAddRole, setShowAddRole] = useState(false);
  const [assigningRole, setAssigningRole] = useState<ManagedPosition | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => { getDepartments().then(setDepartments).catch(() => setDepartments([])); }, []);
  useEffect(() => {
    const timer = window.setTimeout(() => {
      setIsLoading(true);
      setError('');
      getManagedPositions(search).then(setResult).catch((requestError) => setError(requestError instanceof Error ? requestError.message : 'Unable to load roles.')).finally(() => setIsLoading(false));
    }, 250);
    return () => window.clearTimeout(timer);
  }, [search, refreshKey]);

  const cards = [
    { label: 'Total Roles', value: result.stats.total, icon: Shield, color: 'text-indigo-600 bg-indigo-50' },
    { label: 'Assigned Roles', value: result.stats.assigned, icon: Users, color: 'text-emerald-600 bg-emerald-50' },
    { label: 'Unassigned Roles', value: result.stats.unassigned, icon: Briefcase, color: 'text-amber-600 bg-amber-50' },
  ];

  return (
    <div className="mx-auto max-w-7xl space-y-7">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"><div><h2 className="text-3xl font-bold text-slate-950">Employee Roles</h2><p className="mt-2 text-lg text-slate-500">Define and manage job roles and assignments.</p></div><button onClick={() => onNavigate('roles/new')} className="inline-flex h-12 items-center justify-center gap-2 rounded-xl bg-indigo-600 px-5 font-bold text-white shadow-lg shadow-indigo-200 transition hover:bg-indigo-700"><Plus className="h-5 w-5" />Add New Role</button></div>
      <div className="grid gap-5 md:grid-cols-3">{cards.map(({ label, value, icon: Icon, color }) => <div key={label} className="flex items-center justify-between rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><div><p className="text-sm text-slate-500">{label}</p><p className="mt-2 text-2xl font-bold text-slate-950">{value}</p></div><div className={`flex h-11 w-11 items-center justify-center rounded-xl ${color}`}><Icon className="h-5 w-5" /></div></div>)}</div>
      <div className="flex flex-col gap-4 rounded-3xl bg-white p-3 sm:flex-row sm:items-center"><div className="flex h-14 flex-1 items-center gap-3 rounded-2xl bg-slate-50 px-5 text-slate-400"><Search className="h-5 w-5" /><input type="search" value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search roles or descriptions..." className="h-full flex-1 bg-transparent text-sm font-medium text-slate-700 outline-none placeholder:text-slate-400" /></div><div className="flex gap-3"><div className="flex rounded-2xl bg-slate-50 p-1"><button title="Grid view" className="flex h-11 w-11 items-center justify-center rounded-xl bg-white text-indigo-600 shadow-sm"><Grid2X2 className="h-5 w-5" /></button><button title="List view" className="flex h-11 w-11 items-center justify-center rounded-xl text-slate-400"><List className="h-5 w-5" /></button></div><button className="flex h-12 items-center gap-2 rounded-2xl bg-slate-50 px-5 text-sm font-bold text-slate-600"><SlidersHorizontal className="h-4 w-4" />Filter</button></div></div>
      {isLoading ? <div className="rounded-2xl border border-slate-200 bg-white p-10 text-center font-semibold text-slate-500">Loading roles...</div> : error ? <div className="rounded-2xl border border-red-200 bg-red-50 p-10 text-center font-semibold text-red-700">{error}</div> : result.items.length === 0 ? <div className="rounded-2xl border border-slate-200 bg-white p-10 text-center font-semibold text-slate-500">No employee roles found.</div> : <motion.div layout className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">{result.items.map((role) => <RoleCard key={role.id} role={role} onAssign={setAssigningRole} />)}</motion.div>}
      <AnimatePresence>{showAddRole && <AddRoleDialog departments={departments} onClose={() => setShowAddRole(false)} onCreated={() => { setShowAddRole(false); setRefreshKey((value) => value + 1); }} />}</AnimatePresence>
      <AnimatePresence>{assigningRole && <AssignRoleDialog role={assigningRole} onClose={() => setAssigningRole(null)} onAssigned={() => { setAssigningRole(null); setRefreshKey((value) => value + 1); }} />}</AnimatePresence>
    </div>
  );
}
