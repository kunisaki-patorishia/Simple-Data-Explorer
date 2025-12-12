# Simple Data Explorer

A full-stack application featuring a data table with filtering, sorting, and pagination capabilities. Built with FastAPI (backend) and Next.js (frontend).

## Features

### Backend (FastAPI)
- ✅ RESTful API endpoints for user data retrieval
- ✅ Filtering by search term, department, and role
- ✅ Sorting by any column in ascending/descending order
- ✅ Pagination with configurable page size (1-100 records per page)
- ✅ SQLite database (local) or PostgreSQL (production) with seeding capability
- ✅ CORS configured for frontend communication
- ✅ Comprehensive error handling for invalid requests
- ✅ Simple in-memory caching (30-second TTL) for improved performance

### Frontend (Next.js with TypeScript)
- ✅ Responsive data table with Tailwind CSS
- ✅ Real-time search across name, email, department, and role
- ✅ Column sorting with visual indicators (chevron icons)
- ✅ Filter dropdowns for department and role
- ✅ Pagination controls with page number display
- ✅ Configurable page size (10, 25, 50, 100)
- ✅ Loading states with spinner animations
- ✅ Error states with retry functionality
- ✅ Clean, modern UI with hover effects

### Bonus Features
- ✅ Docker Compose setup for running both services together
- ✅ Simple caching mechanism to speed up repeated queries
- ✅ Railway deployment ready with PostgreSQL support

## Prerequisites

- **Docker and Docker Compose** (recommended for easy setup)
- **OR** Node.js 18+ and Python 3.11+ (for manual setup)
- **OR** Railway account (for cloud deployment - see [RAILWAY_DEPLOYMENT.md](./RAILWAY_DEPLOYMENT.md))

## Deployment Options

### 🚀 Deploy to Railway (Cloud - Recommended for Production)

Deploy both backend and frontend to Railway for free:
- See [RAILWAY_DEPLOYMENT.md](./RAILWAY_DEPLOYMENT.md) for complete guide
- Automatic HTTPS, PostgreSQL database, and custom domains
- Free tier includes $5 credit/month

### 🐳 Quick Start with Docker (Local)

1. Clone the repository:
```bash
git clone <repository-url>
cd "Simple Data Explorer"
```

2. Start both services with Docker Compose:
```bash
docker-compose up --build
```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. Seed the database:
   - Click the "Seed Database" button in the frontend, or
   - Visit http://localhost:8000/seed/ in your browser, or
   - Use the API: `POST http://localhost:8000/seed/?count=100`

