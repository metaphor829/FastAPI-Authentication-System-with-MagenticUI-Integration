"""
Database configuration and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlmodel import SQLModel
from typing import Generator

from app.config import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
    echo=settings.debug
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()


def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session.
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database with default data."""
    from app.models.user import User
    from app.models.role import Role
    from app.core.security import get_password_hash
    
    # Create tables
    create_db_and_tables()
    
    # Create default roles
    db = SessionLocal()
    try:
        # Check if roles already exist
        if not db.query(Role).first():
            import json
            default_roles = [
                Role(
                    name="admin",
                    description="Administrator with full access",
                    permissions=json.dumps(["*"])  # All permissions
                ),
                Role(
                    name="user",
                    description="Regular user with limited access",
                    permissions=json.dumps(["read:own_profile", "update:own_profile"])
                ),
                Role(
                    name="guest",
                    description="Guest user with read-only access",
                    permissions=json.dumps(["read:public"])
                )
            ]
            
            for role in default_roles:
                db.add(role)
            
            db.commit()
            
        # Create default admin user if not exists
        admin_user = db.query(User).filter(User.email == "admin@magentic-ui.com").first()
        if not admin_user:
            admin_role = db.query(Role).filter(Role.name == "admin").first()
            admin_user = User(
                username="admin",
                email="admin@magentic-ui.com",
                full_name="System Administrator",
                password_hash=get_password_hash("admin123"),
                is_active=True,
                is_superuser=True
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            
            # Assign admin role
            if admin_role:
                admin_user.roles.append(admin_role)
                db.commit()
                
    finally:
        db.close()
