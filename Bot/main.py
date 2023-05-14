from INFO import TOKEN  # Импортируем значение TOKEN из файла INFO.py
from INFO import PREFIX  # Импортируем значение PREFIX из файла INFO.py
import discord
import time
from discord.ext import commands
from discord import app_commands


# INITIALIZATION


intents = discord.Intents.default()
intents.message_content = True
bot = discord.ext.commands.Bot(intents=intents,
                               command_prefix=PREFIX,
                               help_command=None)  # Установка Prefix.


# INITIALIZATION END


# EVENTS


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=f'Prefix: "{bot.command_prefix}"'))


# EVENTS END


# ARRAYS

commands_names = ["0",
                  "prefix",
                  "help",
                  "clear",
                  "user"]
commands_descriptions = ["0",
                         "Изменить Prefix для команд.",
                         "Выводит названия и описания всех команд.",
                         "Удаляет введённое кол-во сообщений.",
                         "Выводит информацию об пользователе."]


# ARRAYS END


# COMMANDS


@bot.command()
async def prefix(ctx, new_prefix: str):
    bot.command_prefix = new_prefix
    emb1 = discord.Embed(title='Выполнено',
                         description=f'Prefix был изменён на "{new_prefix}".',
                         color=0x00FF00)
    await ctx.send(embed=emb1)


@bot.command()
async def help(ctx):
    emb1 = discord.Embed(title='Помощь',
                         description=f'В настоящий момент, prefix - "{bot.command_prefix}". Список возможных команд:',
                         color=0x00FF00)
    emb1.add_field(name=commands_names[1],
                   value=commands_descriptions[1],
                   inline=False)
    emb1.add_field(name=commands_names[2],
                   value=commands_descriptions[2],
                   inline=False)
    emb1.add_field(name=commands_names[3],
                   value=commands_descriptions[3],
                   inline=False)
    emb1.add_field(name=commands_names[4],
                   value=commands_descriptions[4],
                   inline=False)
    await ctx.send(embed=emb1)


def is_me(m):
    return m.author == bot.user


@bot.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    emb1 = discord.Embed(title='Выполнено',
                         description=f'Было удалено {amount} сообщений.',
                         color=0x00FF00)
    await ctx.send(embed=emb1)
    time.sleep(3)
    await ctx.channel.purge(limit=50,
                            check=is_me)


@bot.command()
async def user(ctx, member: discord.Member):
    joined = member.joined_at.strftime("%d.%m.%Y %H:%M:%S")
    created = member.created_at.strftime("%d.%m.%Y %H:%M:%S")
    roles = [role.mention for role in member.roles[1:]]

    embed = discord.Embed(title=f"Информация о пользователе {member.name}",
                          color=0x00FF00)
    embed.set_thumbnail(url=member.avatar)
    embed.add_field(name="Имя:",
                    value=f'{member.name}#{member.discriminator}',
                    inline=False)
    embed.add_field(name="Присоединился:",
                    value=joined,
                    inline=False)
    embed.add_field(name="Создан:",
                    value=created,
                    inline=False)
    embed.add_field(name="Роли:",
                    value=", ".join(roles),
                    inline=False)

    await ctx.send(embed=embed)


# COMMANDS END


# ERRORS


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.CommandError):
        await ctx.channel.purge(limit=1)


@user.error
async def user_error(ctx, error):
    if isinstance(error, commands.CommandError):
        embed = discord.Embed(title="Ошибка!",
                              color=0xFF0000)
        embed.add_field(name="Код ошибки:", value=str(error))

        await ctx.send(embed=embed)


# ERRORS END

bot.run(TOKEN)
