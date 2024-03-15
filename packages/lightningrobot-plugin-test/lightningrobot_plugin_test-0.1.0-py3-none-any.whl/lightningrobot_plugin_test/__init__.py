from lightningrobot.plugin import Plugin

class main(Plugin):
    def __init__(self, adapter):
        self.adapter = adapter  # 存储适配器引用

    async def command(self, message,event_type,id):
         if message == "test":
            await self.adapter.send_message(event_type,id,"你好，很高兴见到你！")