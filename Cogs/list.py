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

class listt(commands.Cog): #2

    def __init__(self, bot): #3
        self.bot = bot #4
            
    @commands.command(name="배치", aliases=['배열', '나열'], help="입력한 수까지 출력합니다.")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def listedadadad(self, ctx, amount:int, dm=None):
        if"*도배가능" in ctx.channel.topic:
            lisst = ""
            listd = ""
            listt = ""
            list1 = ""
            list2 = ""
            list3 = ""
            if amount > 0 and amount < 10:
                for x in range(amount):
                    lisst = lisst + '{0:01d}'.format(x+1)+'\n'
                await ctx.send(lisst)
            elif amount >= 10 and amount < 100:
                for x in range(amount):
                    lisst = lisst + '{0:02d}'.format(x+1)+'\n'
                await ctx.send(lisst)
            elif amount >= 100 and amount <= 400:
                for x in range(amount):
                    lisst = lisst + '{0:03d}'.format(x+1)+'\n'
                await ctx.send(f'{lisst}')
                await ctx.send(f'{ctx.author.mention}님이 시켰어요!!')
            elif amount > 400 and amount < 800:
                for x in range(400):
                    lisst = lisst + '{0:03d}'.format(x+1)+'\n'
                for y in range(amount%400):
                    listd = listd + '{0:03d}'.format(y+401)+'\n'
                await ctx.send(lisst)
                await ctx.send(listd)
                await ctx.send(f'{ctx.author.mention}님이 시켰어요!!')
            elif amount >= 800 and amount < 1000:
                for x in range(400):
                    lisst = lisst + '{0:03d}'.format(x+1)+'\n'
                for y in range(400):
                    listd = listd + '{0:03d}'.format(y+401)+'\n'
                for z in range(amount%800):
                    listt = listt + '{0:03d}'.format(z+801)+'\n'
                await ctx.send(lisst)
                await ctx.send(listd)
                await ctx.send(listt)
                await ctx.send(f'{ctx.author.mention}님이 시켰어요!!')
            elif amount >= 1000 and amount < 1200:
                for x in range(400):
                    lisst = lisst + '{0:04d}'.format(x+1)+'\n'
                for y in range(400):
                    listd = listd + '{0:04d}'.format(y+401)+'\n'
                for z in range(amount%800):
                    listt = listt + '{0:04d}'.format(z+801)+'\n'
                await ctx.send(lisst)
                await ctx.send(listd)
                await ctx.send(listt)
                await ctx.send(f'{ctx.author.mention}님이 시켰어요!!')
            elif amount >= 1200 and amount < 1600:
                for x in range(400):
                    lisst = lisst + '{0:04d}'.format(x+1)+'\n'
                for y in range(400):
                    listd = listd + '{0:04d}'.format(y+401)+'\n'
                for z in range(400):
                    listt = listt + '{0:04d}'.format(z+801)+'\n'
                for z in range(amount%1200):
                    list1 = list1 + '{0:04d}'.format(z+1201)+'\n'
                await ctx.send(lisst)
                await ctx.send(listd)
                await ctx.send(listt)
                await ctx.send(list1)
                await ctx.send(f'{ctx.author.mention}님이 시켰어요!!')
            elif amount >= 1600 and amount < 2000:
                for x in range(400):
                    lisst = lisst + '{0:04d}'.format(x+1)+'\n'
                for y in range(400):
                    listd = listd + '{0:04d}'.format(y+401)+'\n'
                for z in range(400):
                    listt = listt + '{0:04d}'.format(z+801)+'\n'
                for z in range(400):
                    list1 = list1 + '{0:04d}'.format(z+1201)+'\n'
                for z in range(amount%1600):
                    list2 = list2 + '{0:04d}'.format(z+1601)+'\n'
                await ctx.send(lisst)
                await ctx.send(listd)
                await ctx.send(listt)
                await ctx.send(list1)
                await ctx.send(list2)
                await ctx.send(f'{ctx.author.mention}님이 시켰어요!!')
            elif amount >= 2000 and amount < 2400:
                for x in range(400):
                    lisst = lisst + '{0:04d}'.format(x+1)+'\n'
                for y in range(400):
                    listd = listd + '{0:04d}'.format(y+401)+'\n'
                for z in range(400):
                    listt = listt + '{0:04d}'.format(z+801)+'\n'
                for z in range(400):
                    list1 = list1 + '{0:04d}'.format(z+1201)+'\n'
                for z in range(400):
                    list2 = list2 + '{0:04d}'.format(z+1601)+'\n'
                for z in range(amount%2000):
                    list3 = list3 + '{0:04d}'.format(z+2001)+'\n'
                await ctx.send(lisst)
                await ctx.send(listd)
                await ctx.send(listt)
                await ctx.send(list1)
                await ctx.send(list2)
                await ctx.send(list3)
                await ctx.send(f'{ctx.author.mention}님이 시켰어요!!')
            elif amount >= 2400:
                await ctx.channel.send("도배... 하실려고요?")
            else:
                await ctx.send("1이상의 **숫자**만 입력해주세요")
        else:
            await ctx.send("해당 명령어 이용을 할려면 명령어를 쓸 채널 주제에 *도배가능을 넣어주세요")
    @listedadadad.error
    async def listedadadad_error(self, ctx, error):
        await ctx.send("혹시 채널에 *도배가능이 없는지 확인해주세요!\n이기능은 *도배가능이 없으면 오류가 납니다.")
        if isinstance(error, commands.BadArgument):
            await ctx.send("**수**를 넣어주세요.")
        elif isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:20s:752150489583452211>')


def setup(bot): #5
    bot.add_cog(listt(bot))
