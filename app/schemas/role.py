"""
Role Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
import re


class RoleBase(BaseModel):
    """Base role schema with common fields."""
    name: str = Field(..., min_length=2, max_length=50, description="Role name")
    description: Optional[str] = Field(None, max_length=200, description="Role description")
    permissions: List[str] = Field(default_factory=list, description="List of permissions")


class RoleCreate(RoleBase):
    """Schema for role creation."""
    
    @validator('name')
    def validate_name(cls, v):
        """Validate role name format."""
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Role name can only contain letters, numbers, underscores, and hyphens')
        return v.lower()  # Convert to lowercase for consistency
    
    @validator('permissions')
    def validate_permissions(cls, v):
        """Validate permissions format."""
        valid_permissions = [
            '*',  # All permissions
            'read:users', 'create:users', 'update:users', 'delete:users',
            'read:roles', 'create:roles', 'update:roles', 'delete:roles',
            'read:own_profile', 'update:own_profile',
            'read:public'
        ]
        
        for permission in v:
            if permission not in valid_permissions:
                raise ValueError(f'Invalid permission: {permission}')
        
        return v


class RoleUpdate(BaseModel):
    """Schema for role updates."""
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    description: Optional[str] = Field(None, max_length=200)
    permissions: Optional[List[str]] = None
    
    @validator('name')
    def validate_name(cls, v):
        """Validate role name format."""
        if v and not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Role name can only contain letters, numbers, underscores, and hyphens')
        return v.lower() if v else v
    
    @validator('permissions')
    def validate_permissions(cls, v):
        """Validate permissions format."""
        if v is None:
            return v
            
        valid_permissions = [
            '*',  # All permissions
            'read:users', 'create:users', 'update:users', 'delete:users',
            'read:roles', 'create:roles', 'update:roles', 'delete:roles',
            'read:own_profile', 'update:own_profile',
            'read:public'
        ]
        
        for permission in v:
            if permission not in valid_permissions:
                raise ValueError(f'Invalid permission: {permission}')
        
        return v


class RoleResponse(RoleBase):
    """Schema for role response."""
    id: int
    created_at: datetime
    user_count: Optional[int] = Field(None, description="Number of users with this role")
    
    class Config:
        from_attributes = True


class RoleListResponse(BaseModel):
    """Schema for role list response."""
    roles: List[RoleResponse]
    total: int
    
    class Config:
        from_attributes = True


class UserRoleAssignment(BaseModel):
    """Schema for assigning roles to users."""
    role_ids: List[int] = Field(..., description="List of role IDs to assign")
    
    @validator('role_ids')
    def validate_role_ids(cls, v):
        """Validate role IDs."""
        if not v:
            raise ValueError('At least one role ID must be provided')
        
        if len(v) != len(set(v)):
            raise ValueError('Duplicate role IDs are not allowed')
        
        return v
