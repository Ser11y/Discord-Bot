from INFO import TOKEN  # Импортируем значение TOKEN из файла INFO.py
from INFO import PREFIX  # Импортируем значение PREFIX из файла INFO.py
from NAMES import c_names, c_descs
import random
import aiohttp
import discord
import asyncio
from discord.ext import commands

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
    await bot.change_presence(activity=discord.Game(
        name=f'Prefix: "{bot.command_prefix}"'))


# EVENTS END


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
    emb1 = discord.Embed(
        title='Помощь',
        description=
        f'В настоящий момент, prefix - "{bot.command_prefix}". Список возможных команд:',
        color=0x00FF00)
    emb1.add_field(name=c_names[1],
                   value=c_descs[1],
                   inline=False)
    emb1.add_field(name=c_names[2],
                   value=c_descs[2],
                   inline=False)
    emb1.add_field(name=c_names[3],
                   value=c_descs[3],
                   inline=False)
    emb1.add_field(name=c_names[4],
                   value=c_descs[4],
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
    await asyncio.sleep(3)
    await ctx.channel.purge(limit=50, check=is_me)


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
    embed.add_field(name="Присоединился:", value=joined, inline=False)
    embed.add_field(name="Создан:", value=created, inline=False)
    embed.add_field(name="Роли:", value=", ".join(roles), inline=False)

    await ctx.send(embed=embed)


@bot.command()
async def meme(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.reddit.com/r/memes.json') as r:
            if r.status == 400:
                data = await r.json()
                post = random.choice(data['data']['children'])['data']
                embed = discord.Embed(title=post['title'],
                                      description='',
                                      color=0x00FF00)
                embed.set_image(url=post['url'])
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
        embed = discord.Embed(title="Ошибка!", color=0xFF0000)
        embed.add_field(name="Код ошибки:", value=str(error))

        await ctx.send(embed=embed)


# ERRORS END

bot.run(TOKEN)
