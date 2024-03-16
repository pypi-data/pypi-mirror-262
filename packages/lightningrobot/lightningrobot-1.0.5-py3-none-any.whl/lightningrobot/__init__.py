# 导入所需模块，包括Plugin插件基类和Adapter适配器类
from lightningrobot.plugin import Plugin
from lightningrobot.adapter import Adapter

class Main:
    # 初始化方法，传入一个适配器实例和一个插件列表
    def __init__(self, adapter: list[Adapter], plugins: list[Plugin]):
        self.adapter = adapter
        self.plugins = plugins

    # 异步启动方法
    async def start(self):
        # 首先连接适配器以开始监听消息
        await self.adapter.connect(list[Adapter])

        # 进入无限循环，持续监听并处理消息
        while True:
            # 使用Adapter的listen方法异步等待并获取消息
            message,event_type,id = await self.adapter.listen()
            # 判断消息是否有对应指令
            for plugin in self.plugins:
                await plugin.command(message,event_type,id)