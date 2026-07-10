export const MOCK_EMPLOYEES = [
  {
    id: 1,
    name: 'John Doe',
    email: 'john.doe@company.com',
    department: 'Engineering',
    role: 'Software Engineer',
    status: 'Active',
    joinDate: '2023-01-15'
  },
  {
    id: 2,
    name: 'Jane Smith',
    email: 'jane.smith@company.com',
    department: 'Marketing',
    role: 'Marketing Manager',
    status: 'Active',
    joinDate: '2022-11-20'
  },
  {
    id: 3,
    name: 'Bob Johnson',
    email: 'bob.johnson@company.com',
    department: 'Sales',
    role: 'Sales Representative',
    status: 'Active',
    joinDate: '2023-03-10'
  },
  {
    id: 4,
    name: 'Alice Brown',
    email: 'alice.brown@company.com',
    department: 'HR',
    role: 'HR Specialist',
    status: 'Active',
    joinDate: '2022-08-05'
  },
  {
    id: 5,
    name: 'Charlie Wilson',
    email: 'charlie.wilson@company.com',
    department: 'Design',
    role: 'UI Designer',
    status: 'Active',
    joinDate: '2023-05-22'
  },
  {
    id: 6,
    name: 'Diana Lee',
    email: 'diana.lee@company.com',
    department: 'Engineering',
    role: 'DevOps Engineer',
    status: 'Active',
    joinDate: '2023-02-14'
  }
];

export const MOCK_DEPARTMENTS = [
  { id: 1, name: 'Engineering', head: 'John Doe' },
  { id: 2, name: 'Marketing', head: 'Jane Smith' },
  { id: 3, name: 'Sales', head: 'Bob Johnson' },
  { id: 4, name: 'HR', head: 'Alice Brown' },
  { id: 5, name: 'Design', head: 'Charlie Wilson' }
];

export const MOCK_LEAVE_REQUESTS = [
  {
    id: 1,
    employeeName: 'John Doe',
    type: 'Annual',
    startDate: '2023-12-25',
    endDate: '2023-12-27',
    status: 'Pending'
  },
  {
    id: 2,
    employeeName: 'Jane Smith',
    type: 'Sick',
    startDate: '2023-12-20',
    endDate: '2023-12-21',
    status: 'Approved'
  },
  {
    id: 3,
    employeeName: 'Bob Johnson',
    type: 'Personal',
    startDate: '2023-12-28',
    endDate: '2023-12-30',
    status: 'Pending'
  },
  {
    id: 4,
    employeeName: 'Alice Brown',
    type: 'Maternity',
    startDate: '2024-01-01',
    endDate: '2024-03-01',
    status: 'Approved'
  }
];