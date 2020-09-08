import discord
import asyncio
import os
from discord.ext import commands
import urllib
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote
import re
import warnings
import requests
import unicodedata
import json
from googletrans import Translator


class Translate(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['번역'])
    async def _trans(self, ctx, dest, *, translates):
        translator = Translator()
        output = translator.translate(translates, dest)
        embed = discord.Embed(title="번역 결과", description=" ", color=0x00ff56)
        embed.add_field(name="**번역**", value=output.text, inline=False)
        embed.add_field(name="**입력된 언어**", value=output.src, inline=False)
        embed.add_field(name="**발음**", value=output.pronunciation, inline=False)
        await ctx.send(embed = embed)

    @commands.command(name= "번한",aliases=['한국'])
    async def ko(self, ctx, *, translates):
        translator = Translator()
        output = translator.translate(translates, dest="ko")
        embed = discord.Embed(title="번역 결과", description=" ", color=0x00ff56)
        embed.add_field(name="**번역**", value=output.text, inline=False)
        embed.add_field(name="**입력된 언어**", value=output.src, inline=False)
        embed.add_field(name="**발음**", value=output.pronunciation, inline=False)
        await ctx.send(embed = embed,tts=True)

    @commands.command(name= "번영",aliases=['영어'])
    async def en(self, ctx, *, translates):
        translator = Translator()
        output = translator.translate(translates, dest="en")
        embed = discord.Embed(title="번역 결과", description=" ", color=0x00ff56)
        embed.add_field(name="**번역**", value=output.text, inline=False)
        embed.add_field(name="**입력된 언어**", value=output.src, inline=False)
        embed.add_field(name="**발음**", value=output.pronunciation, inline=False)
        await ctx.send(embed = embed)

    @commands.command(name="번일",aliases=['일본'])
    async def jp(self, ctx, *, translates):
        translator = Translator()
        output = translator.translate(translates, dest="ja")
        embed = discord.Embed(title="번역 결과", description=" ", color=0x00ff56)
        embed.add_field(name="**번역**", value=output.text, inline=False)
        embed.add_field(name="**입력된 언어**", value=output.src, inline=False)
        embed.add_field(name="**발음**", value=output.pronunciation, inline=False)
        await ctx.send(embed = embed)

    @commands.command(name="번간",aliases=['간체'])
    async def jp(self, ctx, *, translates):
        translator = Translator()
        output = translator.translate(translates, dest="zh-CN")
        embed = discord.Embed(title="번역 결과", description=" ", color=0x00ff56)
        embed.add_field(name="**번역**", value=output.text, inline=False)
        embed.add_field(name="**입력된 언어**", value=output.src, inline=False)
        embed.add_field(name="**발음**", value=output.pronunciation, inline=False)
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Translate(bot))
