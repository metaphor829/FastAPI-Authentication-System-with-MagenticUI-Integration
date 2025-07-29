# FastAPI Authentication System with Magentic-UI Integration - User Guide

This comprehensive guide will walk you through using the integrated authentication system with Magentic-UI.

## 🚀 Getting Started

### System Overview

Our system consists of two integrated components:
- **Authentication Server** (Port 8000): Secure user management and JWT authentication
- **Magentic-UI Interface** (Port 8081): AI-powered web interface with integrated user management

### Quick Start

1. **Launch the System**:
   ```bash
   # Terminal 1: Start Authentication Server
   python run.py
   
   # Terminal 2: Start Magentic-UI
   python start_magentic_ui.py
   ```

2. **Create Your Account**:
   - Visit http://localhost:8000/register
   - Fill in: username, email, password, full name
   - Click "Register"

3. **Login and Access**:
   - Visit http://localhost:8000/login
   - Enter your credentials
   - Automatic redirect to Magentic-UI with authentication

## 🔐 Authentication Flow

### Login Process
1. **Entry Point**: Always start at http://localhost:8000/login
2. **Credential Validation**: System verifies username/password
3. **Token Generation**: JWT token created for secure authentication
4. **Automatic Redirect**: Seamless transition to Magentic-UI
5. **User Session**: Full access to both systems with single login

### User Management Access
- **Location**: Click the user avatar (circle with your initial) in Magentic-UI's top-right corner
- **Features**: Complete profile management in a modern tabbed interface
- **Real-time Updates**: Changes reflect immediately across the system

## 👤 User Management Interface

### Profile Tab (👤 Profile)
**Current User Display**:
- Shows your active username
- Displays login status and user information

**Profile Editing**:
- **Username**: Read-only (cannot be changed for security)
- **Email**: Read-only (cannot be changed for security)  
- **Full Name**: Editable - update your display name
- **Save Changes**: Click "Update Profile" to save

**Real-time Features**:
- Avatar updates immediately with new name's first letter
- Changes sync across both systems instantly

### Password Tab (🔒 Password)
**Secure Password Management**:
- **Current Password**: Required for verification
- **New Password**: Enter your desired new password
- **Confirm Password**: Re-enter for validation
- **Security**: All password changes require current password

**Validation Features**:
- Password strength requirements
- Confirmation matching validation
- Secure bcrypt hashing

### Settings Tab (⚙️ Settings)
**Language Selection**:
- 🇺🇸 **English**: Default interface language
- 🇨🇳 **中文**: Simplified Chinese interface
- 🇯🇵 **日本語**: Japanese interface

**System Controls**:
- **Logout**: Secure logout from both systems
- **Preferences**: Settings are saved and persistent

## 🌍 Multi-language Support

### Language Features
- **Instant Switching**: Language changes apply immediately
- **Complete Translation**: All interface elements translate
- **Persistent Settings**: Language preference is remembered

### What Gets Translated
- All tab labels and headers
- Form fields and placeholders
- Button text and tooltips
- Error messages and notifications
- Success messages and confirmations

## 🔧 Advanced Features

### Cross-System Integration
**Single Sign-On (SSO)**:
- Login once, access both systems
- Seamless token passing between domains
- Automatic session synchronization

**Data Synchronization**:
- Profile changes reflect in both systems
- Real-time avatar updates
- Consistent user state management

### Security Features
**Authentication Security**:
- JWT token-based authentication
- Secure password hashing with bcrypt
- Cross-domain security measures
- Automatic token expiration

**Session Management**:
- Secure logout across both systems
- Token refresh for extended sessions
- Protection against unauthorized access

## 🛠️ Troubleshooting

### Common Issues and Solutions

**1. Cannot Access Magentic-UI**:
- ✅ Verify both servers are running (ports 8000 and 8081)
- ✅ Check for port conflicts
- ✅ Try hard refresh (Ctrl+Shift+R)

**2. Login Problems**:
- ✅ Verify credentials are correct
- ✅ Check if account exists (try registration)
- ✅ Ensure authentication server is accessible

**3. Profile Updates Not Saving**:
- ✅ Check internet connection
- ✅ Verify you're logged in
- ✅ Check browser console for errors

**4. Language Not Changing**:
- ✅ Try refreshing the page
- ✅ Clear browser cache
- ✅ Check if setting was saved in localStorage

## 📚 API Reference

### Authentication Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | User login |
| GET | `/api/auth/me` | Get current user |
| PUT | `/api/auth/me` | Update profile |
| PUT | `/api/auth/change-password` | Change password |

### Example Usage
```bash
# Register new user
curl -X POST "http://localhost:8000/api/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"username": "newuser", "email": "user@example.com", "password": "SecurePass123!", "full_name": "New User"}'

# Login
curl -X POST "http://localhost:8000/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "newuser", "password": "SecurePass123!"}'
```

## 🎯 Best Practices

### Security
- Use strong passwords with mixed characters
- Don't share login credentials
- Log out when finished, especially on shared computers
- Keep profile information up to date

### Usage
- Always start from http://localhost:8000/login for best experience
- Use the integrated user management interface for all profile changes
- Take advantage of multi-language support
- Keep both servers running for full functionality

## 🚀 Advanced Usage

### Development
```bash
# Database migrations
alembic revision --autogenerate -m "Description"
alembic upgrade head

# Frontend rebuild
cd magentic-ui-main/magentic-ui-main/frontend
npx gatsby clean
npx gatsby build --prefix-paths
robocopy public ..\src\magentic_ui\backend\web\ui /E /IS
```

This completes the user guide for the FastAPI Authentication System with Magentic-UI integration.
