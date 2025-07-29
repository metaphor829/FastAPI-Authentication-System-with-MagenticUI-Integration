#!/usr/bin/env python3
"""
API错误处理器
专门处理OpenRouter、OpenAI等API提供商的错误，并提供用户友好的错误信息
"""

import re
import json
from typing import Dict, Any, Optional, Tuple
from enum import Enum

class APIErrorType(Enum):
    INSUFFICIENT_CREDITS = "insufficient_credits"
    INVALID_API_KEY = "invalid_api_key"
    RATE_LIMIT = "rate_limit"
    MODEL_NOT_FOUND = "model_not_found"
    QUOTA_EXCEEDED = "quota_exceeded"
    NETWORK_ERROR = "network_error"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"

class APIErrorHandler:
    """API错误处理器，将原始错误转换为用户友好的错误信息"""
    
    @staticmethod
    def parse_error(error_message: str, status_code: int = None) -> Tuple[APIErrorType, str, str]:
        """
        解析API错误并返回错误类型、用户友好消息和建议操作
        
        Args:
            error_message: 原始错误消息
            status_code: HTTP状态码
            
        Returns:
            Tuple[APIErrorType, str, str]: (错误类型, 用户消息, 建议操作)
        """
        error_message_lower = error_message.lower()
        
        # OpenRouter余额不足
        if "insufficient credits" in error_message_lower:
            return (
                APIErrorType.INSUFFICIENT_CREDITS,
                "🚫 API余额不足",
                "您的OpenRouter账户余额不足。请充值或切换到自己的API密钥。"
            )
        
        # OpenAI余额不足
        if "insufficient_quota" in error_message_lower or "quota exceeded" in error_message_lower:
            return (
                APIErrorType.QUOTA_EXCEEDED,
                "🚫 API配额已用完",
                "您的API配额已用完。请检查账户余额或等待配额重置。"
            )
        
        # API密钥无效
        if any(phrase in error_message_lower for phrase in [
            "invalid api key", "unauthorized", "authentication failed", 
            "invalid_api_key", "incorrect api key"
        ]):
            return (
                APIErrorType.INVALID_API_KEY,
                "🔑 API密钥无效",
                "您的API密钥无效或已过期。请检查并更新您的API密钥。"
            )
        
        # 速率限制
        if any(phrase in error_message_lower for phrase in [
            "rate limit", "too many requests", "rate_limit_exceeded"
        ]):
            return (
                APIErrorType.RATE_LIMIT,
                "⏱️ 请求过于频繁",
                "您的请求过于频繁，请稍后再试或升级到更高级别的API计划。"
            )
        
        # 模型不存在
        if any(phrase in error_message_lower for phrase in [
            "model not found", "invalid model", "model does not exist"
        ]):
            return (
                APIErrorType.MODEL_NOT_FOUND,
                "🤖 模型不可用",
                "所选择的AI模型不存在或不可用。请选择其他模型。"
            )
        
        # 网络错误
        if any(phrase in error_message_lower for phrase in [
            "connection error", "network error", "connection timeout",
            "failed to connect", "connection refused"
        ]):
            return (
                APIErrorType.NETWORK_ERROR,
                "🌐 网络连接错误",
                "无法连接到API服务器。请检查网络连接或稍后重试。"
            )
        
        # 超时错误
        if any(phrase in error_message_lower for phrase in [
            "timeout", "request timeout", "read timeout"
        ]):
            return (
                APIErrorType.TIMEOUT,
                "⏰ 请求超时",
                "API请求超时。这可能是由于免费模型响应较慢，请稍后重试或使用付费模型。"
            )
        
        # 默认未知错误
        return (
            APIErrorType.UNKNOWN,
            "❌ 发生未知错误",
            f"发生了未知错误：{error_message[:100]}{'...' if len(error_message) > 100 else ''}"
        )
    
    @staticmethod
    def create_user_friendly_error(error_message: str, status_code: int = None) -> Dict[str, Any]:
        """
        创建用户友好的错误响应
        
        Args:
            error_message: 原始错误消息
            status_code: HTTP状态码
            
        Returns:
            Dict: 包含错误信息和建议的字典
        """
        error_type, user_message, suggestion = APIErrorHandler.parse_error(error_message, status_code)
        
        # 根据错误类型提供具体的解决方案
        solutions = []
        
        if error_type == APIErrorType.INSUFFICIENT_CREDITS:
            solutions = [
                {
                    "title": "💳 为OpenRouter账户充值",
                    "description": "访问OpenRouter设置页面为账户充值",
                    "action": "open_url",
                    "url": "https://openrouter.ai/settings/credits",
                    "primary": True
                },
                {
                    "title": "🔑 使用自己的API密钥",
                    "description": "配置您自己的OpenAI或其他API密钥",
                    "action": "open_settings",
                    "primary": False
                },
                {
                    "title": "🆓 尝试其他免费模型",
                    "description": "切换到其他可用的免费模型",
                    "action": "suggest_models",
                    "models": ["meta-llama/llama-3.2-3b-instruct:free", "microsoft/phi-3-mini-128k-instruct:free"],
                    "primary": False
                }
            ]
        
        elif error_type == APIErrorType.INVALID_API_KEY:
            solutions = [
                {
                    "title": "🔧 检查API密钥",
                    "description": "确认API密钥是否正确复制",
                    "action": "open_settings",
                    "primary": True
                },
                {
                    "title": "🔄 重新生成API密钥",
                    "description": "在API提供商网站重新生成密钥",
                    "action": "open_url",
                    "url": "https://openrouter.ai/keys",
                    "primary": False
                }
            ]
        
        elif error_type == APIErrorType.QUOTA_EXCEEDED:
            solutions = [
                {
                    "title": "💰 检查账户余额",
                    "description": "确认账户是否有足够余额",
                    "action": "open_url",
                    "url": "https://platform.openai.com/account/billing",
                    "primary": True
                },
                {
                    "title": "⏳ 等待配额重置",
                    "description": "等待API配额在下个周期重置",
                    "action": "wait",
                    "primary": False
                }
            ]
        
        elif error_type == APIErrorType.RATE_LIMIT:
            solutions = [
                {
                    "title": "⏱️ 稍后重试",
                    "description": "等待几分钟后再次尝试",
                    "action": "retry_later",
                    "primary": True
                },
                {
                    "title": "📈 升级API计划",
                    "description": "升级到更高级别的API计划",
                    "action": "open_url",
                    "url": "https://openrouter.ai/settings/credits",
                    "primary": False
                }
            ]
        
        else:
            solutions = [
                {
                    "title": "🔄 重试请求",
                    "description": "稍后重新尝试您的请求",
                    "action": "retry",
                    "primary": True
                },
                {
                    "title": "⚙️ 检查设置",
                    "description": "检查您的API配置设置",
                    "action": "open_settings",
                    "primary": False
                }
            ]
        
        return {
            "error_type": error_type.value,
            "title": user_message,
            "message": suggestion,
            "solutions": solutions,
            "original_error": error_message,
            "status_code": status_code,
            "timestamp": None  # 可以在调用时添加
        }

# 使用示例和测试
if __name__ == "__main__":
    # 测试不同类型的错误
    test_errors = [
        "Error code: 402 - {'error': {'message': 'Insufficient credits. Add more using https://openrouter.ai/settings/credits', 'code': 402}}",
        "Invalid API key provided",
        "Rate limit exceeded. Please try again later.",
        "Model 'gpt-5' not found",
        "Connection timeout after 30 seconds",
        "Some unknown error occurred"
    ]
    
    print("🧪 API错误处理器测试")
    print("=" * 50)
    
    for i, error in enumerate(test_errors, 1):
        print(f"\n{i}. 测试错误: {error[:50]}...")
        result = APIErrorHandler.create_user_friendly_error(error)
        print(f"   类型: {result['error_type']}")
        print(f"   标题: {result['title']}")
        print(f"   建议: {result['message']}")
        print(f"   解决方案数量: {len(result['solutions'])}")
        if result['solutions']:
            print(f"   主要解决方案: {result['solutions'][0]['title']}")
    
    print("\n" + "=" * 50)
    print("✅ 测试完成")
