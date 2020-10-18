import discord
from discord.ext import commands
import os
from asyncio import sleep
from discord.ext.tasks import loop
import keep_alive
from decouple import config

print(discord.__version__)

intents = discord.Intents.default()
intents.members = True

print("---> BOT is waking up\n")

bot = commands.Bot(command_prefix=[","],case_insensitive=True,intents=intents)
bot.remove_command('help')

def load_cogs():
    for file in os.listdir('./cogs'):
        if file.endswith('.py') and not file.startswith('_'):
            bot.load_extension(f'cogs.{file[:-3]}')


@bot.event
async def on_ready():
    print(f'---> Logged in as : {bot.user.name} , ID : {bot.user.id}')
    print(f'---> Total Servers : {len(bot.guilds)}\n')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Events"))
    load_cogs()
    print('\n---> BOT is awake\n')

keep_alive.keep_alive()
bot.run(config("BOT_TOKEN"))