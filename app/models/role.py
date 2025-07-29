"""
Role model definition.
"""
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime
import json

from app.database import Base
from app.models.user import user_roles


class Role(SQLModel, table=True):
    """Role model."""

    __tablename__ = "roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=50)
    description: Optional[str] = Field(default=None, max_length=200)
    permissions: str = Field(default="[]")  # JSON string for permissions
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def get_permissions(self) -> List[str]:
        """Get permissions as a list."""
        try:
            return json.loads(self.permissions)
        except (json.JSONDecodeError, TypeError):
            return []

    def set_permissions(self, permissions: List[str]) -> None:
        """Set permissions from a list."""
        self.permissions = json.dumps(permissions)


class RoleSQLAlchemy(Base):
    """SQLAlchemy Role model for relationships."""
    
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(200), nullable=True)
    permissions = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    # Relationships
    users = relationship("UserSQLAlchemy", secondary=user_roles, back_populates="roles")
    
    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"
    
    def has_permission(self, permission: str) -> bool:
        """Check if role has a specific permission."""
        perms = self.get_permissions()
        return "*" in perms or permission in perms

    def add_permission(self, permission: str) -> None:
        """Add a permission to this role."""
        perms = self.get_permissions()
        if permission not in perms:
            perms.append(permission)
            self.set_permissions(perms)

    def remove_permission(self, permission: str) -> None:
        """Remove a permission from this role."""
        perms = self.get_permissions()
        if permission in perms:
            perms.remove(permission)
            self.set_permissions(perms)
