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
};

export type Position = {
  id: number;
  department_id: number;
  title: string;
  description: string | null;
  is_active: boolean;
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

export function getPositions(departmentId?: number | '') {
  const query = departmentId ? `?department_id=${departmentId}` : '';
  return request<Position[]>(`/api/v1/positions/${query}`);
}
