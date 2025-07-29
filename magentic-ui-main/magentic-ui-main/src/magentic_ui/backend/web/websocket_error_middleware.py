#!/usr/bin/env python3
"""
WebSocket错误处理中间件
拦截和处理API错误，发送用户友好的错误信息到前端
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from api_error_handler import APIErrorHandler

logger = logging.getLogger(__name__)

class WebSocketErrorMiddleware:
    """WebSocket错误处理中间件"""
    
    @staticmethod
    async def handle_api_error(
        websocket,
        run_id: int,
        error: Exception,
        original_send_message_func
    ) -> None:
        """
        处理API错误并发送用户友好的错误信息
        
        Args:
            websocket: WebSocket连接
            run_id: 运行ID
            error: 原始异常
            original_send_message_func: 原始的发送消息函数
        """
        try:
            error_str = str(error)
            logger.error(f"API error for run {run_id}: {error_str}")
            
            # 使用错误处理器解析错误
            error_info = APIErrorHandler.create_user_friendly_error(error_str)
            error_info['timestamp'] = datetime.now(timezone.utc).isoformat()
            
            # 发送详细的错误信息到前端
            error_message = {
                "type": "api_error",
                "run_id": run_id,
                "error_info": error_info,
                "timestamp": error_info['timestamp']
            }
            
            # 发送到WebSocket
            await original_send_message_func(run_id, error_message)
            
            # 同时发送一个系统消息显示在聊天中
            system_message = {
                "type": "message",
                "data": {
                    "source": "system",
                    "content": f"{error_info['title']}\n\n{error_info['message']}",
                    "metadata": {
                        "internal": "no",
                        "error_type": error_info['error_type'],
                        "has_solutions": len(error_info['solutions']) > 0
                    }
                },
                "timestamp": error_info['timestamp']
            }
            
            await original_send_message_func(run_id, system_message)
            
        except Exception as e:
            logger.error(f"Error in WebSocket error middleware: {e}")
            # 如果中间件本身出错，发送基本错误信息
            fallback_message = {
                "type": "error",
                "error": "An error occurred while processing your request",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            try:
                await original_send_message_func(run_id, fallback_message)
            except:
                pass  # 避免无限递归

    @staticmethod
    def is_api_error(error: Exception) -> bool:
        """
        判断是否为API相关错误
        
        Args:
            error: 异常对象
            
        Returns:
            bool: 是否为API错误
        """
        error_str = str(error).lower()
        
        api_error_indicators = [
            'insufficient credits',
            'invalid api key',
            'rate limit',
            'quota exceeded',
            'model not found',
            'unauthorized',
            'authentication failed',
            'connection error',
            'timeout',
            'openai',
            'openrouter',
            'anthropic'
        ]
        
        return any(indicator in error_str for indicator in api_error_indicators)

    @staticmethod
    def patch_connection_manager(connection_manager):
        """
        为连接管理器添加错误处理中间件
        
        Args:
            connection_manager: WebSocket连接管理器实例
        """
        # 保存原始的错误处理方法
        original_handle_stream_error = connection_manager._handle_stream_error
        original_send_message = connection_manager._send_message
        
        async def enhanced_handle_stream_error(run_id: int, error: Exception) -> None:
            """增强的流错误处理"""
            try:
                # 检查是否为API错误
                if WebSocketErrorMiddleware.is_api_error(error):
                    # 使用我们的错误处理中间件
                    await WebSocketErrorMiddleware.handle_api_error(
                        None,  # websocket对象在这里不需要
                        run_id,
                        error,
                        original_send_message
                    )
                else:
                    # 对于非API错误，使用原始处理方法
                    await original_handle_stream_error(run_id, error)
                    
            except Exception as e:
                logger.error(f"Error in enhanced error handler: {e}")
                # 回退到原始处理方法
                await original_handle_stream_error(run_id, error)
        
        # 替换原始方法
        connection_manager._handle_stream_error = enhanced_handle_stream_error
        
        logger.info("WebSocket error middleware patched successfully")

# 使用示例
def apply_error_middleware(app):
    """
    为FastAPI应用应用错误处理中间件
    
    Args:
        app: FastAPI应用实例
    """
    @app.middleware("http")
    async def error_handling_middleware(request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            if WebSocketErrorMiddleware.is_api_error(e):
                error_info = APIErrorHandler.create_user_friendly_error(str(e))
                return {
                    "status": False,
                    "error_info": error_info,
                    "message": error_info['title']
                }
            else:
                # 重新抛出非API错误
                raise e

# 测试函数
if __name__ == "__main__":
    # 测试错误检测
    test_errors = [
        Exception("Error code: 402 - {'error': {'message': 'Insufficient credits'}}"),
        Exception("Invalid API key provided"),
        Exception("Some random error"),
        Exception("Connection timeout"),
        Exception("Rate limit exceeded")
    ]
    
    print("🧪 WebSocket错误中间件测试")
    print("=" * 50)
    
    for i, error in enumerate(test_errors, 1):
        is_api_error = WebSocketErrorMiddleware.is_api_error(error)
        print(f"{i}. {str(error)[:50]}...")
        print(f"   是API错误: {'✅' if is_api_error else '❌'}")
    
    print("\n" + "=" * 50)
    print("✅ 测试完成")
