"""
中间件基类定义，提供消息处理前后的钩子方法
"""
from core.message import MessageContext

class Middleware:
    def before_process(self, context: MessageContext) -> bool:
        """消息处理前的钩子方法"""
        return True

    def after_process(self, result: str, context: MessageContext) -> str:
        """消息处理后的钩子方法"""
        return result