"""
聊天系统异常类定义
"""
class ChatSystemError(Exception):
    """聊天系统基础异常类"""
    pass

class HandlerNotFoundError(ChatSystemError):
    """找不到消息处理器异常"""
    pass

class MiddlewareError(ChatSystemError):
    """中间件处理异常"""
    pass

class MessageProcessError(ChatSystemError):
    """消息处理异常"""
    pass