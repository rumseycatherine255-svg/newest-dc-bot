import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---------- WARN SYSTEM ----------
WARN_FILE = "warnings.json"

def load_warnings():
    try:
        with open(WARN_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_warnings(data):
    with open(WARN_FILE, "w") as f:
        json.dump(data, f, indent=4)

warnings = load_warnings()

# ---------- READY ----------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# ---------- KICK ----------
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"👢 Kicked {member}. Reason: {reason}")

# ---------- BAN ----------
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 Banned {member}. Reason: {reason}")

# ---------- UNBAN ----------
@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, name):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if user.name == name:
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user}")
            return

# ---------- MUTE ----------
@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)
    await ctx.send(f"🔇 Muted {member}")

# ---------- UNMUTE ----------
@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(role)
    await ctx.send(f"🔊 Unmuted {member}")

# ---------- WARN ----------
@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason="No reason"):
    user_id = str(member.id)

    if user_id not in warnings:
        warnings[user_id] = []

    warnings[user_id].append(reason)
    save_warnings(warnings)

    await ctx.send(f"⚠️ Warned {member}. Reason: {reason}")

# ---------- CHECK WARNINGS ----------
@bot.command()
async def warnings(ctx, member: discord.Member):
    user_id = str(member.id)
    user_warns = warnings.get(user_id, [])

    if not user_warns:
        await ctx.send(f"{member} has no warnings.")
    else:
        await ctx.send(f"{member} warnings:\n" + "\n".join(user_warns))

# ---------- SIMPLE ANTI-SPAM ----------
user_spam = {}

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    uid = message.author.id
    user_spam[uid] = user_spam.get(uid, 0) + 1

    if user_spam[uid] > 5:
        await message.channel.send(f"{message.author.mention} stop spamming!")
        user_spam[uid] = 0

    await bot.process_commands(message)

# ---------- RUN BOT ----------
bot.run(os.getenv("TOKEN"))
