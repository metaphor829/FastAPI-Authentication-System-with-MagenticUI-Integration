"""
Proxy API routes for Magentic-UI integration.
"""
from fastapi import APIRouter, Request, Response, HTTPException, Depends
from fastapi.responses import StreamingResponse, HTMLResponse
import os
from typing import Optional

from app.proxy import proxy
from app.config import settings

router = APIRouter()


def get_openai_api_key() -> Optional[str]:
    """Get OpenAI API key from environment or settings."""
    return os.getenv("OPENAI_API_KEY") or settings.openai_api_key


@router.get("/proxy/health")
async def proxy_health():
    """Check proxy and Magentic-UI health."""
    health_info = await proxy.health_check()
    return {
        "proxy_status": "running",
        "openai_api_key_configured": bool(get_openai_api_key()),
        **health_info
    }


@router.get("/proxy/config")
async def proxy_config():
    """Get proxy configuration."""
    return {
        "magentic_ui_url": proxy.magentic_ui_url,
        "openai_api_key_configured": bool(get_openai_api_key()),
        "proxy_enabled": True
    }


@router.post("/proxy/config")
async def update_proxy_config(config: dict):
    """Update proxy configuration."""
    if "magentic_ui_url" in config:
        proxy.magentic_ui_url = config["magentic_ui_url"].rstrip('/')
    
    return {
        "message": "Configuration updated",
        "magentic_ui_url": proxy.magentic_ui_url
    }


# 移除首页路由，让web.py处理
# @router.get("/", response_class=HTMLResponse)
# 这个路由被移除，因为它会与认证系统的首页冲突


@router.api_route("/ui/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_to_magentic_ui(request: Request, path: str = ""):
    """
    Proxy all requests to Magentic-UI with API key injection.
    
    This endpoint forwards all requests to the Magentic-UI instance,
    automatically injecting the OpenAI API key.
    """
    api_key = get_openai_api_key()
    
    if not api_key:
        raise HTTPException(
            status_code=400,
            detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
        )
    
    # Check if this might be a streaming request
    accept_header = request.headers.get("accept", "")
    if "text/event-stream" in accept_header or "stream" in request.url.query:
        return await proxy.forward_streaming_request(request, path, api_key)
    else:
        return await proxy.forward_request(request, path, api_key)


@router.get("/ui")
async def redirect_to_magentic_ui_root(request: Request):
    """Redirect /ui to /ui/ for proper routing."""
    return await proxy_to_magentic_ui(request, "")


# 临时API端点，用于测试前端连接
@router.get("/ui/api/sessions/")
async def get_sessions(user_id: str = "guestuser@gmail.com"):
    """临时sessions API端点"""
    return {
        "status": True,
        "data": [
            {
                "id": 1,
                "name": "Test Session",
                "user_id": user_id,
                "created_at": "2025-01-27T10:00:00Z"
            }
        ]
    }


@router.get("/ui/api/sessions/{session_id}/runs")
async def get_session_runs(session_id: int, user_id: str = "guestuser@gmail.com"):
    """临时session runs API端点"""
    return {
        "status": True,
        "data": {
            "runs": []
        }
    }


@router.get("/ui/api/plans/")
async def get_plans(user_id: str = "guestuser@gmail.com"):
    """临时plans API端点"""
    return {
        "status": True,
        "data": []
    }


@router.get("/ui/api/settings/")
async def get_settings(user_id: str = "guestuser@gmail.com"):
    """临时settings API端点"""
    return {
        "status": True,
        "data": {
            "config": {}
        }
    }


# Catch-all route for any other paths that should go to Magentic-UI
@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def catch_all_proxy(request: Request, path: str):
    """
    Catch-all proxy route for any paths not handled by other routes.
    Only forwards if the path looks like it should go to Magentic-UI.
    """
    # 排除认证相关的路径，避免冲突
    excluded_paths = ["api/auth", "login", "register", "docs", "openapi.json", "health"]

    # 如果是被排除的路径，不进行代理
    if any(path.startswith(p) for p in excluded_paths):
        raise HTTPException(status_code=404, detail="Path not found")

    # 只代理特定的路径到Magentic-UI
    proxy_paths = ["static", "assets", "_next", "chat", "conversation"]

    if any(path.startswith(p) for p in proxy_paths):
        api_key = get_openai_api_key()
        if api_key:
            return await proxy.forward_request(request, path, api_key)

    # 如果不是代理路径，返回404
    raise HTTPException(status_code=404, detail="Path not found")
