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

    


    # @commands.command(aliases=['한영'])
    # @commands.cooldown(1, 2, commands.BucketType.user)   
    # async def KoEn(self, ctx):
    #     reply = ctx.message.content.split(" ")
    #     if len(reply) > 1:
    #         for i in range(2, len(reply)):
    #             reply[1] = reply[1] + " " + reply[i]

    #     baseurl = "https://openapi.naver.com/v1/papago/n2mt"
    #     try:
    #         if len(reply) == 1:
    #             await ctx.trigger_typing()
    #             embed = discord.Embed(title="에러", description="단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.", color=0xffffff)
     
    #             await ctx.send(embed = embed)
    #         else:
    #             await ctx.trigger_typing()
    #             dataParmas = "source=ko&target=en&text=" + reply[1]
    #             # 요청 인스턴스 만들기
    #             request = Request(baseurl)
    #             # 패킷에 헤더 추가
    #             request.add_header("X-Naver-Client-Id", 'lTDnImjndhbi1G25FX2Y')
    #             request.add_header("X-Naver-Client-Secret", 'Kjm8em9ZQH')
    #             response = urlopen(request, data=dataParmas.encode("utf-8"))
    #             responsedCode = response.getcode()
    #             if (responsedCode == 200):
    #                 response_body = response.read()
    #                 # response_body -> 바이트 문자열 : UTF-8로 디코딩
    #                 api_callResult = response_body.decode('utf-8')
    #                 # 자스 데이터는 문자열 유형으로 나옴, 사전처럼 자스 유형으로 다시 만들어야함
    #                 api_callResult = json.loads(api_callResult)
    #                 # 최종결과
    #                 translatedText = api_callResult['message']['result']["translatedText"]
    #                 embed = discord.Embed(title="번역결과", description=translatedText, color=0xffffff)
    #                 await ctx.send(embed=embed)
    #             else:
    #                 await ctx.trigger_typing()
    #                 embed = discord.Embed(title="에러", description="에러 코드: " + responsedCode, color=0xffffff)
    #                 await ctx.send(embed = embed)
    #     except HTTPError as e:
    #         await ctx.trigger_typing()
    #         embed = discord.Embed(title="에러", description="오류가 발생하여 번역에 실패했어요.", color=0xffffff)
    #         await ctx.send(embed = embed)

    # #En to Ko
    # @commands.command(aliases=['영한'])
    # @commands.cooldown(1, 2, commands.BucketType.user)
    # async def EnKo(self, ctx):
    #     reply = ctx.message.content.split(" ")
    #     if len(reply) > 1:
    #         for i in range(2, len(reply)):
    #             reply[1] = reply[1] + " " + reply[i]

    #     baseurl = "https://openapi.naver.com/v1/papago/n2mt"
    #     try:
    #         if len(reply) == 1:
    #             await ctx.trigger_typing()
    #             embed = discord.Embed(title="에러", description="단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.", color=0xffffff)
     
    #             await ctx.send(embed = embed)
    #         else:
    #             await ctx.trigger_typing()
    #             dataParmas = "source=en&target=ko&text=" + reply[1]
    #             # 요청 인스턴스 만들기
    #             request = Request(baseurl)
    #             # 패킷에 헤더 추가
    #             request.add_header("X-Naver-Client-Id", client_id)
    #             request.add_header("X-Naver-Client-Secret", client_secret)
    #             response = urlopen(request, data=dataParmas.encode("utf-8"))

    #             responsedCode = response.getcode()
    #             if (responsedCode == 200):
    #                 response_body = response.read()
    #                 # response_body -> byte string : decode to utf-8
    #                 api_callResult = response_body.decode('utf-8')
    #                 # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
    #                 api_callResult = json.loads(api_callResult)
    #                 # Final Result
    #                 translatedText = api_callResult['message']['result']["translatedText"]
    #                 embed = discord.Embed(title="번역결과", description=translatedText, color=0xffffff)
         
    #                 await ctx.send(embed=embed)
    #             else:
    #                 await ctx.trigger_typing()
    #                 embed = discord.Embed(title="에러", description="에러 코드: " + responsedCode, color=0xffffff)
         
    #                 await ctx.send(embed = embed)
    #     except HTTPError as e:
    #         await ctx.trigger_typing()
    #         embed = discord.Embed(title="에러", description="오류가 발생하여 번역에 실패했어요.", color=0xffffff)
 
    #         await ctx.send(embed = embed)

    # #Ko to zh-CN(간체)
    # @commands.command(aliases=['한중'])
    # @commands.cooldown(1, 2, commands.BucketType.user)
    # async def KoCh(self, ctx):
    #     reply = ctx.message.content.split(" ")
    #     if len(reply) > 1:
    #         for i in range(2, len(reply)):
    #             reply[1] = reply[1] + " " + reply[i]

    #     baseurl = "https://openapi.naver.com/v1/papago/n2mt"
    #     try:
    #         if len(reply) == 1:
    #             embed = discord.Embed(title="에러", description="단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.", color=0xffffff)
    #             await ctx.send(embed = embed)
    #         else:
    #             await ctx.trigger_typing()
    #             dataParmas = "source=ko&target=zh-CN&text=" + reply[1]
    #             # Make a Request Instance
    #             request = Request(baseurl)
    #             # add header to packet
    #             request.add_header("X-Naver-Client-Id", client_id)
    #             request.add_header("X-Naver-Client-Secret", client_secret)
    #             response = urlopen(request, data=dataParmas.encode("utf-8"))
    #             responsedCode = response.getcode()
    #             if (responsedCode == 200):
    #                 response_body = response.read()
    #                 # response_body -> byte string : decode to utf-8
    #                 api_callResult = response_body.decode('utf-8')
    #                 # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
    #                 api_callResult = json.loads(api_callResult)
    #                 # Final Result
    #                 translatedText = api_callResult['message']['result']["translatedText"]
    #                 embed = discord.Embed(title="번역결과", description=translatedText, color=0xffffff)
    #                 await ctx.send(embed=embed)
    #             else:
    #                 embed = discord.Embed(title="에러", description="에러 코드: " + responsedCode, color=0xffffff)
    #                 await ctx.send(embed = embed)
    #     except HTTPError as e:
    #         embed = discord.Embed(title="에러", description="오류가 발생하여 번역에 실패했어요.", color=0xffffff)
    #         await ctx.send(embed = embed)

    # #Ko to Ja
    # @commands.command(aliases=['한일'])
    # @commands.cooldown(1, 2, commands.BucketType.user)
    # async def KoJa(self, ctx):
    #     reply = ctx.message.content.split(" ")
    #     if len(reply) > 1:
    #         for i in range(2, len(reply)):
    #             reply[1] = reply[1] + " " + reply[i]
    #     baseurl = "https://openapi.naver.com/v1/papago/n2mt"
    #     try:
    #         if len(reply) == 1:
    #             embed = discord.Embed(title="에러", description="단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.", color=0xffffff)
    #             await ctx.send(embed = embed)
    #         else:
    #             await ctx.trigger_typing()
    #             dataParmas = "source=ko&target=ja&text=" + reply[1]
    #             # Make a Request Instance
    #             request = Request(baseurl)
    #             # add header to packet
    #             request.add_header("X-Naver-Client-Id", client_id)
    #             request.add_header("X-Naver-Client-Secret", client_secret)
    #             response = urlopen(request, data=dataParmas.encode("utf-8"))
    #             responsedCode = response.getcode()
    #             if (responsedCode == 200):
    #                 response_body = response.read()
    #                 # response_body -> byte string : decode to utf-8
    #                 api_callResult = response_body.decode('utf-8')
    #                 # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
    #                 api_callResult = json.loads(api_callResult)
    #                 # Final Result
    #                 translatedText = api_callResult['message']['result']["translatedText"]
    #                 embed = discord.Embed(title="번역결과", description=translatedText, color=0xffffff)
    #                 await ctx.send(embed=embed)
    #             else:
    #                 embed = discord.Embed(title="에러", description="에러 코드: " + responsedCode, color=0xffffff)
    #                 await ctx.send(embed = embed)
    #     except HTTPError as e:
    #         embed = discord.Embed(title="에러", description="오류가 발생하여 번역에 실패했어요.", color=0xffffff)
    #         await ctx.send(embed = embed)

    # #Ja to Ko
    # @commands.command(aliases=['일한'])
    # @commands.cooldown(1, 2, commands.BucketType.user)
    # async def JaKo(self, ctx):
    #     reply = ctx.message.content.split(" ")
    #     if len(reply) > 1:
    #         for i in range(2, len(reply)):
    #             reply[1] = reply[1] + " " + reply[i]

    #     baseurl = "https://openapi.naver.com/v1/papago/n2mt"
    #     try:
    #         if len(reply) == 1:
    #             embed = discord.Embed(title="에러", description="단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.", color=0xffffff)
     
    #             await ctx.send(embed = embed)
    #         else:
    #             dataParmas = "source=ja&target=ko&text=" + reply[1]
    #             # Make a Request Instance
    #             request = Request(baseurl)
    #             # add header to packet
    #             request.add_header("X-Naver-Client-Id", client_id)
    #             request.add_header("X-Naver-Client-Secret", client_secret)
    #             response = urlopen(request, data=dataParmas.encode("utf-8"))
    #             responsedCode = response.getcode()
    #             if (responsedCode == 200):
    #                 response_body = response.read()
    #                 # response_body -> byte string : decode to utf-8
    #                 api_callResult = response_body.decode('utf-8')
    #                 # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
    #                 api_callResult = json.loads(api_callResult)
    #                 # Final Result
    #                 translatedText = api_callResult['message']['result']["translatedText"]
    #                 embed = discord.Embed(title="번역결과", description=translatedText, color=0xffffff)
    #                 await ctx.send(embed=embed)
    #             else:
    #                 embed = discord.Embed(title="에러", description="에러 코드: " + responsedCode, color=0xffffff)
    #                 await ctx.send(embed = embed)
    #     except HTTPError as e:
    #         embed = discord.Embed(title="에러", description="오류가 발생하여 번역에 실패했어요.", color=0xffffff)
    #         await ctx.send(embed = embed)

    # #zh-CN to Ko(간체)
    # @commands.command(aliases=['중한'])
    # @commands.cooldown(1, 2, commands.BucketType.user)
    # async def ChKo(self, ctx):
    #     reply = ctx.message.content.split(" ")
    #     if len(reply) > 1:
    #         for i in range(2, len(reply)):
    #             reply[1] = reply[1] + " " + reply[i]
    #     baseurl = "https://openapi.naver.com/v1/papago/n2mt"
    #     try:
    #         if len(reply) == 1:
    #             embed = discord.Embed(title="에러", description="단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.", color=0xffffff)
    #             await ctx.send(embed = embed)
    #         else:
    #             dataParmas = "source=zh-CN&target=ko&text=" + reply[1]
    #             # Make a Request Instance
    #             request = Request(baseurl)
    #             # add header to packet
    #             request.add_header("X-Naver-Client-Id", client_id)
    #             request.add_header("X-Naver-Client-Secret", client_secret)
    #             response = urlopen(request, data=dataParmas.encode("utf-8"))

    #             responsedCode = response.getcode()
    #             if (responsedCode == 200):
    #                 response_body = response.read()
    #                 # response_body -> byte string : decode to utf-8
    #                 api_callResult = response_body.decode('utf-8')
    #                 # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
    #                 api_callResult = json.loads(api_callResult)
    #                 # Final Result
    #                 translatedText = api_callResult['message']['result']["translatedText"]
    #                 embed = discord.Embed(title="번역결과", description=translatedText, color=0xffffff)
    #                 await ctx.send(embed=embed)
    #             else:
    #                 embed = discord.Embed(title="에러", description="에러 코드: " + responsedCode, color=0xffffff)
    #                 await ctx.send(embed = embed)
    #     except HTTPError as e:
    #         embed = discord.Embed(title="에러", description="오류가 발생하여 번역에 실패했어요.", color=0xffffff)
    #         await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Translate(bot))