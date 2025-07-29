"""
Utility helper functions.
"""
from typing import Optional, Dict, Any
from datetime import datetime
import re


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_username(username: str) -> bool:
    """
    Validate username format.
    
    Args:
        username: Username to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Username should be 3-50 characters, alphanumeric with underscores and hyphens
    pattern = r'^[a-zA-Z0-9_-]{3,50}$'
    return re.match(pattern, username) is not None


def validate_password_strength(password: str) -> Dict[str, Any]:
    """
    Validate password strength and return detailed feedback.
    
    Args:
        password: Password to validate
        
    Returns:
        dict: Validation result with details
    """
    result = {
        "valid": True,
        "errors": [],
        "score": 0,
        "suggestions": []
    }
    
    # Length check
    if len(password) < 8:
        result["valid"] = False
        result["errors"].append("Password must be at least 8 characters long")
    else:
        result["score"] += 1
    
    # Uppercase check
    if not re.search(r'[A-Z]', password):
        result["valid"] = False
        result["errors"].append("Password must contain at least one uppercase letter")
    else:
        result["score"] += 1
    
    # Lowercase check
    if not re.search(r'[a-z]', password):
        result["valid"] = False
        result["errors"].append("Password must contain at least one lowercase letter")
    else:
        result["score"] += 1
    
    # Number check
    if not re.search(r'\d', password):
        result["valid"] = False
        result["errors"].append("Password must contain at least one number")
    else:
        result["score"] += 1
    
    # Special character check
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        result["valid"] = False
        result["errors"].append("Password must contain at least one special character")
    else:
        result["score"] += 1
    
    # Additional strength checks
    if len(password) >= 12:
        result["score"] += 1
    
    if len(set(password)) >= len(password) * 0.7:  # Character diversity
        result["score"] += 1
    
    # Suggestions based on score
    if result["score"] < 3:
        result["suggestions"].append("Consider using a longer password")
        result["suggestions"].append("Mix uppercase, lowercase, numbers, and symbols")
    elif result["score"] < 5:
        result["suggestions"].append("Good password! Consider making it even longer")
    else:
        result["suggestions"].append("Excellent password strength!")
    
    return result


def sanitize_input(input_str: str) -> str:
    """
    Sanitize user input to prevent XSS and other attacks.
    
    Args:
        input_str: Input string to sanitize
        
    Returns:
        str: Sanitized string
    """
    if not input_str:
        return ""
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', input_str)
    
    # Trim whitespace
    sanitized = sanitized.strip()
    
    return sanitized


def format_datetime(dt: Optional[datetime]) -> Optional[str]:
    """
    Format datetime for API responses.
    
    Args:
        dt: Datetime object
        
    Returns:
        str: Formatted datetime string or None
    """
    if dt is None:
        return None
    
    return dt.isoformat() + "Z"


def paginate_query(query, page: int = 1, size: int = 20):
    """
    Add pagination to SQLAlchemy query.
    
    Args:
        query: SQLAlchemy query object
        page: Page number (1-based)
        size: Items per page
        
    Returns:
        tuple: (paginated_query, total_count)
    """
    # Ensure minimum values
    page = max(1, page)
    size = max(1, min(100, size))  # Limit max size to 100
    
    # Calculate offset
    offset = (page - 1) * size
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    paginated = query.offset(offset).limit(size)
    
    return paginated, total
