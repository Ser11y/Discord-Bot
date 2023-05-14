from INFO import TOKEN # Импортируем значение TOKEN из файла INFO.py
from INFO import PREFIX # Импортируем значение PREFIX из файла INFO.py
import discord
import time
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True
bot = discord.ext.commands.Bot(intents=intents,
                               command_prefix=PREFIX,
                               help_command=None)  # Установка Prefix.


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=f'Prefix: "{bot.command_prefix}"'))
# Показывает свой Prefix с помощью активности.


# ARRAYS

commands_names = ["0",
                  "prefix",
                  "help",
                  "clear"]
commands_descriptions = ["0",
                         "Изменить Prefix для команд.",
                         "Выводит названия и описания всех команд.",
                         "Удаляет введённое кол-во сообщений."]

# ARRAYS END

@bot.command()
async def prefix(ctx, new_prefix: str):
    bot.command_prefix = new_prefix
    emb1 = discord.Embed(title='Выполнено',
                         description=f'Prefix был изменён на "{new_prefix}".')
    await ctx.send(embed=emb1)


@bot.command()
async def help(ctx):
    emb1 = discord.Embed(title='Помощь',
                         description=f'В настоящий момент, prefix - "{bot.command_prefix}". Список команд, которые можно выполнить им:')
    emb1.add_field(name=commands_names[1],
                   value=commands_descriptions[1])
    emb1.add_field(name=commands_names[2],
                   value=commands_descriptions[2])
    emb1.add_field(name=commands_names[3],
                   value=commands_descriptions[3])
    await ctx.send(embed=emb1)


def is_me(m):
    return m.author == bot.user


@bot.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    emb1 = discord.Embed(title='Выполнено',
                         description=f'Было удалено {amount} сообщений.')
    await ctx.send(embed=emb1)
    time.sleep(3)
    await ctx.channel.purge(limit=50,
                            check=is_me)


bot.run(TOKEN)
