import {
  LayoutDashboard,
  Users,
  Building2,
  CalendarClock,
  CreditCard,
  BarChart3,
  Settings,

  ClipboardCheck,
  Calendar,
  Shield,
  Clock,
  Wallet,
  FileText
} from 'lucide-react';
import { cn } from '../lib/utils';
import { motion } from 'framer-motion';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  userRole: 'admin' | 'employee';
}

export default function Sidebar({ activeTab, setActiveTab, userRole }: SidebarProps) {
  const adminNavItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'employees', label: 'Employees', icon: Users },
    { id: 'roles', label: 'Roles', icon: Shield },
    { id: 'departments', label: 'Departments', icon: Building2 },
    { id: 'attendance', label: 'Attendance', icon: ClipboardCheck },
    { id: 'shift', label: 'Shift', icon: Clock },
    { id: 'leave', label: 'Leave Tracking', icon: Calendar },
    { id: 'events-schedule', label: 'Events & Schedule', icon: CalendarClock },
    { id: 'payroll', label: 'Payroll', icon: CreditCard },
    { id: 'performance', label: 'Performance', icon: BarChart3 },
  ];

  const employeeNavItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'attendance', label: 'Attendance', icon: ClipboardCheck },
    { id: 'shift', label: 'Shift', icon: Clock },
    { id: 'leave', label: 'Leave Tracking', icon: Calendar },
    { id: 'allowance-deduction', label: 'Allowance & Deduction', icon: Wallet },
    { id: 'events-schedule', label: 'Events & Schedule', icon: CalendarClock },
    { id: 'reports', label: 'Reports', icon: FileText },
  ];

  const navItems = userRole === 'employee' ? employeeNavItems : adminNavItems;

  return (
    <div className="w-64 bg-white border-r border-slate-200 h-screen flex flex-col sticky top-0">
      <div className="p-6 flex items-center gap-3">
        <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center text-white font-bold text-lg">
          SH
        </div>
        <h1 className="text-xl font-bold text-slate-900 tracking-tight">Siegecode HRM</h1>
      </div>

      <nav className="flex-1 px-4 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id || activeTab.startsWith(`${item.id}/`);

          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={cn(
                "w-full flex items-center justify-between px-4 py-3 rounded-lg transition-all duration-200 group",
                isActive
                  ? "bg-indigo-50 text-indigo-700 shadow-sm"
                  : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
              )}
            >
              <div className="flex items-center gap-3">
                <Icon className={cn(
                  "w-5 h-5 transition-colors",
                  isActive ? "text-indigo-600" : "text-slate-400 group-hover:text-slate-600"
                )} />
                <span className="font-medium">{item.label}</span>
              </div>
              {isActive && (
                <motion.div
                  layoutId="activeTab"
                  className="w-1.5 h-1.5 bg-indigo-600 rounded-full"
                />
              )}
            </button>
          );
        })}
      </nav>

      <div className="p-4 border-t border-slate-100 space-y-1">
        <button
          onClick={() => setActiveTab('settings')}
          className={cn(
            "w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors group",
            activeTab === 'settings' ? "bg-indigo-50 text-indigo-700 shadow-sm" : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
          )}
        >
          <Settings className={cn(
            "w-5 h-5 transition-colors",
            activeTab === 'settings' ? "text-indigo-600" : "text-slate-400 group-hover:text-slate-600"
          )} />
          <span className="font-medium">Settings</span>
        </button>
      </div>
    </div>
  );
}
