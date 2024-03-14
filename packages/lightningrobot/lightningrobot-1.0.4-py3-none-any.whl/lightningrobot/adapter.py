from abc import ABC, abstractmethod
from lightningrobot import log
class Adapter(ABC):
    @abstractmethod
    async def connect(self) -> None:
        """连接到聊天平台"""
        log.info("正在连接聊天平台...")
        pass
    
    @abstractmethod
    async def send_message(self, event_type, id, message: str) -> None:
        """发送消息"""
        log.info("发送消息：",message)
        pass

    @abstractmethod
    async def listen(self) -> str:
        """监听并获取新消息"""
        pass