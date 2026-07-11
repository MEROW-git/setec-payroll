const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:5000';

type ApiResponse<T> = {
  success: boolean;
  message: string;
  data: T;
  errors?: unknown;
};

export type AuthUser = {
  id: number;
  name: string;
  email: string;
  role: string | null;
};

export type LoginResult = {
  access_token: string;
  token_type: 'Bearer';
  user: AuthUser;
};

export type PaginationMeta = {
  page: number;
  per_page: number;
  total: number;
  pages: number;
};

export type EmployeeListItem = {
  id: number;
  employee_code: string;
  name: string;
  email: string | null;
  department: string | null;
  department_id: number;
  position: string | null;
  position_id: number;
  status: string;
  employment_type: string;
  profile_photo: string | null;
  hire_date: string | null;
};

export type EmployeeListResult = {
  items: EmployeeListItem[];
  meta: PaginationMeta;
};

export type Department = {
  id: number;
  name: string;
  code: string;
  description: string | null;
  is_active: boolean;
  annual_budget: number | null;
};

export type DepartmentMember = {
  id: number;
  name: string;
  email: string | null;
  position: string | null;
  status: string;
  profile_photo: string | null;
};

export type ManagedDepartment = Department & {
  manager: string | null;
  manager_id: number | null;
  employee_count: number;
  member_preview: DepartmentMember[];
};

export type DepartmentDetail = ManagedDepartment & {
  members: DepartmentMember[];
  performance: Array<{ month: string; score: number }>;
  annual_budget: number | null;
};

export type Position = {
  id: number;
  department_id: number;
  title: string;
  description: string | null;
  is_active: boolean;
  permissions: string[];
};

export type ManagedPosition = Position & {
  department: string | null;
  employee_count: number;
};

export type PositionManagementResult = {
  items: ManagedPosition[];
  stats: {
    total: number;
    assigned: number;
    unassigned: number;
  };
};

export type CreateEmployeePayload = {
  first_name: string;
  last_name: string;
  work_email: string;
  phone?: string;
  department_id: number | '';
  position_id: number | '';
  manager_id?: number | '';
  hire_date: string;
  basic_salary: number;
  address?: string;
  emergency_contact_name?: string;
  emergency_contact_phone?: string;
};

export type DashboardStats = {
  stats: {
    totalEmployees: number;
    presentToday: number;
    onLeave: number;
    pendingRequests: number;
  };
  attendanceTrend: Array<{ name: string; present: number; absent: number; onLeave: number }>;
  departmentDistribution: Array<{ name: string; value: number; color: string }>;
  recentEmployees: EmployeeListItem[];
  leaveRequests: Array<{
    id: number;
    employeeName: string;
    type: string;
    startDate: string | null;
    endDate: string | null;
    status: string;
  }>;
  recentActivity: Array<{
    id: number;
    user: string;
    action: string;
    time: string | null;
    type: string;
  }>;
};

export type NotificationItem = {
  id: string;
  title: string;
  message: string;
  time: string | null;
  unread: boolean;
  type: string;
};

export type NotificationResult = {
  items: NotificationItem[];
  unread_count: number;
};

export type AttendanceRecord = {
  id: number;
  employee_id: number;
  employee_code: string;
  employee_name: string;
  date: string;
  check_in: string | null;
  check_out: string | null;
  work_minutes: number;
  overtime_minutes: number;
  location: string | null;
  status: string;
  note: string | null;
};

export type AttendanceRecordsResult = {
  items: AttendanceRecord[];
  stats: Record<'present' | 'late' | 'absent' | 'remote' | 'on_leave', number>;
};

export type AttendanceMatrixEmployee = {
  id: number;
  employee_code: string;
  name: string;
  records: Record<string, string>;
};

export type RawPunch = {
  id: string;
  employee_id: number;
  employee_name: string;
  timestamp: string;
  device: string | null;
  method: string;
  status: string;
};

export type AttendancePolicy = {
  id: number;
  name: string;
  count_type: string;
  considerable_value: number;
  adjusted_days: number;
  description: string | null;
  is_active: boolean;
};

export type ShiftItem = { id: number; name: string; start_time: string; end_time: string; shift_type: string; status: string; notes: string | null; employee_count: number };
export type ShiftManagement = { items: ShiftItem[]; stats: { active: number; inactive: number; employees: number } };
export type ShiftRequestItem = { id: number; request_type: 'swap' | 'change'; request_date: string; requester_id: number; requester_name: string; current_shift_id: number; current_shift: string; target_employee_id: number | null; target_employee_name: string | null; new_shift_id: number | null; new_shift: string | null; remarks: string | null; status: string; created_at: string };
export type ShiftRequestsResult = { items: ShiftRequestItem[]; pending_count: number };

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem('access_token');
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
    ...options,
  });

  const payload = (await response.json()) as ApiResponse<T>;

  if (!response.ok || !payload.success) {
    throw new Error(payload.message || 'Request failed');
  }

  return payload.data;
}

