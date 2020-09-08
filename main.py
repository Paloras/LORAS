# To make a discord bot you need to download discord.py with pip
#-*- coding: utf-8 -*-
import asyncio
import discord
from discord.ext import commands
import os
import inspect
import aiohttp
import re
import subprocess
import datetime
import time

token = "token"

bot = commands.Bot(command_prefix="팔")

for filename in os.listdir("Cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"Cogs.{filename[:-3]}")

# 봇 주인 확인 코드
def owner(ctx):
    return ctx.message.author.id == 384227121267998722

@bot.command(name="로드", help="로드을 합니다.")
@commands.check(owner)

async def load(ctx, extension):
    bot.load_extension(f"Cogs.{extension}")
    await ctx.send(f":white_check_mark: {extension}을(를) 로드했습니다!")

@bot.command(name="언로드", help="언로드을 합니다.")
@commands.check(owner)
async def unload(ctx, extension):
    bot.unload_extension(f"Cogs.{extension}")
    await ctx.send(f":white_check_mark: {extension}을(를) 언로드했습니다!")    

@bot.command(name="리로드", help="리로드을 합니다.")
@commands.check(owner)
async def reload(ctx, extension=None):
    if extension is None:
        for filename in os.listdir("Cogs"):
            if filename.endswith(".py"):
                bot.unload_extension(f"Cogs.{filename[:-3]}")
                bot.load_extension(f"Cogs.{filename[:-3]}")
        await ctx.send(":white_check_mark: 모든 명령어를 다시 불러왔습니다!")
    else:
        bot.unload_extension(f"Cogs.{extension}")
        bot.load_extension(f"Cogs.{extension}")
        await ctx.send(f":white_check_mark: {extension}를 다시 불러왔습니다!")

@bot.command(name="셧다운", aliases=['죽어'])
@commands.check(owner)
async def shutdown(ctx):
    await ctx.send("죽어가는 중...")
    await bot.logout()

@bot.command(name="업뎃", aliases=['업데이트'])
@commands.check(owner)
async def update(ctx):
    try:
        for filename in os.listdir("Cogs"):
            if filename.endswith(".py"):
                bot.load_extension(f"Cogs.{filename[:-3]}")
                await ctx.send(f"{filename[:-3]} 업데이트 완료!")
    except Exception as ex:
        await ctx.send(f"오류 - {ex}")


bot.remove_command("help")

bot.run(token)
