# Testing Guide for Simple Data Explorer

This guide will help you test all features of the application.

## Quick Start Testing

### Option 1: Using Docker (Recommended)

1. **Start the services:**
```bash
docker-compose up --build
```

2. **Wait for services to be ready:**
   - Backend: Look for "Application startup complete" in logs
   - Frontend: Look for "Ready" message on http://localhost:3000

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health/

### Option 2: Manual Setup

**Terminal 1 - Backend:**
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Testing Checklist

### 1. Initial Setup & Database Seeding

✅ **Test: Database Auto-Seeding**
- Start the backend
- Check console logs for: "Database is empty. Seeding with 100 records..."
- Verify in frontend that data appears automatically

✅ **Test: Manual Seeding**
- Click "Seed Database" button in frontend
- Verify success message or check that data refreshes
- Or use API: `POST http://localhost:8000/seed/?count=100`

### 2. Frontend UI Testing

✅ **Test: Data Table Display**
- [ ] Table loads with user data
- [ ] All columns visible: ID, Name, Email, Role, Department, Date Joined
- [ ] Table is responsive (try resizing browser)
- [ ] Hover effects work on table rows

✅ **Test: Search Functionality**
- [ ] Type in search box (e.g., "john")
- [ ] Results filter in real-time
- [ ] Search works across name, email, department, role
- [ ] Clear search shows all results again
- [ ] Search with no results shows "No users found" message

✅ **Test: Filter Dropdowns**
- [ ] Department dropdown shows all unique departments
- [ ] Role dropdown shows all unique roles
- [ ] Select a department - table filters correctly
- [ ] Select a role - table filters correctly
- [ ] Combine department + role filters
- [ ] "Clear Filters" button resets all filters

✅ **Test: Sorting**
- [ ] Click on column headers (ID, Name, Email, etc.)
- [ ] First click sorts ascending (↑ chevron)
- [ ] Second click sorts descending (↓ chevron)
- [ ] Verify data is actually sorted correctly
- [ ] Sorting works with filters applied

✅ **Test: Pagination**
- [ ] Change page size (10, 25, 50, 100)
- [ ] Verify correct number of records per page
- [ ] Click "Next" button - moves to next page
- [ ] Click "Previous" button - moves to previous page
- [ ] Click page numbers - jumps to that page
- [ ] Verify "Showing X to Y of Z results" counter is correct
- [ ] Test pagination with filters applied

✅ **Test: Loading States**
- [ ] Spinner appears when data is loading
- [ ] Table shows loading indicator in table body
- [ ] Loading state appears when changing filters/sorting

✅ **Test: Error Handling**
- [ ] Stop backend server
- [ ] Try to refresh data in frontend
- [ ] Verify error message appears
- [ ] "Try again" button is clickable
- [ ] Restart backend and verify recovery works

### 3. Backend API Testing

#### Using Browser/Postman

✅ **Test: Health Check**
```
GET http://localhost:8000/health/
Expected: {"status": "healthy"}
```

✅ **Test: Get Users (Basic)**
```
GET http://localhost:8000/users/
Expected: JSON with users array, total, page, limit, total_pages
```

✅ **Test: Get Users with Pagination**
```
GET http://localhost:8000/users/?skip=0&limit=10
GET http://localhost:8000/users/?skip=10&limit=10
Verify: Different pages return different data
```

✅ **Test: Get Users with Search**
```
GET http://localhost:8000/users/?search=john
Expected: Only users matching "john" in name, email, department, or role
```

✅ **Test: Get Users with Filters**
```
GET http://localhost:8000/users/?department=Engineering
GET http://localhost:8000/users/?role=Senior
GET http://localhost:8000/users/?department=Engineering&role=Senior
Verify: Filters work individually and combined
```

✅ **Test: Get Users with Sorting**
```
GET http://localhost:8000/users/?sort_by=name&sort_order=asc
GET http://localhost:8000/users/?sort_by=name&sort_order=desc
GET http://localhost:8000/users/?sort_by=date_joined&sort_order=desc
Verify: Data is sorted correctly
```

✅ **Test: Get Departments**
```
GET http://localhost:8000/departments/
Expected: Array of unique department names
```

✅ **Test: Get Roles**
```
GET http://localhost:8000/roles/
Expected: Array of unique role names
```

✅ **Test: Seed Database**
```
POST http://localhost:8000/seed/?count=50
Expected: {"message": "Seeded 50 users"}
Verify: Database now has 50 users
```

✅ **Test: Error Handling - Invalid Parameters**
```
GET http://localhost:8000/users/?limit=200
Expected: Error (limit max is 100)

GET http://localhost:8000/users/?sort_by=invalid_column
Expected: Error (invalid sort column)

GET http://localhost:8000/users/?skip=-1
Expected: Error (skip must be >= 0)
```

