"""
FastAPI application entry point for Magentic-UI Authentication System.
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.config import settings
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print("Starting up Magentic-UI Authentication System...")
    init_db()
    print("Database initialized successfully")
    yield
    # Shutdown
    print("Shutting down...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Authentication and authorization system for Magentic-UI",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=False,  # Set to False when using allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Magentic-UI Authentication System",
        "version": settings.app_version,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": "2025-07-17T00:00:00Z"
    }


# 创建静态文件目录（如果不存在）
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

# 挂载静态文件
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include API routers - 顺序很重要！
from app.api import proxy, auth, web

# 1. 首先包含认证路由（最高优先级）
app.include_router(auth.router, prefix="/api", tags=["authentication"])

# 2. 然后包含Web页面路由
app.include_router(web.router, tags=["web"])

# 3. 最后包含代理路由（最低优先级，包含catch-all）
app.include_router(proxy.router, tags=["proxy"])

# Future routers (will be added in next phase)
# from app.api import users, roles
# app.include_router(users.router, prefix="/users", tags=["users"])
# app.include_router(roles.router, prefix="/roles", tags=["roles"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
