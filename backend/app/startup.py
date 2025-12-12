"""
Startup script to seed the database if it's empty
"""
from database import SessionLocal
from sqlalchemy import func
import models
import crud

def init_db():
    """Initialize database with seed data if empty"""
    db = SessionLocal()
    try:
        # Check if database is empty
        count = db.query(func.count(models.User.id)).scalar()
        if count == 0:
            print("Database is empty. Seeding with 100 records...")
            crud.seed_database(db, 100)
            print("Database seeded successfully!")
        else:
            print(f"Database already contains {count} records.")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()

