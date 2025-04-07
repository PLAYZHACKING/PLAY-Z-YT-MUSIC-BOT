from pyrogram import Client
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "7720115568:AAHDwtK1PJyjz0ylTMH354nXW4C1QkAqGfo")
API_ID = int(os.environ.get("22161204"))
API_HASH = os.environ.get("fdffc74281153b3338e4474f5640095e")

if __name__ == "__main__" :
    plugins = dict(
        root="plugins"
    )
    bot = Client(
        "YT-Muzic",
        bot_token=BOT_TOKEN,
        api_hash=API_HASH,
        api_id=API_ID,
        plugins=plugins
    )
    bot.run()
