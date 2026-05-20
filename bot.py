import discord
from discord.ext import commands
import aiohttp
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True

class Comet(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.session = None

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        await self.tree.sync()

    async def close(self):
        if self.session:
            await self.session.close()
        await super().close()

bot = Comet()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel:
        await channel.send(f"👋 Welcome {member.mention}!")

@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong 🏓")

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        raise ValueError("Missing DISCORD_TOKEN")
    bot.run(DISCORD_TOKEN)
