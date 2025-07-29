import React from "react";
import {
  StopCircle,
  MessageSquare,
  Loader2,
  AlertTriangle,
  PauseCircle,
  HelpCircle,
  CheckCircle,
  CreditCard,
  Key,
  Clock,
  Wifi,
} from "lucide-react";
import { Run, InputRequest } from "../types/datamodel";

// 智能错误解析函数
const parseErrorMessage = (errorMessage?: string): { message: string; icon: React.ReactNode; color: string; suggestion?: string } => {
  if (!errorMessage) {
    return {
      message: "An error occurred",
      icon: <AlertTriangle size={20} className="inline-block mr-2 text-red-500" />,
      color: "text-red-500"
    };
  }

  const errorLower = errorMessage.toLowerCase();

  // API余额不足
  if (errorLower.includes('insufficient credits') || errorLower.includes('402')) {
    return {
      message: "🚫 API余额不足",
      icon: <CreditCard size={20} className="inline-block mr-2 text-orange-500" />,
      color: "text-orange-500",
      suggestion: "请充值OpenRouter账户或配置自己的API密钥"
    };
  }

  // API密钥无效
  if (errorLower.includes('invalid api key') || errorLower.includes('unauthorized') || errorLower.includes('401')) {
    return {
      message: "🔑 API密钥无效",
      icon: <Key size={20} className="inline-block mr-2 text-red-500" />,
      color: "text-red-500",
      suggestion: "请检查并更新您的API密钥"
    };
  }

  // 速率限制
  if (errorLower.includes('rate limit') || errorLower.includes('too many requests') || errorLower.includes('429')) {
    return {
      message: "⏱️ 请求过于频繁",
      icon: <Clock size={20} className="inline-block mr-2 text-yellow-500" />,
      color: "text-yellow-500",
      suggestion: "请稍后再试或升级API计划"
    };
  }

  // 网络连接错误
  if (errorLower.includes('connection') || errorLower.includes('network') || errorLower.includes('timeout')) {
    return {
      message: "🌐 网络连接错误",
      icon: <Wifi size={20} className="inline-block mr-2 text-blue-500" />,
      color: "text-blue-500",
      suggestion: "请检查网络连接或稍后重试"
    };
  }

  // 配额用完
  if (errorLower.includes('quota') || errorLower.includes('exceeded')) {
    return {
      message: "📊 API配额已用完",
      icon: <AlertTriangle size={20} className="inline-block mr-2 text-orange-500" />,
      color: "text-orange-500",
      suggestion: "请检查账户余额或等待配额重置"
    };
  }

  // 默认错误
  return {
    message: errorMessage.length > 100 ? errorMessage.substring(0, 100) + "..." : errorMessage,
    icon: <AlertTriangle size={20} className="inline-block mr-2 text-red-500" />,
    color: "text-red-500"
  };
};

export const getStatusIcon = (
  status: Run["status"],
  errorMessage?: string,
  stopReason?: string,
  inputRequest?: InputRequest
) => {
  switch (status) {
    case "active":
      return (
        <div className="inline-block mr-1">
          <Loader2
            size={20}
            className="inline-block mr-1 text-accent animate-spin"
          />
          <span className="inline-block mr-2 ml-1 ">Processing</span>
        </div>
      );
    case "awaiting_input":
      const Icon =
        inputRequest?.input_type === "approval" ? HelpCircle : MessageSquare;
      return (
        <div className="flex items-center text-sm mb-2">
          {inputRequest?.input_type === "approval" ? (
            <div>
              <div className="flex items-center">
                <span>
                  <span className="font-semibold">Approval Request:</span>{" "}
                  {inputRequest.prompt || "Waiting for approval"}
                </span>
              </div>
            </div>
          ) : (
            <>
              <MessageSquare
                size={20}
                className="flex-shrink-0 mr-2 text-accent"
              />
              <span className="flex-1">Waiting for your input</span>
            </>
          )}
        </div>
      );
    case "complete":
      const completeError = parseErrorMessage(errorMessage);
      return (
        <div className="text-sm mb-2">
          <div className="flex items-start">
            {completeError.icon}
            <div className="flex-1">
              <div className={completeError.color}>{completeError.message}</div>
              {completeError.suggestion && (
                <div className="text-xs text-gray-600 mt-1">
                  💡 {completeError.suggestion}
                </div>
              )}
            </div>
          </div>
        </div>
      );
    case "error":
      const errorInfo = parseErrorMessage(errorMessage);
      return (
        <div className="text-sm mb-2">
          <div className="flex items-start">
            {errorInfo.icon}
            <div className="flex-1">
              <div className={errorInfo.color}>{errorInfo.message}</div>
              {errorInfo.suggestion && (
                <div className="text-xs text-gray-600 mt-1">
                  💡 {errorInfo.suggestion}
                </div>
              )}
            </div>
          </div>
        </div>
      );
    case "stopped":
      return (
        <div className="text-sm mb-2 mt-4">
          <StopCircle size={20} className="inline-block mr-2 text-red-500" />
          Task was stopped: {stopReason}
        </div>
      );
    case "pausing":
      return (
        <div className="text-sm mb-2">
          <Loader2
            size={20}
            className="inline-block mr-2 text-accent animate-spin"
          />
          <span className="inline-block mr-2 ml-1">Pausing</span>
        </div>
      );
    case "paused":
      return (
        <div className="text-sm mb-2">
          <PauseCircle size={20} className="inline-block mr-2 text-accent" />
          <span className="inline-block mr-2 ml-1">Paused</span>
        </div>
      );
    case "resuming":
      return (
        <div className="text-sm mb-2">
          <Loader2
            size={20}
            className="inline-block mr-2 text-accent animate-spin"
          />
          <span className="inline-block mr-2 ml-1">Resuming</span>
        </div>
      );
    default:
      return null;
  }
};

// SessionRunStatusIndicator: for sidebar session status
export const SessionRunStatusIndicator: React.FC<{
  status?: Run["status"] | "final_answer_awaiting_input";
}> = ({ status }) => {
  switch (status) {
    case "awaiting_input":
      return <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />;
    case "active":
      return <Loader2 className="w-3 h-3 animate-spin text-accent" />;
    case "final_answer_awaiting_input":
      return <CheckCircle className="w-3 h-3 text-green-500" />;
    case "error":
      return <AlertTriangle className="w-3 h-3 text-red-500" />;
    default:
      return null;
  }
};
