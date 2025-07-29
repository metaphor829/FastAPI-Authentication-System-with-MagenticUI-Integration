"""
Proxy middleware for Magentic-UI integration.
"""
import httpx
import json
from fastapi import Request, Response, HTTPException
from fastapi.responses import StreamingResponse
from typing import Optional
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class MagenticUIProxy:
    """Proxy class for forwarding requests to Magentic-UI."""

    def __init__(self, magentic_ui_url: str = None):
        self.magentic_ui_url = (magentic_ui_url or settings.magentic_ui_url).rstrip('/')
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def forward_request(
        self, 
        request: Request, 
        path: str,
        openai_api_key: Optional[str] = None
    ) -> Response:
        """
        Forward request to Magentic-UI with optional API key injection.
        
        Args:
            request: FastAPI request object
            path: Target path on Magentic-UI
            openai_api_key: OpenAI API key to inject
            
        Returns:
            Response from Magentic-UI
        """
        try:
            # Build target URL
            target_url = f"{self.magentic_ui_url}/{path.lstrip('/')}"
            
            # Get request body
            body = await request.body()
            
            # Prepare headers
            headers = dict(request.headers)
            
            # Remove host header to avoid conflicts
            headers.pop('host', None)
            
            # Inject OpenAI API key if provided
            if openai_api_key:
                headers['Authorization'] = f'Bearer {openai_api_key}'
                
                # Also try to inject into request body if it's JSON
                if body and request.headers.get('content-type', '').startswith('application/json'):
                    try:
                        body_json = json.loads(body)
                        if isinstance(body_json, dict):
                            body_json['api_key'] = openai_api_key
                            body = json.dumps(body_json).encode()
                            headers['content-length'] = str(len(body))
                    except (json.JSONDecodeError, TypeError):
                        pass
            
            # Forward the request
            response = await self.client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                params=request.query_params
            )
            
            # Prepare response headers
            response_headers = dict(response.headers)
            
            # Remove headers that might cause issues
            response_headers.pop('content-encoding', None)
            response_headers.pop('transfer-encoding', None)
            
            # Return response
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=response_headers,
                media_type=response.headers.get('content-type')
            )
            
        except httpx.RequestError as e:
            logger.error(f"Request error when forwarding to Magentic-UI: {e}")
            raise HTTPException(
                status_code=502, 
                detail=f"Failed to connect to Magentic-UI: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error in proxy: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Proxy error: {str(e)}"
            )
    
    async def forward_streaming_request(
        self, 
        request: Request, 
        path: str,
        openai_api_key: Optional[str] = None
    ) -> StreamingResponse:
        """
        Forward streaming request to Magentic-UI (for SSE/WebSocket-like responses).
        
        Args:
            request: FastAPI request object
            path: Target path on Magentic-UI
            openai_api_key: OpenAI API key to inject
            
        Returns:
            Streaming response from Magentic-UI
        """
        try:
            target_url = f"{self.magentic_ui_url}/{path.lstrip('/')}"
            body = await request.body()
            
            headers = dict(request.headers)
            headers.pop('host', None)
            
            if openai_api_key:
                headers['Authorization'] = f'Bearer {openai_api_key}'
            
            async def generate():
                async with httpx.stream(
                    method=request.method,
                    url=target_url,
                    headers=headers,
                    content=body,
                    params=request.query_params,
                    timeout=60.0
                ) as response:
                    async for chunk in response.aiter_bytes():
                        yield chunk
            
            return StreamingResponse(
                generate(),
                media_type="text/plain"
            )
            
        except Exception as e:
            logger.error(f"Streaming proxy error: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Streaming proxy error: {str(e)}"
            )
    
    async def health_check(self) -> dict:
        """Check if Magentic-UI is accessible."""
        try:
            response = await self.client.get(f"{self.magentic_ui_url}/")
            return {
                "magentic_ui_status": "accessible",
                "status_code": response.status_code,
                "url": self.magentic_ui_url
            }
        except Exception as e:
            return {
                "magentic_ui_status": "inaccessible",
                "error": str(e),
                "url": self.magentic_ui_url
            }
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


# Global proxy instance
proxy = MagenticUIProxy()
