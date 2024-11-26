import logging
import config
import bot_event

# 設置日誌
FORMAT = '%(asctime)s %(filename)s %(levelname)s:%(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

token = config.DISCORD_BOT_TOKEN

if __name__ == "__main__":
    bot_event.bot.run(token)
