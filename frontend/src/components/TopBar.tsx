import { Bell, Calendar, CheckCircle2, ChevronDown, Clock, Info, LogOut, Search, Settings, User, UserPlus, X } from 'lucide-react';
import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { AuthUser } from '../lib/api';
import { cn } from '../lib/utils';

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

const notifications = [
  {
    title: 'Leave Request Approved',
    message: 'Your annual leave request for April 15-20 has been approved by Sarah Chen.',
    time: '2 hours ago',
    unread: true,
    icon: CheckCircle2,
    color: 'text-emerald-500',
  },
  {
    title: 'New Team Member',
    message: 'Michael Scott has joined the Sales department as Regional Manager.',
    time: '5 hours ago',
    unread: true,
    icon: UserPlus,
    color: 'text-indigo-500',
  },
  {
    title: 'Upcoming Event',
    message: 'Quarterly Team Building is scheduled for next Friday at 2:00 PM.',
    time: '1 day ago',
    unread: false,
    icon: Calendar,
    color: 'text-orange-500',
  },
  {
    title: 'Attendance Reminder',
    message: 'Please remember to clock out for your lunch break.',
    time: '2 days ago',
    unread: false,
    icon: Clock,
    color: 'text-rose-500',
  },
  {
    title: 'Policy Update',
    message: 'The Remote Work Policy has been updated. Please review the changes.',
    time: '3 days ago',
    unread: false,
    icon: Info,
    color: 'text-slate-500',
  },
];

export default function TopBar({ user, userRole, onNavigate, onLogout }: TopBarProps) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isNotificationsOpen, setIsNotificationsOpen] = useState(false);
  const displayName = user?.name ?? (userRole === 'employee' ? 'Employee User' : 'Admin User');
  const initials = initialsFor(displayName) || (userRole === 'employee' ? 'EM' : 'AD');
  const title = userRole === 'employee' ? 'Product Designer' : user?.role ?? 'HR Director';
  const unreadCount = notifications.filter((notification) => notification.unread).length;

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
        <button
          onClick={() => setIsNotificationsOpen(true)}
          className="relative flex h-11 w-11 items-center justify-center rounded-xl text-slate-500 transition hover:bg-slate-50 hover:text-slate-900"
        >
          <Bell className="h-5 w-5" />
          {unreadCount > 0 && <span className="absolute right-3 top-2 h-2 w-2 rounded-full bg-rose-500" />}
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

          <AnimatePresence>
            {isMenuOpen && (
            <motion.div
              animate={{ opacity: 1, scale: 1, y: 0 }}
              className="absolute right-0 mt-3 w-56 origin-top-right overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-xl shadow-slate-200"
              exit={{ opacity: 0, scale: 0.96, y: -8 }}
              initial={{ opacity: 0, scale: 0.96, y: -8 }}
              transition={{ duration: 0.16, ease: 'easeOut' }}
            >
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
            </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      <AnimatePresence>
        {isNotificationsOpen && (
          <>
            <motion.button
              aria-label="Close notifications"
              className="fixed inset-0 z-40 cursor-default bg-slate-950/20 backdrop-blur-sm"
              initial={{ opacity: 0, backdropFilter: 'blur(0px)' }}
              animate={{ opacity: 1, backdropFilter: 'blur(8px)' }}
              exit={{ opacity: 0, backdropFilter: 'blur(0px)' }}
              transition={{ duration: 0.2 }}
              onClick={() => setIsNotificationsOpen(false)}
            />
            <motion.aside
              animate={{ opacity: 1, x: 0 }}
              className="fixed right-0 top-0 z-50 flex h-screen w-full max-w-md flex-col bg-white shadow-2xl shadow-slate-900/20"
              exit={{ opacity: 0, x: 40 }}
              initial={{ opacity: 0, x: 80 }}
              transition={{ duration: 0.24, ease: 'easeOut' }}
            >
              <div className="flex items-center justify-between border-b border-slate-100 p-6">
                <div className="flex items-center gap-4">
                  <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-indigo-50 text-indigo-600">
                    <Bell className="h-6 w-6" />
                  </div>
                  <div>
                    <h2 className="text-xl font-bold text-slate-950">Notifications</h2>
                    <p className="text-sm text-slate-500">You have {unreadCount} unread messages</p>
                  </div>
                </div>
                <button
                  onClick={() => setIsNotificationsOpen(false)}
                  className="rounded-xl p-2 text-slate-400 transition hover:bg-slate-50 hover:text-slate-900"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>

              <div className="flex items-center justify-between border-b border-slate-100 px-6 py-4 text-sm font-bold">
                <button className="text-indigo-600">Mark all as read</button>
                <button className="text-slate-500">Clear all</button>
              </div>

              <div className="flex-1 space-y-4 overflow-y-auto p-6">
                {notifications.map((notification, index) => {
                  const Icon = notification.icon;
                  return (
                    <motion.article
                      key={notification.title}
                      animate={{ opacity: 1, x: 0 }}
                      className="relative rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
                      initial={{ opacity: 0, x: 24 }}
                      transition={{ delay: index * 0.04, duration: 0.2 }}
                    >
                      {notification.unread && <span className="absolute right-5 top-5 h-2 w-2 rounded-full bg-indigo-600" />}
                      <div className="flex gap-4">
                        <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-slate-50">
                          <Icon className={cn('h-5 w-5', notification.color)} />
                        </div>
                        <div>
                          <h3 className="font-bold text-slate-950">{notification.title}</h3>
                          <p className="mt-2 leading-6 text-slate-500">{notification.message}</p>
                          <div className="mt-3 flex items-center gap-2 text-xs font-bold uppercase text-slate-400">
                            <Clock className="h-3.5 w-3.5" />
                            {notification.time}
                          </div>
                        </div>
                      </div>
                    </motion.article>
                  );
                })}
              </div>

              <div className="border-t border-slate-100 p-6">
                <button className="h-12 w-full rounded-xl border border-slate-200 bg-white font-bold text-slate-600 shadow-sm transition hover:bg-slate-50">
                  View All Notifications
                </button>
              </div>
            </motion.aside>
          </>
        )}
      </AnimatePresence>
    </header>
  );
}
