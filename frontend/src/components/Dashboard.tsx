import { 
  Users, 
  UserPlus, 
  Calendar, 
  ArrowUpRight,
  ArrowDownRight,
  ClipboardCheck,
  FileCheck,
  Clock,
  CheckCircle2
} from 'lucide-react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend
} from 'recharts';
import { MOCK_EMPLOYEES, MOCK_LEAVE_REQUESTS } from '../mockData';
import { cn } from '../lib/utils';

const attendanceData = [
  { name: 'Jan', present: 85, absent: 8, onLeave: 7 },
  { name: 'Feb', present: 88, absent: 7, onLeave: 5 },
  { name: 'Mar', present: 82, absent: 10, onLeave: 8 },
  { name: 'Apr', present: 90, absent: 5, onLeave: 5 },
  { name: 'May', present: 87, absent: 7, onLeave: 6 },
  { name: 'Jun', present: 92, absent: 4, onLeave: 4 },
];

const departmentData = [
  { name: 'Engineering', value: 35, color: '#0ea5e9' },
  { name: 'Marketing', value: 20, color: '#10b981' },
  { name: 'Sales', value: 25, color: '#f59e0b' },
  { name: 'HR', value: 10, color: '#8b5cf6' },
  { name: 'Design', value: 10, color: '#ec4899' },
];

const StatCard = ({ title, value, change, icon: Icon, trend, iconBg, iconColor }: any) => (
  <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
    <div className="flex justify-between items-start mb-4">
      <div>
        <p className="text-sm font-medium text-slate-500 mb-1">{title}</p>
        <h3 className="text-2xl font-bold text-slate-900">{value}</h3>
      </div>
      <div className={cn("p-3 rounded-xl", iconBg)}>
        <Icon className={cn("w-6 h-6", iconColor)} />
      </div>
    </div>
    <div className="flex items-center gap-1 mt-2">
      {trend === 'up' ? (
        <ArrowUpRight className="w-4 h-4 text-emerald-500" />
      ) : (
        <ArrowDownRight className="w-4 h-4 text-rose-500" />
      )}
      <span className={trend === 'up' ? "text-emerald-600 text-sm font-bold" : "text-rose-600 text-sm font-bold"}>
        {change}
      </span>
      <span className="text-slate-400 text-xs ml-1">
        {title === 'Total Employees' ? 'vs last month' : 
         title === 'Present Today' ? 'vs yesterday' :
         title === 'On Leave' ? 'vs last week' : 'new today'}
      </span>
    </div>
  </div>
);

interface DashboardProps {
  onNavigate: (tab: string) => void;
}

