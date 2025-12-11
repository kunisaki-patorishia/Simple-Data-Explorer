'use client';

import { useState, useEffect, useMemo } from 'react';
import DataTable from './components/DataTable';
import Filters from './components/Filters';
import Pagination from './components/Pagination';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';
import { User, ApiResponse } from './types';
import { fetchUsers, fetchDepartments, fetchRoles } from './lib/api';

export default function Home() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalItems, setTotalItems] = useState(0);
  const [pageSize, setPageSize] = useState(10);
  
  const [filters, setFilters] = useState({
    search: '',
    department: '',
    role: '',
    sortBy: 'id',
    sortOrder: 'asc' as 'asc' | 'desc'
  });

  const [departments, setDepartments] = useState<string[]>([]);
  const [roles, setRoles] = useState<string[]>([]);

  useEffect(() => {
    loadFilterOptions();
  }, []);

  useEffect(() => {
    loadUsers();
  }, [currentPage, pageSize, filters]);

  const loadFilterOptions = async () => {
    try {
      const [depts, rolesData] = await Promise.all([
        fetchDepartments(),
        fetchRoles()
      ]);
      setDepartments(depts);
      setRoles(rolesData);
    } catch (err) {
      console.error('Failed to load filter options:', err);
    }
  };

  const loadUsers = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetchUsers({
        page: currentPage,
        limit: pageSize,
        ...filters
      });
      
      setUsers(response.users);
      setTotalPages(response.total_pages);
      setTotalItems(response.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load users');
    } finally {
      setLoading(false);
    }
  };

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  const handleFilterChange = (newFilters: Partial<typeof filters>) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
    setCurrentPage(1); // Reset to first page when filters change
  };

  const handlePageSizeChange = (size: number) => {
    setPageSize(size);
    setCurrentPage(1);
  };

  if (loading && users.length === 0) {
    return <LoadingSpinner />;
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">User Management</h1>
          <p className="text-gray-600 mt-2">
            Manage and explore user records with filtering, sorting, and pagination
          </p>
        </header>

        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <Filters
            filters={filters}
            departments={departments}
            roles={roles}
            onFilterChange={handleFilterChange}
            onRefresh={loadUsers}
          />
        </div>

        {error ? (
          <ErrorMessage message={error} onRetry={loadUsers} />
        ) : (
          <>
            <div className="bg-white rounded-lg shadow-md overflow-hidden mb-6">
              <DataTable
                users={users}
                sortBy={filters.sortBy}
                sortOrder={filters.sortOrder}
                onSortChange={(sortBy, sortOrder) => 
                  handleFilterChange({ sortBy, sortOrder })
                }
                loading={loading}
              />
            </div>

            <div className="bg-white rounded-lg shadow-md p-4">
              <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                totalItems={totalItems}
                pageSize={pageSize}
                onPageChange={handlePageChange}
                onPageSizeChange={handlePageSizeChange}
              />
            </div>
          </>
        )}
      </div>
    </div>
  );
}