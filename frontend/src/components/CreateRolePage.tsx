import { ArrowLeft, Building2, CheckCircle2, FileText, Plus, Shield, X } from 'lucide-react';
import { FormEvent, KeyboardEvent, useEffect, useState } from 'react';
import { createPosition, Department, getDepartments } from '../lib/api';

export default function CreateRolePage({ onNavigate }: { onNavigate: (path: string) => void }) {
  const [departments, setDepartments] = useState<Department[]>([]);
  const [title, setTitle] = useState('');
  const [departmentId, setDepartmentId] = useState('');
  const [description, setDescription] = useState('');
  const [permission, setPermission] = useState('');
  const [permissions, setPermissions] = useState<string[]>([]);
  const [error, setError] = useState('');
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => { getDepartments().then(setDepartments).catch(() => setError('Unable to load departments.')); }, []);

  const addPermission = () => {
    const value = permission.trim();
    if (value && !permissions.includes(value)) setPermissions((items) => [...items, value]);
    setPermission('');
  };

  const handlePermissionKey = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') { event.preventDefault(); addPermission(); }
  };

  const submit = async (event: FormEvent) => {
    event.preventDefault(); setError(''); setIsSaving(true);
    try {
      await createPosition({ title, department_id: Number(departmentId), description, permissions });
      onNavigate('roles');
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Unable to create role.');
    } finally { setIsSaving(false); }
  };

  return (
    <form onSubmit={submit} className="mx-auto max-w-4xl space-y-8">
      <div className="flex items-start gap-5"><button type="button" title="Back to roles" onClick={() => onNavigate('roles')} className="mt-1 rounded-lg p-2 text-slate-500 transition hover:bg-white hover:text-indigo-600"><ArrowLeft className="h-5 w-5" /></button><div><h2 className="text-3xl font-bold text-slate-950">Create New Role</h2><p className="mt-2 text-lg text-slate-500">Define a new job role and its associated permissions.</p></div></div>
      <section className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <div className="grid gap-6 md:grid-cols-2">
          <label className="text-sm font-bold text-slate-800">Role Name<span className="mt-2 flex h-12 items-center gap-3 rounded-xl bg-slate-50 px-4 text-slate-400"><Shield className="h-5 w-5" /><input required maxLength={150} value={title} onChange={(event) => setTitle(event.target.value)} placeholder="e.g. Senior Frontend Developer" className="h-full flex-1 bg-transparent font-normal text-slate-800 outline-none" /></span></label>
          <label className="text-sm font-bold text-slate-800">Department<span className="mt-2 flex h-12 items-center gap-3 rounded-xl bg-slate-50 px-4 text-slate-400"><Building2 className="h-5 w-5" /><select required value={departmentId} onChange={(event) => setDepartmentId(event.target.value)} className="h-full flex-1 bg-transparent font-normal text-slate-800 outline-none"><option value="">Select Department</option>{departments.map((department) => <option key={department.id} value={department.id}>{department.name}</option>)}</select></span></label>
        </div>
        <label className="mt-7 block text-sm font-bold text-slate-800">Description <span className="font-medium text-slate-400">(optional)</span><span className="mt-2 flex items-start gap-3 rounded-xl bg-slate-50 px-4 py-3 text-slate-400"><FileText className="mt-1 h-5 w-5 shrink-0" /><textarea rows={4} value={description} onChange={(event) => setDescription(event.target.value)} placeholder="Describe the responsibilities and requirements for this role..." className="w-full resize-none bg-transparent font-normal text-slate-800 outline-none" /></span></label>
        <div className="my-8 border-t border-slate-100" />
        <h3 className="text-lg font-bold text-slate-950">Permissions & Access</h3>
        <div className="mt-4 flex gap-3"><input value={permission} onChange={(event) => setPermission(event.target.value)} onKeyDown={handlePermissionKey} placeholder="Add a permission (e.g. Code Access, Payroll, etc.)" className="h-12 flex-1 rounded-xl bg-slate-50 px-4 outline-none focus:ring-2 focus:ring-indigo-100" /><button type="button" onClick={addPermission} className="flex h-12 items-center gap-2 rounded-xl bg-slate-900 px-6 font-bold text-white"><Plus className="h-5 w-5" />Add</button></div>
        <div className="mt-4 flex min-h-8 flex-wrap gap-2">{permissions.length === 0 ? <p className="text-sm italic text-slate-400">No permissions added yet.</p> : permissions.map((item) => <span key={item} className="flex items-center gap-2 rounded-lg bg-indigo-50 px-3 py-2 text-xs font-bold text-indigo-700">{item}<button type="button" title={`Remove ${item}`} onClick={() => setPermissions((values) => values.filter((value) => value !== item))}><X className="h-3.5 w-3.5" /></button></span>)}</div>
        {error && <p className="mt-5 rounded-xl bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">{error}</p>}
      </section>
      <footer className="flex justify-end gap-4 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><button type="button" onClick={() => onNavigate('roles')} className="h-11 rounded-xl border border-slate-200 px-6 text-sm font-bold text-slate-600">Cancel</button><button disabled={isSaving || departments.length === 0} className="flex h-11 items-center gap-2 rounded-xl bg-indigo-600 px-7 text-sm font-bold text-white shadow-lg shadow-indigo-200 disabled:bg-slate-300">{isSaving ? 'Creating...' : 'Create Role'}<CheckCircle2 className="h-4 w-4" /></button></footer>
    </form>
  );
}
