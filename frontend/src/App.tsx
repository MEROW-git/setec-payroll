import { useEffect, useState } from 'react';
import { ArrowRight, Lock, Mail, ShieldCheck } from 'lucide-react';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import EmployeeDashboard from './components/EmployeeDashboard';
import EmployeesPage from './components/EmployeesPage';
import ProfilePage from './components/ProfilePage';
import RolesPage from './components/RolesPage';
import DepartmentsPage from './components/DepartmentsPage';
import CreateRolePage from './components/CreateRolePage';
import CreateDepartmentPage from './components/CreateDepartmentPage';
import AttendancePage from './components/AttendancePage';
import AttendancePolicyPage from './components/AttendancePolicyPage';
import ShiftPage from './components/ShiftPage';
import LeavePage from './components/LeavePage';
import LeaveSettingsPage from './components/LeaveSettingsPage';
import LeaveConfigPage from './components/LeaveConfigPage';
import AdjustmentsPage from './components/AdjustmentsPage';
import EventsPage from './components/EventsPage';
import CreateSchedulePage from './components/CreateSchedulePage';
import PayrollPage from './components/PayrollPage';
import PayrollSettingsPage from './components/PayrollSettingsPage';
import PayrollConfigPage from './components/PayrollConfigPage';
import PayrollUtilityPage from './components/PayrollUtilityPage';
import ReportsPage from './components/ReportsPage';
import PerformancePage from './components/PerformancePage';
import SettingsPage from './components/SettingsPage';
import TopBar from './components/TopBar';
import { AuthUser, getCurrentUser, login, logout } from './lib/api';
import AddEmployeePage from './components/AddEmployeePage';

type UserRole = 'admin' | 'employee';

function roleFromUser(user: AuthUser | null): UserRole {
  return user?.role === 'Employee' ? 'employee' : 'admin';
}

function tabFromPath(pathname: string) {
  const tab = pathname.replace(/^\/+/, '') || 'dashboard';
  return tab === 'login' ? 'dashboard' : tab;
}

