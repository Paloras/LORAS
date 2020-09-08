# To make a discord bot you need to download discord.py with pip
#-*- coding: utf-8 -*-
import asyncio
import discord
from discord.ext import commands
from discord.utils import get
from bs4 import BeautifulSoup
import urllib
import requests
from urllib.request import urlopen, Request
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.parse import quote
from urllib import parse
import json



class overwatch(commands.Cog, name="전적"): 

    def __init__(self, bot): 
        self.bot = bot 
 
    @commands.command(name="오버워치전적", aliases=['오버워치'], help="팔오버워치")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def overwatch(self, ctx, name, tag):
        url= f"http://owapi.io/profile/pc/asia/{name}-{tag}"
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        output = json.loads(webpage)
        username = output['username']
        level = output['level']
        competitive = output['competitive']
        tanker = output['competitive']['tank']['rank']
        dealer = output['competitive']['tank']['rank']
        healer = output['competitive']['tank']['rank']
        playtime = output['playtime']
        portrait = output['portrait']
        quickplaytime = output['playtime']['quickplay']
        competitivetime = output['playtime']['competitive']
        won = output['games']['quickplay']['won']
        played = output['games']['quickplay']['played']
        global TankRank
        if 0 <= tanker <= 1499:
            TankRank = "브론즈"
        elif 1500 <= tanker <= 1999:
            TankRank = "실버"
        elif 2000 <= tanker <= 2499:
            TankRank = "골드"
        elif 2500 <= tanker <= 2999:
            TankRank = "플래티넘"
        elif 3000 <= tanker <= 3499:
            TankRank = "다이아몬드"
        elif 3500 <= tanker <= 3999:
            TankRank = "마스터"
        elif 4000 <= tanker <= 5000:
            TankRank = "그랜드마스터"
        elif 5000 <= tanker:
            TankRank = "그랜드마스터 이상"
        global DealRank
        if 0 <= dealer <= 1499:
            DealRank = "브론즈"
        elif 1500 <= dealer <= 1999:
            DealRank = "실버"
        elif 2000 <= dealer <= 2499:
            DealRank = "골드"
        elif 2500 <= dealer <= 2999:
            DealRank = "플래티넘"
        elif 3000 <= dealer <= 3499:
            DealRank = "다이아몬드"
        elif 3500 <= dealer <= 3999:
            DealRank = "마스터"
        elif 4000 <= dealer <= 5000:
            DealRank = "그랜드마스터"
        elif 5000 <= dealer:
            DealRank = "그랜드마스터 이상"
        global HealRank
        if 0 <= tanker <= 1499:
            HealRank = "브론즈"
        elif 1500 <= healer <= 1999:
            HealRank = "실버"
        elif 2000 <= healer <= 2499:
            HealRank = "골드"
        elif 2500 <= healer <= 2999:
            HealRank = "플래티넘"
        elif 3000 <= healer <= 3499:
            HealRank = "다이아몬드"
        elif 3500 <= healer <= 3999:
            HealRank = "마스터"
        elif 4000 <= healer <= 5000:
            HealRank = "그랜드마스터"
        elif 5000 <= healer:
            HealRank = "그랜드마스터 이상"
        embed = discord.Embed(title=f'{name}#{tag} 님의 정보', colour=discord.Color.red())
        embed.set_author(name=f'{ctx.author.name}', icon_url=f'{portrait}')
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name="레벨", value = f'{len(ctx.guild.emojis)}개', inline=False)
        embed.add_field(name="경쟁전", value = f"탱커 : {tanker} : {TankRank}\n딜러 : {dealer} : {DealRank}\n힐러 : {healer} : {HealRank}", inline=False)
        embed.add_field(name="플레이", value = f"{playtime}", inline=False)
        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
    @overwatch.error
    async def overwatch_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

def setup(bot):
    bot.add_cog(overwatch(bot))