from TOKEN import TOKEN
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = discord.ext.commands.Bot(intents=intents, command_prefix="!")


@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")


print(TOKEN)

bot.run(TOKEN)
