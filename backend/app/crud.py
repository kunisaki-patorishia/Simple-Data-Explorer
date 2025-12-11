from sqlalchemy.orm import Session
from sqlalchemy import or_, func, desc
import models, schemas
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()

def get_users(db: Session, skip: int = 0, limit: int = 10, 
              search: str = None, sort_by: str = "id", 
              sort_order: str = "asc", department: str = None, 
              role: str = None):
    
    query = db.query(models.User)
    
    # Search filter
    if search:
        search = f"%{search}%"
        query = query.filter(
            or_(
                models.User.name.ilike(search),
                models.User.email.ilike(search),
                models.User.department.ilike(search),
                models.User.role.ilike(search)
            )
        )
    
    # Department filter
    if department:
        query = query.filter(models.User.department == department)
    
    # Role filter
    if role:
        query = query.filter(models.User.role == role)
    
    # Sorting
    if hasattr(models.User, sort_by):
        column = getattr(models.User, sort_by)
        if sort_order == "desc":
            query = query.order_by(desc(column))
        else:
            query = query.order_by(column)
    
    # Get total count
    total = query.count()
    
    # Pagination
    users = query.offset(skip).limit(limit).all()
    
    # Calculate total pages
    total_pages = (total + limit - 1) // limit
    
    return {
        "users": users,
        "total": total,
        "page": skip // limit + 1,
        "limit": limit,
        "total_pages": total_pages
    }

def get_departments(db: Session):
    return db.query(models.User.department).distinct().all()

def get_roles(db: Session):
    return db.query(models.User.role).distinct().all()

def seed_database(db: Session, count: int = 100):
    # Clear existing data
    db.query(models.User).delete()
    
    departments = ["Engineering", "Marketing", "Sales", "HR", "Finance", "IT", "Operations"]
    roles = ["Intern", "Junior", "Mid-level", "Senior", "Lead", "Manager", "Director"]
    
    users = []
    for i in range(count):
        user = models.User(
            name=fake.name(),
            email=fake.unique.email(),
            role=random.choice(roles),
            department=random.choice(departments),
            date_joined=fake.date_between(start_date='-5y', end_date='today')
        )
        users.append(user)
    
    db.add_all(users)
    db.commit()
    
    return {"message": f"Seeded {count} users"}