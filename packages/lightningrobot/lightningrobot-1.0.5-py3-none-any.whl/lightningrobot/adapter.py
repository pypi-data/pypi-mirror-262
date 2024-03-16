from abc import ABC, abstractmethod
from lightningrobot import log
class Adapter(ABC):
    @abstractmethod
    async def connect(self,list) -> None:
        """连接到聊天平台"""
        await log.info("正在连接适配器"+list)
        pass
    
    @abstractmethod
    async def send_message(self, event_type, id, message: str) -> None:
        """发送消息"""
        await log.info("发送消息：",message)
        pass

    @abstractmethod
    async def listen(self) -> str:
        """监听并获取新消息"""
        pass