"""
定义消息相关的装饰器和消息上下文类
"""
from datetime import datetime
from typing import Any, Callable

def message_handler(msg_type: str, priority: int = 0):
    """装饰器：用于标记消息处理函数，指定其处理的消息类型和优先级"""
    def decorator(func: Callable) -> Callable:
        func.handle_type = msg_type
        func.priority = priority
        return func
    return decorator

class MessageContext:
    """消息上下文类，包含消息的内容、时间戳和发送者信息"""
    def __init__(self, content: Any, timestamp: datetime, sender: str):
        self.content = content
        self.timestamp = timestamp
        self.sender = sender