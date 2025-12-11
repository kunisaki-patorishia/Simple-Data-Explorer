from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import models, schemas, crud
from database import SessionLocal, engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Data Table API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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

@app.get("/departments/")
def get_departments(db: Session = Depends(get_db)):
    """
    Get unique departments for filter dropdown
    """
    return crud.get_departments(db)

@app.get("/roles/")
def get_roles(db: Session = Depends(get_db)):
    """
    Get unique roles for filter dropdown
    """
    return crud.get_roles(db)

@app.post("/seed/")
def seed_database(db: Session = Depends(get_db), count: int = 100):
    """
    Seed database with fake data
    """
    return crud.seed_database(db, count)

@app.get("/health/")
def health_check():
    return {"status": "healthy"}