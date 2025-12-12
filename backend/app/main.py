from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from typing import Optional
import os
import models, schemas, crud
from database import SessionLocal, engine, Base
from datetime import datetime, timedelta

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Data Table API", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    """Seed database on startup if empty"""
    db = SessionLocal()
    try:
        count = db.query(func.count(models.User.id)).scalar()
        if count == 0:
            print("Database is empty. Seeding with 100 records...")
            crud.seed_database(db, 100)
            print("Database seeded successfully!")
        else:
            print(f"Database already contains {count} records.")
    except Exception as e:
        print(f"Error during startup: {e}")
    finally:
        db.close()

# Simple in-memory cache
cache = {}
CACHE_TTL = timedelta(seconds=30)  # Cache for 30 seconds

def get_cache_key(skip, limit, search, sort_by, sort_order, department, role):
    """Generate a cache key from query parameters"""
    return f"users:{skip}:{limit}:{search or ''}:{sort_by}:{sort_order}:{department or ''}:{role or ''}"

def get_cached_or_compute(cache_key, compute_func):
    """Get from cache or compute and cache the result"""
    if cache_key in cache:
        cached_data, cached_time = cache[cache_key]
        if datetime.now() - cached_time < CACHE_TTL:
            return cached_data
    
    # Compute and cache
    result = compute_func()
    cache[cache_key] = (result, datetime.now())
    return result

# CORS configuration - supports both localhost and production URLs
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
if os.getenv("FRONTEND_URL"):
    allowed_origins.append(os.getenv("FRONTEND_URL"))

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Data Table API"}

@app.get("/users/", response_model=schemas.UserListResponse)
def get_users(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    sort_by: Optional[str] = Query("id", regex="^(id|name|email|role|department|date_joined)$"),
    sort_order: Optional[str] = Query("asc", regex="^(asc|desc)$"),
    department: Optional[str] = None,
    role: Optional[str] = None
):
    """
    Get users with pagination, filtering, and sorting
    """
    try:
        cache_key = get_cache_key(skip, limit, search, sort_by, sort_order, department, role)
        
        def compute_users():
            return crud.get_users(
                db=db,
                skip=skip,
                limit=limit,
                search=search,
                sort_by=sort_by,
                sort_order=sort_order,
                department=department,
                role=role
            )
        
        return get_cached_or_compute(cache_key, compute_users)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/departments/")
def get_departments(db: Session = Depends(get_db)):
    """
    Get unique departments for filter dropdown
    """
    try:
        cache_key = "departments"
        def compute_departments():
            return crud.get_departments(db)
        return get_cached_or_compute(cache_key, compute_departments)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/roles/")
def get_roles(db: Session = Depends(get_db)):
    """
    Get unique roles for filter dropdown
    """
    try:
        cache_key = "roles"
        def compute_roles():
            return crud.get_roles(db)
        return get_cached_or_compute(cache_key, compute_roles)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/seed/")
def seed_database(db: Session = Depends(get_db), count: int = Query(100, ge=1, le=1000)):
    """
    Seed database with fake data
    """
    try:
        # Clear cache when seeding
        cache.clear()
        result = crud.seed_database(db, count)
        return result
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health/")
def health_check():
    return {"status": "healthy"}

@app.delete("/cache/")
def clear_cache():
    """
    Clear the cache (useful for testing or manual cache invalidation)
    """
    cache.clear()
    return {"message": "Cache cleared"}