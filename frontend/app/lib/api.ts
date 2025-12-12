import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface FetchUsersParams {
  page: number;
  limit: number;
  search?: string;
  department?: string;
  role?: string;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

export interface ApiResponse {
  users: User[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

export interface User {
  id: number;
  name: string;
  email: string;
  role: string;
  department: string;
  date_joined: string;
}

export const fetchUsers = async (params: FetchUsersParams): Promise<ApiResponse> => {
  const skip = (params.page - 1) * params.limit;
  
  const response = await api.get('/users/', {
    params: {
      skip,
      limit: params.limit,
      search: params.search,
      department: params.department,
      role: params.role,
      sort_by: params.sortBy,
      sort_order: params.sortOrder,
    },
  });
  
  return response.data;
};

export const fetchDepartments = async (): Promise<string[]> => {
  const response = await api.get('/departments/');
  return response.data.map((item: { department: string }) => item.department);
};

export const fetchRoles = async (): Promise<string[]> => {
  const response = await api.get('/roles/');
  return response.data.map((item: { role: string }) => item.role);
};

export const seedDatabase = async (count: number = 100): Promise<void> => {
  await api.post(`/seed/?count=${count}`);
};