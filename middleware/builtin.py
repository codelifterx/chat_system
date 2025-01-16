"""
内置中间件实现，包括日志记录和敏感词过滤
"""
from typing import List
from .base import Middleware
from core.message import MessageContext

class LoggingMiddleware(Middleware):
    """日志记录中间件：记录消息处理的开始和结束"""
    def before_process(self, context: MessageContext):
        print(f"收到来自 {context.sender} 的消息")
        return True

    def after_process(self, result: str, context: MessageContext):
        print(f"消息处理完成: {result}")
        return result

class SensitiveWordMiddleware(Middleware):
    """敏感词过滤中间件：检查消息是否包含敏感词"""
    def __init__(self, sensitive_words: List[str]):
        self.sensitive_words = sensitive_words

    def before_process(self, context: MessageContext):
        if isinstance(context.content, str):
            for word in self.sensitive_words:
                if word in context.content:
                    return False
        return True