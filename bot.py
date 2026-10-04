# +++ Modified By [telegram username: @Codeflix_Bots]
import asyncio
import sys
from datetime import datetime
from pyrogram import Client
from pyrogram.enums import ParseMode
import pyrogram.utils

# Channel ID limit patch (must be executed before importing modules that use it)
pyrogram.utils.MIN_CHANNEL_ID = -1009147483647

from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, PORT, OWNER_ID
from plugins import web_server
from aiohttp import web

name = """
Links Sharing Started
"""

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=int(APP_ID),
            plugins={"root": "plugins"},
            workers=int(TG_BOT_WORKERS) if TG_BOT_WORKERS else 8,
            bot_token=TG_BOT_TOKEN,
        )
        self.LOGGER = LOGGER

    async def start(self, *args, **kwargs):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        # Ensure OWNER_ID is an integer
        try:
            owner_chat_id = int(OWNER_ID)
            await self.send_message(
                chat_id=owner_chat_id,
                text="<b><blockquote>🤖 Bot Restarted ♻️</blockquote></b>",
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            self.LOGGER(__name__).warning(f"Failed to notify owner ({OWNER_ID}) of bot start: {e}")

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info("Bot Running..!\n\nCreated by \nhttps://t.me/ProObito")
        self.LOGGER(__name__).info(f"{name}")
        self.username = usr_bot_me.username

        # Web-response (Fix for Railway Port & Healthcheck)
        try:
            app = web.AppRunner(await web_server())
            await app.setup()
            bind_address = "0.0.0.0"
            server_port = int(PORT) if PORT else 8080
            await web.TCPSite(app, bind_address, server_port).start()
            self.LOGGER(__name__).info(f"Web server started on {bind_address}:{server_port}")
        except Exception as e:
            self.LOGGER(__name__).error(f"Failed to start web server: {e}")

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")

# Global cancel flag for broadcast
is_canceled = False
cancel_lock = asyncio.Lock()

if __name__ == "__main__":
    Bot().run()
