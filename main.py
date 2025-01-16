"""
聊天系统的主程序入口
"""
from pathlib import Path

from core.chat_system import ChatSystem
from core.config import ChatSystemConfig
from middleware.builtin import LoggingMiddleware, SensitiveWordMiddleware
from handlers import message_handlers

def main():
    # 加载配置
    config_path = Path(__file__).parent / "config" / "default_config.json"
    config = ChatSystemConfig.load_from_file(str(config_path))

    # 创建聊天系统实例
    chat_system = ChatSystem(config)

    # 注册消息处理器
    chat_system.register_handlers(message_handlers)

    # 添加中间件
    chat_system.add_middleware(LoggingMiddleware())
    if config.enable_sensitive_filter:
        chat_system.add_middleware(
            SensitiveWordMiddleware(config.sensitive_words)
        )

    # 测试消息处理
    test_messages = [
        ("text", "你好，世界！", "张三"),
        ("image", "风景照片.jpg", "李四"),
        ("location", "北京市海淀区", "王五"),
        ("text", "这是一条包含敏感词1的消息", "赵六"),
        ("unknown", "未知类型消息", "钱七"),
        ("text", "测试" * 1000, "周九")
    ]

    print("开始测试消息处理系统：\n")
    for msg_type, content, sender in test_messages:
        print(f"\n处理消息: {msg_type} - {content}")
        result = chat_system.process_message(msg_type, content, sender)
        print(f"处理结果: {result}")

if __name__ == "__main__":
    main()