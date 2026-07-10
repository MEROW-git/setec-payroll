import { Bell, ChevronDown, LogOut, Search, Settings, User } from 'lucide-react';
import { useState } from 'react';
import { AuthUser } from '../lib/api';

type TopBarProps = {
  user: AuthUser | null;
  userRole: 'admin' | 'employee';
  onNavigate: (tab: string) => void;
  onLogout: () => void;
};

function initialsFor(name: string) {
  return name
    .split(' ')
    .map((part) => part[0])
    .join('')
    .slice(0, 2)
    .toUpperCase();
}

export default function TopBar({ user, userRole, onNavigate, onLogout }: TopBarProps) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const displayName = user?.name ?? (userRole === 'employee' ? 'Employee User' : 'Admin User');
  const initials = initialsFor(displayName) || (userRole === 'employee' ? 'EM' : 'AD');
  const title = userRole === 'employee' ? 'Product Designer' : user?.role ?? 'HR Director';

  return (
    <header className="sticky top-0 z-30 flex h-20 items-center justify-between border-b border-slate-200 bg-white px-8">
      <div className="flex h-12 w-full max-w-md items-center gap-3 rounded-2xl bg-slate-50 px-4 text-slate-400">
        <Search className="h-5 w-5" />
        <input
          className="h-full flex-1 bg-transparent text-sm text-slate-700 outline-none placeholder:text-slate-400"
          placeholder="Search anything..."
          type="search"
        />
      </div>

      <div className="flex items-center gap-5">
        <button className="relative flex h-11 w-11 items-center justify-center rounded-xl text-slate-500 transition hover:bg-slate-50 hover:text-slate-900">
          <Bell className="h-5 w-5" />
          <span className="absolute right-3 top-2 h-2 w-2 rounded-full bg-rose-500" />
        </button>

        <div className="h-9 w-px bg-slate-200" />

        <div className="relative">
          <button
            onClick={() => setIsMenuOpen((value) => !value)}
            className="flex items-center gap-3 rounded-2xl px-2 py-1.5 transition hover:bg-slate-50"
          >
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-indigo-100 text-sm font-bold text-indigo-700">
              {initials}
            </div>
            <div className="hidden text-left sm:block">
              <p className="text-sm font-bold text-slate-950">{displayName}</p>
              <p className="text-xs text-slate-500">{title}</p>
            </div>
            <ChevronDown className={`h-4 w-4 text-slate-400 transition ${isMenuOpen ? 'rotate-180' : ''}`} />
          </button>

          {isMenuOpen && (
            <div className="absolute right-0 mt-3 w-56 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-xl shadow-slate-200">
              <button
                onClick={() => {
                  onNavigate('profile');
                  setIsMenuOpen(false);
                }}
                className="flex w-full items-center gap-3 px-5 py-4 text-left text-sm font-medium text-slate-600 transition hover:bg-slate-50"
              >
                <User className="h-4 w-4" />
                View Profile
              </button>
              <button
                onClick={() => {
                  onNavigate('settings');
                  setIsMenuOpen(false);
                }}
                className="flex w-full items-center gap-3 px-5 py-4 text-left text-sm font-medium text-slate-600 transition hover:bg-slate-50"
              >
                <Settings className="h-4 w-4" />
                Account Settings
              </button>
              <button
                onClick={onLogout}
                className="flex w-full items-center gap-3 border-t border-slate-100 px-5 py-4 text-left text-sm font-bold text-rose-600 transition hover:bg-rose-50"
              >
                <LogOut className="h-4 w-4" />
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
