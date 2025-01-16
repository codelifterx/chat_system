"""
聊天系统的核心类，负责消息处理、中间件管理和处理器注册
"""
from datetime import datetime
import inspect
import logging
from typing import Any, Dict, List
from .message import MessageContext
from .exceptions import ChatSystemError, HandlerNotFoundError, MiddlewareError, MessageProcessError
from middleware.base import Middleware
from .config import ChatSystemConfig
from pathlib import Path

class ChatSystem:
    def __init__(self, config: ChatSystemConfig = None):
        """
        初始化聊天系统

        Args:
            config: 系统配置，如果为None则使用默认配置
        """
        self.config = config or ChatSystemConfig()
        self.handlers = {}
        self.middlewares: List[Middleware] = []
        self.message_log = []

        # 配置日志
        logging.basicConfig(
            level=getattr(logging, self.config.log_level),
            format=self.config.log_format
        )
        self.logger = logging.getLogger(__name__)

        # 创建存储目录
        if self.config.enable_message_history:
            Path(self.config.storage_path).mkdir(parents=True, exist_ok=True)

    def register_handlers(self, module):
        """
        注册模块中所有带有 handle_type 属性的函数作为消息处理器

        Args:
            module: 包含处理器函数的模块

        Raises:
            ChatSystemError: 注册过程中出现错误
        """
        try:
            for name, obj in inspect.getmembers(module):
                if inspect.isfunction(obj) and hasattr(obj, "handle_type"):
                    msg_type = obj.handle_type
                    if msg_type not in self.handlers:
                        self.handlers[msg_type] = []
                    self.handlers[msg_type].append(obj)
                    self.handlers[msg_type].sort(
                        key=lambda x: getattr(x, "priority", 0),
                        reverse=True
                    )
            self.logger.info(f"成功注册处理器，当前支持的消息类型: {list(self.handlers.keys())}")
        except Exception as e:
            self.logger.error(f"注册处理器时出错: {str(e)}")
            raise ChatSystemError(f"注册处理器失败: {str(e)}")

    def add_middleware(self, middleware: Middleware):
        """
        添加中间件到处理链中

        Args:
            middleware: 中间件实例
        """
        try:
            self.middlewares.append(middleware)
            self.logger.info(f"成功添加中间件: {middleware.__class__.__name__}")
        except Exception as e:
            self.logger.error(f"添加中间件时出错: {str(e)}")
            raise MiddlewareError(f"添加中间件失败: {str(e)}")

    def process_message(self, msg_type: str, content: Any, sender: str) -> str:
        """
        处理消息的主要方法，包括中间件处理和消息处理器的调用

        Args:
            msg_type: 消息类型
            content: 消息内容
            sender: 发送者

        Returns:
            str: 处理结果

        Raises:
            HandlerNotFoundError: 找不到对应的消息处理器
            MessageProcessError: 消息处理过程中出现错误
        """
        context = None
        try:
            # 检查消息类型是否支持
            if msg_type not in self.config.supported_message_types:
                raise HandlerNotFoundError(f"不支持的消息类型：{msg_type}")

            # 检查消息长度
            if isinstance(content, str) and len(content) > self.config.max_message_length:
                return f"消息长度超过限制 ({self.config.max_message_length})"

            context = MessageContext(content, datetime.now(), sender)
            self.logger.info(f"开始处理来自 {sender} 的 {msg_type} 类型消息")

            # 中间件前置处理
            for middleware in self.middlewares:
                try:
                    if not middleware.before_process(context):
                        self.logger.info(f"消息被中间件 {middleware.__class__.__name__} 拦截")
                        return "消息被中间件拦截"
                except Exception as e:
                    self.logger.error(f"中间件 {middleware.__class__.__name__} 处理出错: {str(e)}")
                    raise MiddlewareError(f"中间件处理失败: {str(e)}")

            # 获取并执行处理器
            handler_list = self.handlers.get(msg_type, [])
            if not handler_list:
                self.logger.warning(f"未找到消息类型 {msg_type} 的处理器")
                raise HandlerNotFoundError(f"不支持的消息类型：{msg_type}")

            try:
                result = handler_list[0](context)
                self.message_log.append((msg_type, context))
            except Exception as e:
                self.logger.error(f"消息处理器执行出错: {str(e)}")
                raise MessageProcessError(f"消息处理失败: {str(e)}")

            # 中间件后置处理
            for middleware in reversed(self.middlewares):
                try:
                    result = middleware.after_process(result, context)
                except Exception as e:
                    self.logger.error(f"中间件 {middleware.__class__.__name__} 后置处理出错: {str(e)}")
                    raise MiddlewareError(f"中间件后置处理失败: {str(e)}")

            self.logger.info("消息处理完成")
            return result

        except ChatSystemError as e:
            self.logger.error(str(e))
            return f"处理失败: {str(e)}"

        except Exception as e:
            self.logger.error(f"系统错误: {str(e)}", exc_info=True)
            return f"系统错误: {str(e)}"