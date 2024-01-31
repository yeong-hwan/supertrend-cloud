import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from private import private_key

import discord
from discord.ext import commands

CHANNEL_ID = private_key.DISCORD['CHANNEL_ID']
TOKEN = private_key.DISCORD['BOT_TOKEN']

class DiscordAlertBot(discord.Client):
    message = "Default Message"

    def set_message(self, message):
        self.message = message

    async def on_ready(self):
        channel = self.get_channel(int(CHANNEL_ID))
        await channel.send(self.message)
        await self.close()

    # async def on_message(self, message):
    #     # contents
    #     return

intents = discord.Intents.default()
intents.message_content = True

def send_message(message):
    discord_alert_bot = DiscordAlertBot(intents=intents)
    discord_alert_bot.set_message(message)
    discord_alert_bot.run(TOKEN)