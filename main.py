from telegram.telegram import GptBot
# from db.init_db import init_db
import logging

logging.basicConfig()
logging.root.setLevel(logging.INFO)
logging.basicConfig(level=logging.WARNING)
handle = "chatgpt"
logger1 = logging.getLogger(handle)

if __name__ == '__main__':
    # init_db()
    client = GptBot()
    client.bot_polling()
