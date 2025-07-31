# FastAPI Authentication System with Magentic-UI Integration

A comprehensive authentication system built with FastAPI, featuring user management, JWT tokens, and seamless integration with Magentic-UI web interface.

> **About Magentic-UI**: Magentic-UI is Microsoft's open-source web interface for AI agents, providing a modern React-based UI for interacting with AI systems. Learn more at [microsoft/magentic-ui](https://github.com/microsoft/magentic-ui).

## 🚀 Features

### Authentication System
- **User Registration & Login** - Complete user management with secure authentication
- **JWT Token Authentication** - Stateless authentication with refresh tokens
- **Password Security** - bcrypt hashing with salt for password protection
- **Database Management** - SQLite with SQLAlchemy ORM and Alembic migrations
- **CORS Support** - Cross-origin requests for frontend integration
- **API Documentation** - Interactive Swagger UI documentation

### Magentic-UI Integration
- **Seamless SSO** - Single sign-on between authentication system and Magentic-UI
- **User Profile Sync** - Real-time synchronization of user data
- **Multi-language Support** - English, Chinese, and Japanese interface
- **Advanced User Management** - Profile editing, password changes, and settings
- **Cross-domain Authentication** - Secure token passing between systems

## 🛠️ Tech Stack

- **Backend**: FastAPI 0.104+
- **Frontend**: React + Gatsby (Magentic-UI)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT with python-jose
- **Password Security**: bcrypt via passlib
- **Validation**: Pydantic v2
- **Migrations**: Alembic
- **UI Framework**: Ant Design + Tailwind CSS
- **Build Tools**: Gatsby, Webpack

## 🛠️ Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+ (for Magentic-UI frontend)
- Git

### Installation

1. **Clone and Setup**:
```bash
git clone <repository-url>
cd fastapi-practice
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

2. **Initialize Database**:
```bash
alembic upgrade head
```

3. **Install Magentic-UI Dependencies**:
```bash
cd magentic-ui-main/magentic-ui-main/frontend
npm install
```

### Running the Application

1. **Start Authentication Server** (Terminal 1):
```bash
python run.py
```
🌐 API: http://localhost:8000

2. **Start Magentic-UI** (Terminal 2):
```bash
python start_magentic_ui.py
```
🌐 UI: http://localhost:8081

### First Time Setup

1. Visit http://localhost:8000/register to create an account
2. Login at http://localhost:8000/login
3. You'll be redirected to Magentic-UI with authentication
4. Click the user avatar to access the full management interface

## 📚 API Reference

### Authentication Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | User login |
| GET | `/api/auth/me` | Get current user |
| PUT | `/api/auth/me` | Update user profile |
| PUT | `/api/auth/change-password` | Change password |

### Web Interface
| Route | Description |
|-------|-------------|
| `/login` | Login page |
| `/register` | Registration page |
| `/dashboard` | User dashboard |

## 🏗️ Project Architecture

```
fastapi-practice/
├── app/                          # FastAPI Application
│   ├── api/                      # API Routes
│   │   ├── auth.py              # Authentication endpoints
│   │   ├── proxy.py             # Proxy for Magentic-UI
│   │   └── web.py               # Web interface routes
│   ├── core/                     # Core Components
│   │   ├── auth.py              # JWT authentication logic
│   │   └── security.py          # Password hashing
│   ├── models/                   # Database Models
│   │   └── user.py              # User model
│   ├── schemas/                  # Pydantic Schemas
│   │   └── user.py              # User validation schemas
│   ├── static/                   # Static Assets
│   ├── templates/                # HTML Templates
│   └── utils/                    # Utility Functions
├── magentic-ui-main/            # Magentic-UI Integration
│   └── magentic-ui-main/
│       ├── frontend/            # React Frontend
│       │   └── src/components/  # Modified components
│       └── src/                 # Python Backend
├── alembic/                     # Database Migrations
├── requirements.txt             # Python Dependencies
├── run.py                       # FastAPI Server Launcher
└── start_magentic_ui.py        # Magentic-UI Launcher
```

## ⚙️ Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=sqlite:///./magentic_auth.db

# JWT Configuration
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Settings
ALLOWED_ORIGINS=http://localhost:8081,http://127.0.0.1:8081
```

## 🔧 Development

### Database Operations
```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Frontend Development
```bash
cd magentic-ui-main/magentic-ui-main/frontend

# Clean build cache
npx gatsby clean

# Build for production
npx gatsby build --prefix-paths

# Copy to backend
robocopy public ..\src\magentic_ui\backend\web\ui /E /IS
```

## 🌟 Key Features Explained

### Cross-System Authentication
- JWT tokens passed via URL parameters during redirect
- Automatic token validation and user data synchronization
- Secure logout across both systems

### Multi-language Support
- Dynamic language switching in user interface
- Persistent language preferences
- Support for English, Chinese (Simplified), and Japanese

### User Management
- Real-time profile updates with immediate UI reflection
- Secure password changes with validation
- Avatar generation based on user names

## 📖 Documentation

- **API Docs**: http://localhost:8000/docs (Interactive Swagger UI)
- **User Guide**: See `user_guide.md` for detailed usage instructions

## 🤝 Contributing

This project is for educational purposes. Feel free to explore and modify the code to learn about:
- FastAPI development
- JWT authentication
- React/Gatsby frontend integration
- Cross-domain authentication patterns
- Multi-language web applications

## 📄 License

Educational use only.