export default function Dashboard({ onNavigate }: DashboardProps) {
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-slate-900 tracking-tight">Dashboard Overview</h2>
        <p className="text-slate-500 mt-1">Welcome back! Here's what's happening today.</p>
      </div>

      {/* Row 1: Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard 
          title="Total Employees" 
          value="248" 
          change="12%" 
          icon={Users} 
          trend="up"
          iconBg="bg-blue-500"
          iconColor="text-white"
        />
        <StatCard 
          title="Present Today" 
          value="234" 
          change="5%" 
          icon={CheckCircle2} 
          trend="up"
          iconBg="bg-emerald-500"
          iconColor="text-white"
        />
        <StatCard 
          title="On Leave" 
          value="8" 
          change="2%" 
          icon={Calendar} 
          trend="down"
          iconBg="bg-orange-500"
          iconColor="text-white"
        />
        <StatCard 
          title="Pending Requests" 
          value="14" 
          change="3%" 
          icon={Clock} 
          trend="up"
          iconBg="bg-purple-500"
          iconColor="text-white"
        />
      </div>

      {/* Row 2: Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
          <h3 className="text-lg font-bold text-slate-900 mb-6">Attendance Trends</h3>
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={attendanceData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis 
                  dataKey="name" 
                  axisLine={false} 
                  tickLine={false} 
                  tick={{ fill: '#64748b', fontSize: 12 }} 
                  dy={10}
                />
                <YAxis 
                  axisLine={false} 
                  tickLine={false} 
                  tick={{ fill: '#64748b', fontSize: 12 }}
                />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#fff', borderRadius: '12px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                />
                <Legend verticalAlign="bottom" height={36}/>
                <Line type="monotone" dataKey="present" stroke="#10b981" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} name="Present" />
                <Line type="monotone" dataKey="absent" stroke="#ef4444" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} name="Absent" />
                <Line type="monotone" dataKey="onLeave" stroke="#f59e0b" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} name="On Leave" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
          <h3 className="text-lg font-bold text-slate-900 mb-6">Department Distribution</h3>
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={departmentData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {departmentData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Row 3: Quick Actions (Full Width) */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <h3 className="text-lg font-bold text-slate-900 mb-6">Quick Actions</h3>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {[
            { label: 'Add Employee', icon: UserPlus, color: 'bg-blue-500', onClick: () => onNavigate('add-employee') },
            { label: 'Mark Attendance', icon: ClipboardCheck, color: 'bg-emerald-500', onClick: () => onNavigate('attendance') },
            { label: 'Approve Leaves', icon: FileCheck, color: 'bg-purple-500', onClick: () => onNavigate('leave') },
            { label: 'Events & Schedule', icon: Calendar, color: 'bg-pink-500', onClick: () => onNavigate('events-schedule') },
            { label: 'View Calendar', icon: Calendar, color: 'bg-indigo-500', onClick: () => onNavigate('leave') },
          ].map((action) => (
            <button 
              key={action.label}
              onClick={action.onClick}
              className="flex flex-col items-center justify-center p-4 rounded-xl border border-slate-100 hover:bg-slate-50 transition-all group"
            >
              <div className={cn("p-3 rounded-xl mb-3 group-hover:scale-110 transition-transform", action.color)}>
                <action.icon className="w-6 h-6 text-white" />
              </div>
              <span className="text-xs font-bold text-slate-700 text-center">{action.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Row 3: Recent Activity and Leave Requests (Side by Side) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
          <h3 className="text-lg font-bold text-slate-900 mb-6">Recent Activity</h3>
          <div className="space-y-6">
            {[
              { user: 'Sarah Johnson', action: 'submitted a leave request for Dec 28-30', time: '2 hours ago', icon: FileCheck, color: 'text-orange-500' },
              { user: 'Alex Thompson', action: 'was added to Engineering department', time: '5 hours ago', icon: UserPlus, color: 'text-emerald-500' },
              { user: 'Michael Chen', action: 'marked attendance at 9:15 AM', time: '7 hours ago', icon: ClipboardCheck, color: 'text-blue-500' },
              { user: 'Emily Rodriguez', action: 'leave request was approved', time: '1 day ago', icon: FileCheck, color: 'text-orange-500' },
              { user: 'James Wilson', action: 'updated profile information', time: '2 days ago', icon: Clock, color: 'text-slate-400' },
            ].map((activity, i) => (
              <div key={i} className="flex gap-4">
                <div className={cn("mt-1", activity.color)}>
                  <activity.icon className="w-4 h-4" />
                </div>
                <div>
                  <p className="text-sm text-slate-600">
                    <span className="font-bold text-slate-900">{activity.user}</span> {activity.action}
                  </p>
                  <p className="text-xs text-slate-400 mt-1">{activity.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-lg font-bold text-slate-900">Leave Requests</h3>
            <button onClick={() => onNavigate('leave')} className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-bold hover:bg-blue-700 transition-colors">
              View all
            </button>
          </div>
          <div className="space-y-4">
            {MOCK_LEAVE_REQUESTS.slice(0, 3).map((request) => (
              <div key={request.id} className="p-4 rounded-xl border border-slate-100 space-y-4">
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="font-bold text-slate-900">{request.employeeName}</h4>
                    <p className="text-sm text-slate-500">{request.type} Leave</p>
                    <p className="text-xs text-slate-400 mt-1">{request.startDate} - {request.endDate}</p>
                  </div>
                  <span className={cn(
                    "px-2.5 py-1 rounded-lg text-[10px] font-bold uppercase tracking-wider",
                    request.status === 'Approved' ? "bg-emerald-100 text-emerald-700" : "bg-amber-100 text-amber-700"
                  )}>
                    {request.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Row 4: Recent Employees (Full Width) */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-6 border-b border-slate-100">
          <h3 className="text-lg font-bold text-slate-900">Recent Employees</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-slate-50 text-slate-500 text-xs uppercase tracking-wider">
              <tr>
                <th className="px-6 py-4 font-semibold">Name</th>
                <th className="px-6 py-4 font-semibold">Email</th>
                <th className="px-6 py-4 font-semibold">Department</th>
                <th className="px-6 py-4 font-semibold">Position</th>
                <th className="px-6 py-4 font-semibold text-center">Status</th>
                <th className="px-6 py-4 font-semibold">Join Date</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {MOCK_EMPLOYEES.slice(0, 5).map((emp) => (
                <tr key={emp.id} className="hover:bg-slate-50 transition-colors cursor-pointer">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center text-white text-[10px] font-bold">
                        {emp.name.split(' ').map(n => n[0]).join('')}
                      </div>
                      <span className="font-bold text-slate-900 text-sm">{emp.name}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-slate-500 text-sm">{emp.email}</td>
                  <td className="px-6 py-4 text-slate-600 font-medium text-sm">{emp.department}</td>
                  <td className="px-6 py-4 text-slate-600 text-sm">{emp.role}</td>
                  <td className="px-6 py-4 text-center">
                    <span className={cn(
                      "px-2.5 py-1 rounded-lg text-[10px] font-bold",
                      emp.status === 'Active' ? "bg-emerald-100 text-emerald-700" : "bg-orange-100 text-orange-700"
                    )}>
                      {emp.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-slate-500 text-sm">{emp.joinDate}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}