import { ArrowLeft, Building2, DollarSign, FileText, Save, UserRound } from 'lucide-react';
import { FormEvent, useEffect, useMemo, useState } from 'react';
import { createDepartment, EmployeeListItem, getEmployees } from '../lib/api';

function codeFromName(name: string) {
  return name.toUpperCase().replace(/[^A-Z0-9]+/g, '_').replace(/^_|_$/g, '').slice(0, 30);
}

export default function CreateDepartmentPage({ onNavigate }: { onNavigate: (path: string) => void }) {
  const [employees, setEmployees] = useState<EmployeeListItem[]>([]);
  const [name, setName] = useState('');
  const [code, setCode] = useState('');
  const [managerId, setManagerId] = useState('');
  const [budget, setBudget] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  const suggestedCode = useMemo(() => code || codeFromName(name), [code, name]);

  useEffect(() => { getEmployees({ per_page: 100 }).then((data) => setEmployees(data.items)).catch(() => setError('Unable to load manager options.')); }, []);

  const submit = async (event: FormEvent) => {
    event.preventDefault(); setError(''); setIsSaving(true);
    try {
      await createDepartment({ name, code: suggestedCode, description, manager_employee_id: managerId ? Number(managerId) : undefined, annual_budget: budget ? Number(budget) : undefined });
      onNavigate('departments');
    } catch (requestError) { setError(requestError instanceof Error ? requestError.message : 'Unable to create department.'); }
    finally { setIsSaving(false); }
  };

  const inputShell = 'mt-2 flex h-12 items-center gap-3 rounded-xl border border-slate-200 bg-slate-50 px-4 text-slate-400 focus-within:border-indigo-400 focus-within:ring-2 focus-within:ring-indigo-100';
  return (
    <form onSubmit={submit} className="mx-auto max-w-3xl space-y-8">
      <div className="flex items-start gap-5"><button type="button" title="Back to departments" onClick={() => onNavigate('departments')} className="mt-1 rounded-lg p-2 text-slate-500 transition hover:bg-white hover:text-indigo-600"><ArrowLeft className="h-5 w-5" /></button><div><h2 className="text-3xl font-bold text-slate-950">Add New Department</h2><p className="mt-2 text-lg text-slate-500">Create a new organizational unit for your company.</p></div></div>
      <section className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <label className="block text-sm font-bold text-slate-800">Department Name<span className={inputShell}><Building2 className="h-5 w-5" /><input required maxLength={150} value={name} onChange={(event) => setName(event.target.value)} placeholder="e.g. Engineering, Marketing" className="h-full flex-1 bg-transparent font-normal text-slate-800 outline-none" /></span></label>
        <label className="mt-6 block text-sm font-bold text-slate-800">Department Code <span className="font-medium text-slate-400">(optional)</span><span className={inputShell}><Building2 className="h-5 w-5" /><input maxLength={30} value={code} onChange={(event) => setCode(event.target.value.toUpperCase().replace(/[^A-Z0-9_-]/g, ''))} placeholder={codeFromName(name) || 'e.g. ENG'} className="h-full flex-1 bg-transparent font-normal uppercase text-slate-800 outline-none" /></span></label>
        <label className="mt-6 block text-sm font-bold text-slate-800">Department Manager <span className="font-medium text-slate-400">(optional)</span><span className={inputShell}><UserRound className="h-5 w-5" /><select value={managerId} onChange={(event) => setManagerId(event.target.value)} className="h-full flex-1 bg-transparent font-normal text-slate-800 outline-none"><option value="">Select a manager...</option>{employees.map((employee) => <option key={employee.id} value={employee.id}>{employee.name} — {employee.position ?? 'No role'}</option>)}</select></span></label>
        <label className="mt-6 block text-sm font-bold text-slate-800">Annual Budget ($) <span className="font-medium text-slate-400">(optional)</span><span className={inputShell}><DollarSign className="h-5 w-5" /><input type="number" min="0" step="0.01" value={budget} onChange={(event) => setBudget(event.target.value)} placeholder="e.g. 500000" className="h-full flex-1 bg-transparent font-normal text-slate-800 outline-none" /></span></label>
        <label className="mt-6 block text-sm font-bold text-slate-800">Description <span className="font-medium text-slate-400">(optional)</span><span className="mt-2 flex items-start gap-3 rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-400"><FileText className="mt-1 h-5 w-5" /><textarea rows={4} value={description} onChange={(event) => setDescription(event.target.value)} placeholder="Describe the department's core responsibilities..." className="w-full resize-none bg-transparent font-normal text-slate-800 outline-none" /></span></label>
        {error && <p className="mt-5 rounded-xl bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">{error}</p>}
        <div className="mt-8 grid grid-cols-2 gap-4"><button type="button" onClick={() => onNavigate('departments')} className="h-12 rounded-xl bg-slate-100 font-bold text-slate-700">Cancel</button><button disabled={isSaving || !suggestedCode} className="flex h-12 items-center justify-center gap-2 rounded-xl bg-indigo-600 font-bold text-white shadow-lg shadow-indigo-200 disabled:bg-slate-300"><Save className="h-5 w-5" />{isSaving ? 'Creating...' : 'Create Department'}</button></div>
      </section>
    </form>
  );
}
