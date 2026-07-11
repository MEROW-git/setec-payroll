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
