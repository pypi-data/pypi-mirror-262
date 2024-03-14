from zbig.ztime import cn_now
from .define import bot, CHAT_ID


def send_message(message: str):
    bot.send_message(chat_id=CHAT_ID, text=f"{cn_now()} {message}")


if __name__ == "__main__":
    send_message('zbig send_message test')
