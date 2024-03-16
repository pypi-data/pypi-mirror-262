from lightningrobot.adapter import Adapter
from lightningrobot import log

class ConsoleAdapter(Adapter):
    async def connect(self,list) -> None:
        await log.info("已加载-ConsoleAdapter")
        pass

    async def send_message(self, event_type, id, message: str) -> None:
        if event_type == "group":
            await log.info("[群聊]Bot机器人："+message)
        elif event_type == "private":
            await log.info("[私聊]Bot机器人："+message)

    async def listen(self) -> str:
        user_input = input("User用户：")
        event_type_temp = input("请选择场景：1.群聊 2.私聊\n")
        if event_type_temp == "1":
            event_type = "group"
        elif event_type_temp == "2":
            event_type = "private"
        else:
            await log.error("输入错误")
        id = 1
        return user_input, event_type, id