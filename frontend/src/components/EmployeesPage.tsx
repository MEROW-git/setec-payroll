import { Briefcase, Calendar, Grid2X2, List, Mail, MoreVertical, Plus, Search, SlidersHorizontal } from 'lucide-react';
import { useEffect, useMemo, useState } from 'react';
import { EmployeeListItem, getEmployees } from '../lib/api';
import { cn } from '../lib/utils';

function statusLabel(status: string) {
  return status
    .split('_')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

function initialsFor(name: string) {
  return name
    .split(' ')
    .map((part) => part[0])
    .join('')
    .slice(0, 2)
    .toUpperCase();
}

function EmployeeCard({ employee }: { employee: EmployeeListItem }) {
  const isActive = employee.status === 'active';

  return (
    <article className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div className="p-6">
        <div className="mb-6 flex items-start justify-between">
          {employee.profile_photo ? (
            <img
              alt={employee.name}
              className="h-16 w-16 rounded-xl object-cover"
              src={employee.profile_photo}
            />
          ) : (
            <div className="flex h-16 w-16 items-center justify-center rounded-xl bg-indigo-100 text-lg font-bold text-indigo-700">
              {initialsFor(employee.name)}
            </div>
          )}
          <button className="rounded-lg p-1 text-slate-400 transition hover:bg-slate-50 hover:text-slate-700">
            <MoreVertical className="h-5 w-5" />
          </button>
        </div>

        <h3 className="text-xl font-bold text-slate-950">{employee.name}</h3>
        <p className="mt-1 text-sm font-medium text-slate-500">{employee.position ?? 'Unassigned'}</p>

        <div className="mt-5 space-y-3 text-sm text-slate-600">
          <div className="flex items-center gap-3">
            <Briefcase className="h-4 w-4 text-slate-400" />
            <span>{employee.department ?? 'No department'}</span>
          </div>
          <div className="flex items-center gap-3">
            <Mail className="h-4 w-4 text-slate-400" />
            <span>{employee.email ?? 'No email'}</span>
          </div>
          <div className="flex items-center gap-3">
            <Calendar className="h-4 w-4 text-slate-400" />
            <span>Joined {employee.hire_date ?? 'Unknown'}</span>
          </div>
        </div>
      </div>

      <div className="flex items-center justify-between border-t border-slate-100 bg-slate-50 px-6 py-4">
        <span
          className={cn(
            'rounded-full px-3 py-1 text-xs font-bold',
            isActive ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700',
          )}
        >
          {statusLabel(employee.status)}
        </span>
        <button className="text-sm font-bold text-indigo-600">View Profile</button>
      </div>
    </article>
  );
}

type EmployeesPageProps = {
  onNavigate: (tab: string) => void;
};

export default function EmployeesPage({ onNavigate }: EmployeesPageProps) {
  const [employees, setEmployees] = useState<EmployeeListItem[]>([]);
  const [search, setSearch] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const timer = window.setTimeout(() => {
      setIsLoading(true);
      setError('');
      getEmployees({ search, per_page: 24 })
        .then((result) => setEmployees(result.items))
        .catch((requestError) => {
          setError(requestError instanceof Error ? requestError.message : 'Unable to load employees.');
        })
        .finally(() => setIsLoading(false));
    }, 250);

    return () => window.clearTimeout(timer);
  }, [search]);

  const emptyMessage = useMemo(() => {
    if (isLoading) return 'Loading employees...';
    if (error) return error;
    return 'No employees found.';
  }, [error, isLoading]);

  return (
    <div className="mx-auto max-w-7xl space-y-7">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-3xl font-bold text-slate-950">Employee Directory</h2>
          <p className="mt-2 text-lg text-slate-500">Manage and view all team members in one place.</p>
        </div>
        <button
          onClick={() => onNavigate('add-employee')}
          className="inline-flex h-12 items-center justify-center gap-2 rounded-xl bg-indigo-600 px-5 font-bold text-white shadow-lg shadow-indigo-200 transition hover:bg-indigo-700"
        >
          <Plus className="h-5 w-5" />
          Add New Employee
        </button>
      </div>

      <div className="flex flex-col gap-4 rounded-3xl bg-white p-3 sm:flex-row sm:items-center">
        <div className="flex h-14 flex-1 items-center gap-3 rounded-2xl bg-slate-50 px-5 text-slate-400">
          <Search className="h-5 w-5" />
          <input
            className="h-full flex-1 bg-transparent text-sm font-medium text-slate-700 outline-none placeholder:text-slate-400"
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Search by Employee name, id, role and department"
            type="search"
            value={search}
          />
        </div>
        <div className="flex gap-3">
          <div className="flex rounded-2xl bg-slate-50 p-1">
            <button className="flex h-11 w-11 items-center justify-center rounded-xl bg-white text-indigo-600 shadow-sm">
              <Grid2X2 className="h-5 w-5" />
            </button>
            <button className="flex h-11 w-11 items-center justify-center rounded-xl text-slate-400">
              <List className="h-5 w-5" />
            </button>
          </div>
          <button className="flex h-12 items-center gap-2 rounded-2xl bg-slate-50 px-5 text-sm font-bold text-slate-600">
            <SlidersHorizontal className="h-4 w-4" />
            Filter
          </button>
        </div>
      </div>

      {employees.length === 0 ? (
        <div className="rounded-2xl border border-slate-200 bg-white p-10 text-center font-semibold text-slate-500">
          {emptyMessage}
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
          {employees.map((employee) => (
            <EmployeeCard employee={employee} key={employee.id} />
          ))}
        </div>
      )}
    </div>
  );
}
