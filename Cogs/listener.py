# To make a discord bot you need to download discord.py with pip
#-*- coding: utf-8 -*-

from discord.utils import get
import youtube_dl
from bs4 import BeautifulSoup
import urllib
import requests
from urllib.request import urlopen, Request
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.parse import quote
from urllib import parse
import json
import aiohttp
import time
import discord
from discord.ext import commands
import random
import asyncio
from captcha.image import ImageCaptcha
import re
import ast
import datetime



class Events(commands.Cog):
    
    def __init__(self, bot):
        """Initialisation bot"""
        self.bot = bot
    
    def is_owner(self, ctx):
        return ctx.message.author.id == 384227121267998722

    @commands.Cog.listener()
    async def on_ready(self):
        print("다음으로 로그인합니다 : ")
        print(self.bot.user.name)
        print(self.bot.user.id)
        print("==========")
        print("New log in as {0.user}".format(self.bot))
        while True:
            user = len(self.bot.users)
            server = len(self.bot.guilds)
            messages = ["팔도움을 요구", "건의는 !  PLRS#3588에게 해주세요!", str(user) + "명의 유저들과 함께 ", str(server) + "개의 서버에 참가되어있습니다.", "봇이 오프라인이라면 점검중또는 봇을 끈겁니다."]
            for m in range(5):
                await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=messages[m]))
                await asyncio.sleep(3)
    
    @commands.Cog.listener()
    async def on_message(self, message):    
        if message.author.bot:
            return None
        
        if "죽음" in message.content or "사망" in message.content:
            await message.add_reaction('❎')

        # if message.content.startswith("팔"):
        #     cha = self.bot.get_channel(745091205641011290)
        #     embed = discord.Embed(title= '말한 사람 이름 : ' + message.author.name + ", id : " + str(message.author.id), description= '말한 내용 : ' + message.content+"\n"+'말한 채널의 id : ' + str(message.channel.id),colour=discord.Colour.green())#+"\n"
        #     embed.set_footer(text=f"{message.author} 시간: "+str(datetime.datetime.now()), icon_url=message.author.avatar_url)
        #     await cha.send(embed=embed)

        if message.content.startswith("팔캡차") or message.content.startswith("팔캡챠"):
            Image_captcha = ImageCaptcha()
            msg = ""
            a = ""
            for i in range(6):
                a += str(random.randint(0, 9))

            name = "Captcha.png"
            Image_captcha.write(a, name)

            await message.channel.send(file=discord.File(name))

            def check(msg):
                return msg.author == message.author and msg.channel == message.channel

            try:
                msg = await self.bot.wait_for("message", timeout=20, check=check)
            except:
                await message.channel.send("**시간 초과입니다.**")
                return

            if msg.content == a:
                await message.channel.send("**정답입니다.**")
            else:
                await message.channel.send("**오답입니다.**")

        if message.content.startswith("팔공지"):
            if message.author.id == 384227121267998722:
                if str(message.content[4:]) == None:
                    await message.channel.send("팔공지 내용")
                msg = message.content[4:]
                oksv = 0
                embed = discord.Embed(  
                    title = "로라스 공지",
                    description = msg + f"\n\n이 채널에 공지가 오기 싫다면 봇-공지채널을 만들어주세요!\n[서포트 서버](https://discord.gg/SVDm3hg)",
                    colour = discord.Colour.blue(),
                    timestamp = message.created_at
                ).set_footer(icon_url=message.author.avatar_url, text=f'{message.author}') .set_thumbnail(url=self.bot.user.avatar_url_as(format=None, static_format="png", size=1024))
                for i in self.bot.guilds:
                    arr = [0]
                    alla = False
                    flag = True
                    z = 0
                    for j in i.channels:
                        arr.append(j.id)
                        z+=1
                        if "봇-공지" in j.name or "봇_공지" in j.name or "봇공지" in j.name or "bot_announcement" in j.name or "봇ㆍ공지" in j.name or "🧪『팔로라스』" in j.name or "🧪｜로라스" in j.name:
                            if str(j.type)=='text':
                                try:
                                    oksv += 1
                                    await j.send(embed=embed)
                                    alla = True
                                except:
                                    pass
                                break
                    if alla==False:
                        try:
                            chan=i.channels[1]
                        except:
                            pass
                        if str(chan.type)=='text':
                            try:
                                oksv += 1
                                await chan.send(embed=embed)
                            except:
                                pass
                await message.channel.send(f"**`📢 공지 발신 완료 📢`**\n\n{len(self.bot.guilds)}개의 서버 중 {oksv}개의 서버에 발신 완료, {len(self.bot.guilds) - oksv}개의 서버에 발신 실패")
            else:
                await message.channel.send('이 명령어을 쓸수있는 사람은 아직 PLRS님 뿐입니다.')
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        cha = self.bot.get_channel(744483624534933534)  
        if isinstance(error, commands.MissingPermissions):
            await ctx.message.add_reaction('🚫')
            await ctx.send (f"당신이 필요한 권한을 가지고 있지 않습니다.\n필요한 권한: `{', '.join(error.missing_perms)}`", delete_after=5.0)
        elif isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('⏱️')
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send("{}님, 당신은 이 명령을 실행하실 권한이 없습니다.".format(ctx.message.author), delete_after=5.0)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"누락된 필수 항목이 있습니다. **{error.param.name}** 이것을 안 넣으신거같군요.", delete_after=3.0)
        elif isinstance(error, commands.CommandNotFound):
            return
        else:
            embed = discord.Embed(title="오류!!", description="오류가 발생했습니다.", color=0xFF0000)
            embed.add_field(name="상세", value=f"```{error}```")
            # embed.set_footer(text=f"{ctx.author}시간 : {str(ctx.message.created_at())}", icon_url=ctx.author.avatar_url)
            await cha.send(embed=embed)
            await ctx.send("오류가 발생하여 개발자한테 전송하였습니다.", delete_after=5.0)
        
        # print('말한 사람 이름 : ' + message.author.name + ", id : " + str(message.author.id))timestamp = message.created_at
        # print('말한 내용 : ' + message.content)
        # print('말한 서버의 이름 : ' + message.guild.name + ", id : " + str(message.guild.id))
        # print('말한 채널의 이름 : ' + message.channel.name + ", id : " + str(message.channel.id))

        # if "씨발" in message.content or "새끼" in message.content or "썅" in message.content or "놈" in message.content or "년" in message.content:
        #     if "*욕설금지" in message.chennel.topic:
        #         await message.chennel.purge(limit= 1)
        #     else:
        #         pass


def setup(bot):
    bot.add_cog(Events(bot))    