## Manual Setup (Without Docker)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the FastAPI server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. Seed the database (in a new terminal):
```bash
curl -X POST "http://localhost:8000/seed/?count=100"
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open http://localhost:3000 in your browser

## Project Structure

```
Simple Data Explorer/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application and routes
│   │   ├── models.py         # SQLAlchemy database models
│   │   ├── schemas.py        # Pydantic schemas for validation
│   │   ├── crud.py           # Database operations
│   │   ├── database.py       # Database configuration
│   │   └── data.db           # SQLite database (created automatically)
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── page.tsx          # Main page component
│   │   ├── components/
│   │   │   └── DataTable.tsx # Data table component
│   │   ├── lib/
│   │   │   └── api.ts        # API client functions
│   │   ├── layout.tsx
│   │   └── globals.css
│   ├── Dockerfile
│   ├── package.json
│   └── next.config.js
└── README.md
```

## API Endpoints

### GET `/users/`
Retrieve users with filtering, sorting, and pagination.

**Query Parameters:**
- `skip` (int, default: 0): Number of records to skip
- `limit` (int, default: 10, max: 100): Number of records per page
- `search` (string, optional): Search term for name, email, department, or role
- `sort_by` (string, default: "id"): Column to sort by (id, name, email, role, department, date_joined)
- `sort_order` (string, default: "asc"): Sort order (asc, desc)
- `department` (string, optional): Filter by department
- `role` (string, optional): Filter by role

**Example:**
```
GET /users/?skip=0&limit=10&search=john&sort_by=name&sort_order=asc&department=Engineering
```

### GET `/departments/`
Get list of unique departments for filter dropdown.

### GET `/roles/`
Get list of unique roles for filter dropdown.

### POST `/seed/`
Seed the database with fake data.

**Query Parameters:**
- `count` (int, default: 100, max: 1000): Number of records to generate

**Example:**
```
POST /seed/?count=100
```

### GET `/health/`
Health check endpoint.

### DELETE `/cache/`
Clear the in-memory cache (useful for testing).

## Approach & Design Decisions

### Backend Architecture
- **FastAPI**: Chosen for its modern async support, automatic API documentation, and type safety
- **SQLAlchemy ORM**: Provides database abstraction and easy query building
- **SQLite**: Simple file-based database, perfect for this assessment (easily upgradeable to PostgreSQL)
- **Pydantic Schemas**: Automatic request/response validation and serialization
- **In-Memory Caching**: Simple dictionary-based cache with TTL to improve performance for repeated queries

### Frontend Architecture
- **Next.js 16**: React framework with App Router for modern development experience
- **TypeScript**: Type safety and better developer experience
- **Tailwind CSS**: Utility-first CSS for rapid UI development
- **Axios**: HTTP client for API communication
- **Client-Side State Management**: React hooks (useState, useEffect) for simple state management

### Key Features Implementation
1. **Filtering**: Server-side filtering to reduce data transfer and improve performance
2. **Sorting**: Clickable column headers with visual indicators (chevron icons)
3. **Pagination**: Server-side pagination with configurable page sizes
4. **Search**: Real-time search with debouncing via useEffect dependencies
5. **Error Handling**: Try-catch blocks with user-friendly error messages
6. **Loading States**: Spinner animations during data fetching

## What I Would Add/Improve (Given More Time)

### Performance & Scalability
- **Database Indexing**: Add indexes on frequently queried columns (name, email, department, role)
- **Redis Caching**: Replace in-memory cache with Redis for distributed caching
- **Database Connection Pooling**: Optimize database connections for high concurrency
- **Query Optimization**: Add database query analysis and optimization
- **Pagination Improvements**: Add cursor-based pagination for better performance with large datasets

### Features
- **Export Functionality**: Allow users to export filtered data as CSV/Excel
- **Advanced Filters**: Date range filtering, multiple value selection
- **Column Visibility Toggle**: Let users show/hide columns
- **Saved Filters**: Save and reuse filter combinations
- **Bulk Operations**: Select and perform actions on multiple records
- **User Authentication**: Add login/logout and user-specific data views

### Code Quality
- **Unit Tests**: Comprehensive test coverage for backend and frontend
- **Integration Tests**: End-to-end API testing
- **Type Safety**: More strict TypeScript configuration
- **Error Logging**: Implement proper logging (e.g., using Python's logging module)
- **API Rate Limiting**: Prevent abuse with rate limiting middleware

### UI/UX
- **Responsive Design**: Further optimize for mobile devices
- **Accessibility**: Add ARIA labels, keyboard navigation, screen reader support
- **Dark Mode**: Add theme toggle
- **Animations**: Smooth transitions and loading states
- **Toast Notifications**: Replace alerts with toast notifications for better UX

### DevOps
- **CI/CD Pipeline**: Automated testing and deployment
- **Environment Variables**: Better configuration management
- **Database Migrations**: Use Alembic for database version control
- **Monitoring**: Add application monitoring and error tracking (e.g., Sentry)
- **Production Database**: Use PostgreSQL or MySQL for production

## Technologies Used

### Backend
- FastAPI 0.104+
- SQLAlchemy 2.0+
- Pydantic 2.5+
- Faker (for generating test data)
- Uvicorn (ASGI server)

### Frontend
- Next.js 16
- React 19
- TypeScript 5
- Tailwind CSS 3.3
- Axios 1.6
- Lucide React (icons)

## License

This project is created for assessment purposes.
