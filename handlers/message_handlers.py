"""
定义各种类型消息的具体处理函数
"""
from core.message import message_handler, MessageContext

# 文本消息处理器
@message_handler("text", priority=1)
def handle_text(ctx: MessageContext) -> str:
    return f"[文本消息] {ctx.sender}: {ctx.content}"

# 图片消息处理器
@message_handler("image", priority=1)
def handle_image(ctx: MessageContext) -> str:
    return f"[图片消息] {ctx.sender} 分享了图片: {ctx.content}"

# 位置消息处理器
@message_handler("location", priority=1)
def handle_location(ctx: MessageContext) -> str:
    return f"[位置消息] {ctx.sender} 分享了位置: {ctx.content}"