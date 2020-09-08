# To make a discord bot you need to download discord.py with pip
#-*- coding: utf-8 -*-
import asyncio
import discord
from discord.ext import commands
import random
from discord.utils import get
import youtube_dl
from bs4 import BeautifulSoup
import urllib
import datetime
from captcha.image import ImageCaptcha
import time

class timer(commands.Cog): #2

    def __init__(self, bot): #3
        self.bot = bot #4
            
    @commands.command(name="타이머", help="타이머기능입니다.")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def timer(self, ctx, set_time):
        set_time=int(set_time)
        msg=await ctx.send(embed=discord.Embed())
        for i in range(set_time):
            set_time-=1
            embed=discord.Embed(title=f"{set_time}초 남았어요.")
            await msg.edit(embed=embed)
            await asyncio.sleep(1)
        embed=discord.Embed(title="땡!")
        await msg.edit(embed=embed, delete_after=5)
        await ctx.send(f"{ctx.author.mention}님 타이머가 끝났어요")
    @timer.error
    async def timer_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(name="타이머2", help="타이머기능입니다.")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def ㅇㅁㅇ(self, ctx, hour:int, minut:int, second:int):
        set_time = 3600*hour + 60*minut + second
        msg=await ctx.send(embed=discord.Embed())
        for i in range(set_time):
            set_time-=1
            if set_time >= 3600:
                hour1 = set_time//3600
                minu= (set_time//60)-60
                sec = set_time%60
                embed=discord.Embed(title=f"{hour1}시간 {minu}분 {sec}초 남았어요.")
                await msg.edit(embed=embed)
            elif set_time >= 60 and set_time < 3600:
                minu= set_time//60
                sec = set_time%60
                embed=discord.Embed(title=f"{minu}분 {sec}초 남았어요.")
                await msg.edit(embed=embed)
            elif set_time < 60:
                embed=discord.Embed(title=f"{set_time}초 남았어요.")
                await msg.edit(embed=embed)
            await asyncio.sleep(1)
        embed=discord.Embed(title="땡!")
        await msg.edit(embed=embed, delete_after=5)
        await ctx.send(f"{ctx.author.mention}님 타이머가 끝났어요")
    @ㅇㅁㅇ.error
    async def ㅇㅁㅇ_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

def setup(bot): #5
    bot.add_cog(timer(bot))