export function login(email: string, password: string) {
  return request<LoginResult>('/api/v1/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
}

export function getCurrentUser() {
  return request<AuthUser>('/api/v1/auth/me');
}

export function logout() {
  return request<null>('/api/v1/auth/logout', {
    method: 'POST',
  });
}

export function getEmployees(params: { search?: string; page?: number; per_page?: number } = {}) {
  const searchParams = new URLSearchParams();
  if (params.search) searchParams.set('search', params.search);
  if (params.page) searchParams.set('page', String(params.page));
  if (params.per_page) searchParams.set('per_page', String(params.per_page));

  const query = searchParams.toString();
  return request<EmployeeListResult>(`/api/v1/employees/${query ? `?${query}` : ''}`);
}

export function createEmployee(payload: CreateEmployeePayload) {
  return request<EmployeeListItem>('/api/v1/employees/', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function getDepartments() {
  return request<Department[]>('/api/v1/departments/');
}

export function getManagedDepartments(search = '') {
  const query = search ? `?search=${encodeURIComponent(search)}` : '';
  return request<ManagedDepartment[]>(`/api/v1/departments/management${query}`);
}

export function getDepartmentDetail(departmentId: number) {
  return request<DepartmentDetail>(`/api/v1/departments/${departmentId}`);
}

export function createDepartment(payload: { name: string; code: string; description?: string; manager_employee_id?: number; annual_budget?: number }) {
  return request<ManagedDepartment>('/api/v1/departments/', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function getPositions(departmentId?: number | '') {
  const query = departmentId ? `?department_id=${departmentId}` : '';
  return request<Position[]>(`/api/v1/positions/${query}`);
}

export function getManagedPositions(search = '') {
  const query = search ? `?search=${encodeURIComponent(search)}` : '';
  return request<PositionManagementResult>(`/api/v1/positions/management${query}`);
}

export function createPosition(payload: { title: string; description?: string; department_id: number; permissions?: string[] }) {
  return request<ManagedPosition>('/api/v1/positions/', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function assignPosition(positionId: number, employeeId: number) {
  return request<{
    employee_id: number;
    position_id: number;
    position: string;
    department_id: number;
    department: string | null;
  }>(`/api/v1/positions/${positionId}/assign`, {
    method: 'POST',
    body: JSON.stringify({ employee_id: employeeId }),
  });
}

export function getDashboardStats() {
  return request<DashboardStats>('/api/v1/dashboard/stats');
}

export function getNotifications() {
  return request<NotificationResult>('/api/v1/dashboard/notifications');
}

export function getAttendanceRecords(params: { start_date: string; end_date: string; search?: string }) {
  const query = new URLSearchParams(params).toString();
  return request<AttendanceRecordsResult>(`/api/v1/attendance/records?${query}`);
}

export function getAttendanceMatrix(month: string, search = '') {
  const query = new URLSearchParams({ month, ...(search ? { search } : {}) }).toString();
  return request<{ employees: AttendanceMatrixEmployee[] }>(`/api/v1/attendance/matrix?${query}`);
}

export function getRawPunches(params: { start_date: string; end_date: string; search?: string }) {
  const query = new URLSearchParams(params).toString();
  return request<RawPunch[]>(`/api/v1/attendance/raw-punches?${query}`);
}

export function getAttendanceDevices() {
  return request<unknown[]>('/api/v1/attendance/devices');
}

export function markAttendance(payload: { employee_id: number; date: string; status: string; check_in?: string; check_out?: string; location?: string; note?: string }) {
  return request<AttendanceRecord>('/api/v1/attendance/records', { method: 'POST', body: JSON.stringify(payload) });
}

export function getAttendancePolicies() {
  return request<AttendancePolicy[]>('/api/v1/attendance/policies');
}

export function createAttendancePolicy(payload: { name: string; count_type: string; considerable_value: number; adjusted_days: number; description?: string }) {
  return request<AttendancePolicy>('/api/v1/attendance/policies', { method: 'POST', body: JSON.stringify(payload) });
}

export function getShifts(search = '') { const query = search ? `?search=${encodeURIComponent(search)}` : ''; return request<ShiftManagement>(`/api/v1/shifts/${query}`); }
export function createShift(payload: { name: string; start_time: string; end_time: string; shift_type: string; status: string; notes?: string }) { return request<ShiftItem>('/api/v1/shifts/', { method: 'POST', body: JSON.stringify(payload) }); }
export function getShiftRequests(search = '') { const query = search ? `?search=${encodeURIComponent(search)}` : ''; return request<ShiftRequestsResult>(`/api/v1/shifts/requests${query}`); }
export function createShiftRequest(payload: { request_type: string; request_date: string; requester_id: number; current_shift_id: number; target_employee_id?: number; new_shift_id?: number; remarks?: string }) { return request<ShiftRequestItem>('/api/v1/shifts/requests', { method: 'POST', body: JSON.stringify(payload) }); }
export function reviewShiftRequest(requestId: number, status: 'approved' | 'rejected') { return request<ShiftRequestItem>(`/api/v1/shifts/requests/${requestId}`, { method: 'PATCH', body: JSON.stringify({ status }) }); }