function pathForTab(tab: string) {
  return `/${tab}`;
}

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authUser, setAuthUser] = useState<AuthUser | null>(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loginError, setLoginError] = useState('');
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);
  const userRole = roleFromUser(authUser);

  useEffect(() => {
    try {
      const appearance = JSON.parse(localStorage.getItem('appearance') ?? '{}');
      const dark = appearance.theme === 'dark' || (appearance.theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);
      document.documentElement.dataset.theme = dark ? 'dark' : 'light';
      document.documentElement.dataset.density = appearance.density === 'compact' ? 'compact' : 'comfortable';
    } catch {
      document.documentElement.dataset.theme = 'light';
    }

    const verifySession = async () => {
      const savedToken = localStorage.getItem('access_token');

      if (!savedToken) {
        window.history.replaceState({ tab: 'login' }, '', '/login');
        setIsCheckingAuth(false);
        return;
      }

      try {
        const user = await getCurrentUser();
        localStorage.setItem('auth_user', JSON.stringify(user));
        setAuthUser(user);
        setIsAuthenticated(true);

        if (window.location.pathname === '/' || window.location.pathname === '/login') {
          window.history.replaceState({ tab: 'dashboard' }, '', '/dashboard');
          setActiveTab('dashboard');
        } else {
          setActiveTab(tabFromPath(window.location.pathname));
        }
      } catch {
        localStorage.removeItem('access_token');
        localStorage.removeItem('auth_user');
        setAuthUser(null);
        setIsAuthenticated(false);
        window.history.replaceState({ tab: 'login' }, '', '/login');
      } finally {
        setIsCheckingAuth(false);
      }
    };

    void verifySession();

    const handlePopState = () => {
      if (window.location.pathname === '/login') {
        localStorage.removeItem('access_token');
        localStorage.removeItem('auth_user');
        setAuthUser(null);
        setIsAuthenticated(false);
        setActiveTab('dashboard');
        return;
      }

      setActiveTab(tabFromPath(window.location.pathname));
    };

    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  const navigateTo = (tab: string) => {
    setActiveTab(tab);
    window.history.pushState({ tab }, '', pathForTab(tab));
  };

  const handleLogin = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoginError('');
    setIsLoggingIn(true);

    try {
      const result = await login(email, password);
      localStorage.setItem('access_token', result.access_token);
      localStorage.setItem('auth_user', JSON.stringify(result.user));
      setAuthUser(result.user);
      setActiveTab('dashboard');
      setIsAuthenticated(true);
      window.history.pushState({ tab: 'dashboard' }, '', '/dashboard');
    } catch (error) {
      setLoginError(error instanceof Error ? error.message : 'Unable to sign in.');
    } finally {
      setIsLoggingIn(false);
    }
  };

  const handleLogout = () => {
    void logout().catch(() => undefined);
    localStorage.removeItem('access_token');
    localStorage.removeItem('auth_user');
    setAuthUser(null);
    setActiveTab('dashboard');
    setIsAuthenticated(false);
    window.history.pushState({ tab: 'login' }, '', '/login');
  };

  const renderContent = () => {
    if (activeTab === 'departments/new') {
      return <CreateDepartmentPage onNavigate={navigateTo} />;
    }

    if (activeTab === 'departments' || activeTab.startsWith('departments/')) {
      const departmentId = activeTab.startsWith('departments/') ? Number(activeTab.split('/')[1]) : undefined;
      return <DepartmentsPage departmentId={departmentId} onNavigate={navigateTo} />;
    }

    switch (activeTab) {
      case 'dashboard':
        return userRole === 'employee' ? (
          <EmployeeDashboard userName={authUser?.name ?? 'Employee User'} />
        ) : (
          <Dashboard onNavigate={navigateTo} />
        );
      case 'employees':
        return <EmployeesPage onNavigate={navigateTo} />;
      case 'add-employee':
        return <AddEmployeePage onNavigate={navigateTo} />;
      case 'profile':
        return <ProfilePage user={authUser} />;
      case 'roles':
        return <RolesPage onNavigate={navigateTo} />;
      case 'roles/new':
        return <CreateRolePage onNavigate={navigateTo} />;
      case 'attendance':
        return <AttendancePage onNavigate={navigateTo} />;
      case 'attendance/policy':
        return <AttendancePolicyPage onNavigate={navigateTo} />;
      case 'shift':
        return <ShiftPage />;
      case 'leave':
        return <LeavePage onNavigate={navigateTo} />;
      case 'leave/settings':
        return <LeaveSettingsPage onNavigate={navigateTo} />;
      case 'allowance-deduction':
        return <AdjustmentsPage />;
      case 'events-schedule':
        return <EventsPage onNavigate={navigateTo} />;
      case 'events-schedule/new-event':
        return <CreateSchedulePage mode="event" onNavigate={navigateTo} />;
      case 'events-schedule/new-notice':
        return <CreateSchedulePage mode="notice" onNavigate={navigateTo} />;
      case 'payroll':
        return <PayrollPage onNavigate={navigateTo} />;
      case 'payroll/settings':
        return <PayrollSettingsPage onNavigate={navigateTo} />;
      case 'reports':
        return <ReportsPage />;
      case 'performance':
        return <PerformancePage />;
      case 'settings':
        return <SettingsPage user={authUser} onUserUpdated={(user)=>{setAuthUser(user);localStorage.setItem('auth_user',JSON.stringify(user));}} />;
      default:
        if (activeTab.startsWith('payroll/settings/')) {
          const kind = activeTab.split('/')[2];
          if (kind === 'bank' || kind === 'payslip' || kind === 'salary-list') {
            return <PayrollUtilityPage mode={kind} onNavigate={navigateTo} />;
          }
          return <PayrollConfigPage kind={kind} onNavigate={navigateTo} />;
        }
        if (activeTab.startsWith('leave/settings/')) {
          return <LeaveConfigPage kind={activeTab.split('/')[2]} onNavigate={navigateTo} />;
        }
        return (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <h2 className="text-2xl font-bold text-slate-900 mb-2">{activeTab.charAt(0).toUpperCase() + activeTab.slice(1)} Page</h2>
              <p className="text-slate-500">
                {userRole === 'employee'
                  ? 'This employee self-service page is under development.'
                  : 'This page is under development.'}
              </p>
            </div>
          </div>
        );
    }
  };

  if (isCheckingAuth) {
    return <div className="min-h-screen bg-slate-50" />;
  }

  if (!isAuthenticated) {
    return (
      <div className="grid min-h-screen bg-slate-50 lg:grid-cols-2">
        <section className="relative hidden overflow-hidden bg-blue-600 lg:flex lg:items-center lg:justify-center">
          <div className="login-orbit login-orbit-slow absolute h-[520px] w-[520px] rounded-full border border-white/10 bg-white/5" />
          <div className="login-orbit login-orbit-fast absolute h-[340px] w-[340px] rounded-full bg-white/5" />
          <div className="login-spark login-spark-one" />
          <div className="login-spark login-spark-two" />
          <div className="login-spark login-spark-three" />
          <div className="relative z-10 flex max-w-lg flex-col items-center px-10 text-center text-white">
            <div className="login-float mb-12 flex h-24 w-24 items-center justify-center rounded-3xl border-2 border-white/80 bg-white/10">
              <ShieldCheck className="h-14 w-14" strokeWidth={1.8} />
            </div>
            <div className="login-card-float mb-14 rounded-[2rem] border-8 border-slate-950 bg-blue-500 p-8 shadow-2xl">
              <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-full bg-white">
                <ShieldCheck className="login-icon-pulse h-9 w-9 text-blue-600" />
              </div>
              <div className="space-y-3">
                <div className="h-3 w-44 rounded-full bg-white/90" />
                <div className="h-3 w-44 rounded-full bg-white/90" />
                <div className="login-scan mx-auto h-3 w-16 rounded-full bg-orange-400" />
              </div>
              <div className="mx-auto mt-10 flex h-16 w-14 items-center justify-center rounded-xl bg-white">
                <Lock className="h-8 w-8 text-blue-600" />
              </div>
            </div>
            <h1 className="text-4xl font-bold">Secure HR Management</h1>
            <p className="mt-5 max-w-md text-xl leading-8 text-blue-50">
              Your data is protected with enterprise-grade security. Sign in to manage your workforce efficiently.
            </p>
          </div>
        </section>

        <main className="flex items-center justify-center px-6 py-12">
          <div className="w-full max-w-md">
            <div className="mb-9 flex items-center gap-6">
              <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-600 text-white shadow-lg shadow-blue-600/20">
                <ShieldCheck className="h-9 w-9" />
              </div>
              <div>
                <h2 className="text-3xl font-bold text-slate-950">Welcome Back</h2>
                <p className="mt-2 text-lg text-slate-500">Please enter your details to sign in</p>
              </div>
            </div>

            <form onSubmit={handleLogin} className="rounded-3xl border border-slate-200 bg-white p-8 shadow-xl shadow-slate-200/70">
              <label className="block">
                <span className="text-sm font-bold text-slate-800">Email Address</span>
                <span className="mt-2 flex h-14 items-center gap-4 rounded-2xl border border-slate-200 bg-slate-50 px-4 text-slate-500">
                  <Mail className="h-5 w-5" />
                  <input
                    className="h-full flex-1 bg-transparent text-slate-950 outline-none"
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    placeholder="admin@example.com"
                    type="email"
                    required
                  />
                </span>
              </label>

              <label className="mt-6 block">
                <span className="flex items-center justify-between text-sm font-bold text-slate-800">
                  <span>Password</span>
                  <button type="button" className="text-xs font-bold text-blue-600">
                    Forgot Password?
                  </button>
                </span>
                <span className="mt-2 flex h-14 items-center gap-4 rounded-2xl border border-slate-200 bg-slate-50 px-4 text-slate-500">
                  <Lock className="h-5 w-5" />
                  <input
                    className="h-full flex-1 bg-transparent text-slate-950 outline-none"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    placeholder="Enter your password"
                    type="password"
                    required
                  />
                </span>
              </label>

              {loginError && (
                <div className="mt-5 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">
                  {loginError}
                </div>
              )}

              <button
                type="submit"
                disabled={isLoggingIn}
                className="mt-7 flex h-14 w-full items-center justify-center gap-3 rounded-2xl bg-blue-600 font-bold text-white shadow-lg shadow-blue-600/20 transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-400"
              >
                {isLoggingIn ? 'Signing In...' : 'Sign In'}
                <ArrowRight className="h-5 w-5" />
              </button>
            </form>

            <p className="mt-9 text-center text-sm text-slate-500">
              Don't have an account? <span className="font-bold text-blue-600">Contact HR</span>
            </p>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar activeTab={activeTab} setActiveTab={navigateTo} userRole={userRole} />
      <div className="flex min-w-0 flex-1 flex-col">
        <TopBar
          user={authUser}
          userRole={userRole}
          onNavigate={navigateTo}
          onLogout={handleLogout}
        />
        <main className="flex-1 overflow-auto p-8">
          {renderContent()}
        </main>
      </div>
    </div>
  );
}

export default App;
