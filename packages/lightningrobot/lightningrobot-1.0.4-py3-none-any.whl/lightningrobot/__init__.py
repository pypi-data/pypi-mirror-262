import asyncio
from lightningrobot.plugin import Plugin
from lightningrobot.adapter import Adapter
from lightningrobot import log

class Main:
    def __init__(self, adapter: Adapter, plugins: list[Plugin]):
        self.adapter = adapter
        self.plugins = plugins
        # 添加一个事件循环控制变量
        self.should_stop = False

    async def stop(self):
        # 设置退出标志为True
        self.should_stop = True

    async def start(self):
        # 连接适配器
        try:
            await self.adapter.connect()
        except Exception as e:
            log.error(f"连接适配器时发生错误: {e}")
            return

        while not self.should_stop:
            try:
                # 异步等待并获取消息
                message, event_type, id = await self.adapter.listen()
                # 并发处理消息
                tasks = [asyncio.create_task(plugin.command(message, event_type, id)) for plugin in self.plugins]
                await asyncio.gather(*tasks)
            except Exception as e:
                # 添加对消息处理过程中的异常捕获
                log.error(f"处理消息时发生错误: {e}")

        # 关闭适配器连接
        await self.adapter.stop()