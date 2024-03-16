import re
from lightningrobot.plugin import Plugin

class Main(Plugin):
    def __init__(self, adapter):
        self.adapter = adapter  # 存储适配器引用

    async def command(self, message,event_type,id):
        if re.search(r"^(#|/)?(echo|复读)$", message):
            echo(message,event_type,id)
        else:
            pass

async def echo(self,message,event_type,id):
    text = re.sub(r"^(#|/)?(echo|复读)$","",message)
    await self.adapter.send_message(event_type,id,text)
