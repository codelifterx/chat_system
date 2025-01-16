"""
系统配置管理模块
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List
import json
from pathlib import Path

@dataclass
class ChatSystemConfig:
    """聊天系统配置类"""
    # 基础配置
    max_message_length: int = 1000
    enable_logging: bool = True
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # 存储配置
    storage_path: str = "./chat_logs"
    enable_message_history: bool = True

    # 中间件配置
    enable_sensitive_filter: bool = True
    sensitive_words: List[str] = field(default_factory=list)

    # 处理器配置
    supported_message_types: List[str] = field(
        default_factory=lambda: ["text", "image", "location"]
    )

    @classmethod
    def load_from_file(cls, config_path: str) -> 'ChatSystemConfig':
        """从JSON文件加载配置"""
        path = Path(config_path)
        if not path.exists():
            return cls()

        with open(path, 'r', encoding='utf-8') as f:
            config_dict = json.load(f)
            return cls.from_dict(config_dict)

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'ChatSystemConfig':
        """从字典创建配置实例"""
        valid_fields = cls.__dataclass_fields__.keys()
        filtered_dict = {
            k: v for k, v in config_dict.items()
            if k in valid_fields
        }
        return cls(**filtered_dict)

    def save_to_file(self, config_path: str) -> None:
        """保存配置到JSON文件"""
        path = Path(config_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, indent=2, ensure_ascii=False)