✅ **Test: Cache**
```
GET http://localhost:8000/users/?search=test
Note the response time

GET http://localhost:8000/users/?search=test
Note the response time (should be faster due to cache)

DELETE http://localhost:8000/cache/
GET http://localhost:8000/users/?search=test
Cache should be cleared
```

#### Using FastAPI Interactive Docs

1. **Open API Documentation:**
   - Navigate to: http://localhost:8000/docs
   - This provides an interactive Swagger UI

2. **Test each endpoint:**
   - Click on an endpoint (e.g., `GET /users/`)
   - Click "Try it out"
   - Fill in parameters
   - Click "Execute"
   - Review the response

3. **Test error cases:**
   - Try invalid parameters
   - Verify error responses are clear

### 4. Integration Testing Scenarios

✅ **Scenario 1: Complete User Flow**
1. Open frontend
2. Search for "engineer"
3. Filter by "Engineering" department
4. Sort by "Name" ascending
5. Change page size to 25
6. Navigate to page 2
7. Clear all filters
8. Verify all data returns

✅ **Scenario 2: Performance Testing**
1. Seed database with 1000 records: `POST /seed/?count=1000`
2. Test pagination with different page sizes
3. Test search performance
4. Test sorting performance
5. Verify caching improves response times

✅ **Scenario 3: Edge Cases**
1. Search with special characters: `!@#$%`
2. Search with empty string
3. Filter with non-existent department
4. Sort by date_joined (verify date sorting works)
5. Test with exactly 10, 25, 50, 100 records

✅ **Scenario 4: Concurrent Requests**
1. Open multiple browser tabs
2. Make different requests simultaneously
3. Verify all requests complete successfully
4. Check for any race conditions

### 5. Browser Console Testing

Open browser DevTools (F12) and check:

✅ **Network Tab:**
- [ ] API requests are made correctly
- [ ] Responses have correct status codes (200, 400, 500)
- [ ] Request/response times are reasonable
- [ ] No CORS errors

✅ **Console Tab:**
- [ ] No JavaScript errors
- [ ] No warnings
- [ ] API errors are logged appropriately

✅ **Application Tab:**
- [ ] Check localStorage/sessionStorage if used
- [ ] Verify no memory leaks

### 6. Manual Test Script

You can use this curl script to test all endpoints:

```bash
# Health check
curl http://localhost:8000/health/

# Get users
curl http://localhost:8000/users/

# Get users with filters
curl "http://localhost:8000/users/?search=john&department=Engineering&sort_by=name&sort_order=asc"

# Get departments
curl http://localhost:8000/departments/

# Get roles
curl http://localhost:8000/roles/

# Seed database
curl -X POST "http://localhost:8000/seed/?count=100"

# Clear cache
curl -X DELETE http://localhost:8000/cache/
```

### 7. Expected Results Summary

**Frontend:**
- ✅ Table displays all user data correctly
- ✅ Search filters results in real-time
- ✅ Filters work independently and together
- ✅ Sorting works on all columns
- ✅ Pagination navigates correctly
- ✅ Loading states show during API calls
- ✅ Error messages display when API fails
- ✅ UI is responsive and modern

**Backend:**
- ✅ All endpoints return correct data
- ✅ Pagination calculates correctly
- ✅ Filters work as expected
- ✅ Sorting works correctly
- ✅ Error handling returns appropriate status codes
- ✅ Caching improves performance
- ✅ Database seeding works

## Troubleshooting

**Issue: Frontend can't connect to backend**
- Check backend is running on port 8000
- Check CORS settings in `main.py`
- Verify `NEXT_PUBLIC_API_URL` environment variable

**Issue: No data showing**
- Check if database is seeded
- Check backend logs for errors
- Verify database file exists: `backend/app/data.db`

**Issue: Filters not working**
- Check browser console for errors
- Verify API endpoints return correct data
- Check network tab for API responses

**Issue: Docker containers not starting**
- Check Docker is running
- Verify ports 3000 and 8000 are not in use
- Check Docker logs: `docker-compose logs`

## Performance Benchmarks

Expected performance (approximate):
- Initial page load: < 2 seconds
- Search/filter response: < 500ms
- Pagination: < 300ms
- Cached requests: < 50ms

## Next Steps After Testing

If you find any issues:
1. Check the browser console for errors
2. Check backend logs for exceptions
3. Verify database has data
4. Test API endpoints directly using `/docs`
5. Review error messages for clues

Happy Testing! 🚀

