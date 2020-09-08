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

class helper(commands.Cog, name='도움말'): #2

    def __init__(self, bot): #3
        self.bot = bot #4

    @commands.command(name="도움", aliases=['도움말'], help="명령어를 알려줘여.")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def help(self, ctx, category):
        if category == "관리":
            embed=discord.Embed(title="**카테고리 : 관리**", color=0xff752e)
            embed.add_field(name="**팔추방**", value="사용법: 팔추방 (추방할사람 맨션)\n서버유저을 추방시킵니다.", inline=True)
            embed.add_field(name="**팔밴**", value="사용법: 팔밴 (추방할사람맨션)\n해당 유저를 차단합니다.", inline=True)
            embed.add_field(name="**팔언밴**", value="사용법: 팔언밴 (유저이름#태그)\n해당유저의 차단을 해제합니다.", inline=True)
            embed.add_field(name="**팔청소**", value="사용법: 팔청소 (숫자)\n해당숫자의 메시지를 없앱니다.", inline=True)
            embed.add_field(name="**팔슬로우**", value="사용법: 팔슬로우 (숫자)\n해당 채널에 슬로우를 겁니다.", inline=True)
            embed.add_field(name="**팔역할추가**", value="사용법: 팔역할추가 (유저맨션) (역할)\n해당유저한테 해당역할을 줍니다.", inline=True)
            embed.add_field(name="**팔역할제거**", value="사용법: 팔역할제거 (유저맨션) (역할)\n해당유저한테서 해당 역할을 뺐습니다.", inline=True)
            embed.add_field(name="**팔경고**", value="사용법: 팔경고 (유저맨션) (사유)\n해당유저한테 경고를 줍니다.", inline=True)
            embed.add_field(name="**팔경고삭제**", value="사용법: 팔경고삭제 (유저맨션) (경고번호)\n해당유저의 경고를 삭제 처리합니다.", inline=True)
            embed.add_field(name="**팔누적경고**", value="사용법: 팔누적경고 (유저맨션)\n해당유저의 경고를 알아봅니다.", inline=True)
            embed.add_field(name="**팔경고정보**", value="사용법: 팔경고정보 (유저맨션) (경고번호)\n경고 번호에 대한 정보를 알려줍니다.", inline=True)
            embed.set_footer(text="제작자 : !  PLRS#3588", icon_url="https://cdn.discordapp.com/avatars/384227121267998722/45244dc5542cccc4ca0424befef4167e.webp?size=1024")
            await ctx.send(embed=embed)
        elif category == "음악":        
            embed=discord.Embed(title="**카테고리 : 음악**", color=0xff752e)
            embed.add_field(name="**팔재생**", value="사용법: 팔재생 (노래 이름)\n노래를 틉니다.", inline=True)
            embed.add_field(name="**팔스킵**", value="사용법: 팔스킵\n현재 틀고있는 음악을 넘어갑니다.", inline=True)
            embed.add_field(name="**팔정지**", value="사용법: 팔정지\n음악을 일시정지 또는 재생시킵니다.", inline=True)
            embed.add_field(name="**팔제거**", value="사용법: 팔제거 (음악 이름)\n재생목록에서 해당 노래를 지웁니다.", inline=True)
            embed.set_footer(text="제작자 : !  PLRS#3588", icon_url="https://cdn.discordapp.com/avatars/384227121267998722/45244dc5542cccc4ca0424befef4167e.webp?size=1024")
            await ctx.send(embed=embed)
        elif category == "검색":
            embed=discord.Embed(title="**카테고리 : 검색**", color=0xff752e)
            embed.add_field(name="**팔네이버**", value="사용법: 팔네이버 (검색할내용)\n검색한 내용을 블로그에서 찾아줍니다.", inline=True)
            embed.add_field(name="**팔뉴스**", value="사용법: 팔뉴스 (검색할내용)\n검색한내용에 대한 뉴스를 보여줍니다.", inline=True)
            embed.add_field(name="**팔실검**", value="사용법: 팔실검\n현재 네이버 실검순위를 알려줍니다.", inline=True)
            embed.add_field(name="**팔유튜브**", value="사용법: 팔유튜브 (검색할내용)\n검색한 내용과 일치하거나 비슷한 동영상을 띄웁니다.", inline=True)
            embed.set_footer(text="제작자 : !  PLRS#3588", icon_url="https://cdn.discordapp.com/avatars/384227121267998722/45244dc5542cccc4ca0424befef4167e.webp?size=1024")
            await ctx.send(embed=embed)
        elif category == "게임":
            embed=discord.Embed(title="**카테고리 : 게임**", color=0xff752e)#**팔8핀**\n사용법: 팔8핀 (질문)\n아무질문에 대답해줍니다.\n
            embed.add_field(name="**팔동전**", value="사용법: 팔동전\n동전을 던집니다.", inline=True)
            embed.add_field(name="**팔랜덤**", value="사용법: 팔랜덤 (선택지1) (선택지2) …\n선택지 중 하나를 골라줍니다.", inline=True)
            embed.add_field(name="**팔계정생성**", value="사용법: 팔계정생성\n전체계정을 생성합니다.", inline=True)
            embed.add_field(name="**팔통장**", value="사용법: 팔통장\n전체통장에 있는 돈의 액수를 알려줍니다.", inline=True)
            embed.add_field(name="**팔일**", value="사용법: 팔일\n전체계정에 돈이 랜덤으로 들어갑니다.", inline=True)
            embed.add_field(name="**팔도박**", value="사용법: 팔도박 (액수)\n확률적으로 2~3배가 됩니다.", inline=True)
            embed.add_field(name="**팔계정삭제**", value="사용법: 팔계정삭제\n사용자의 전체계정을 삭제합니다.", inline=True)
            embed.set_footer(text="제작자 : !  PLRS#3588", icon_url="https://cdn.discordapp.com/avatars/384227121267998722/45244dc5542cccc4ca0424befef4167e.webp?size=1024")
            await ctx.send(embed=embed)
        elif category == "기타":
            embed=discord.Embed(title="**카테고리 : 기타**", color=0xff752e)
            embed.add_field(name="**팔출력**", value="사용법: 팔출력 \n로라스봇이 정상작동중인지 알려줍니다.", inline=True)
            embed.add_field(name="**팔핑**", value="사용법: 팔핑\n현재 로라스봇의 핑을 알려줍니다.", inline=True)
            embed.add_field(name="**팔타이머**", value="사용법: 팔타이머 (시간)\n시간이 지난 후 맨션을 해서 시간이 지났음을 알려줍니다.", inline=True)
            embed.add_field(name="**팔시간**", value="사용법: 팔시간\n현재 한국의 시각을 알려줍니다.", inline=True)
            embed.add_field(name="**팔문의**", value="사용법: 팔문의팔건의 (건의내용)\n개발자한테 문의 또는 건의를 합니다.", inline=True)
            # embed.add_field(name="**팔자가진단**", value="사용법: 팔자가진단\n자가진단을 대신해줍니다.", inline=True)
            # embed.add_field(name="**팔자가진단설정**", value="사용법: 팔자가진단설정 (학교명) (이름) (생년월일)\n자가진단을 하기전 설정을합니다.", inline=True)
            embed.set_footer(text="제작자 : !  PLRS#3588", icon_url="https://cdn.discordapp.com/avatars/384227121267998722/45244dc5542cccc4ca0424befef4167e.webp?size=1024")
            await ctx.send(embed=embed)
        elif category == "계산":
            embed=discord.Embed(title="**카테고리 : 계산**", color=0xff752e)
            embed.add_field(name="**팔계산**", value="사용법: 팔계산 (식)\n계산합니다.", inline=True)
            embed.add_field(name="**팔최대공약수**", value="사용법: 팔최대공약수 (숫자1) (숫자2)\n두수의 최대공약수를 구합니다..", inline=True)
            embed.add_field(name="**팔최소공배수**", value="사용법: 팔최소공배수 (숫자1) (숫자2)\n두수의 최소공배수를 구합니다..", inline=True)
            embed.add_field(name="**팔근**", value="사용법: 팔근\n근의 공식을 써서 근과 대칭축을 구합니다.", inline=True)
            embed.add_field(name="**팔제곱근**", value="사용법: 팔제곱근 (숫자)\n제곱근을 구합니다.", inline=True)
            embed.set_footer(text="제작자 : !  PLRS#3588", icon_url="https://cdn.discordapp.com/avatars/384227121267998722/45244dc5542cccc4ca0424befef4167e.webp?size=1024")
            await ctx.send(embed=embed)
        elif category == "번역":
            embed=discord.Embed(title="**카테고리 : 번역**", color=0xff752e)
            embed.add_field(name="**팔번역**", value="사용법: 팔번역 (번역될언어) (번역될문장)\n해당언어로 번역합니다.", inline=True)
            embed.add_field(name="**팔번영**", value="사용법: 팔번영 (번역할 문장)\n영어로 번역합니다.", inline=True)
            embed.add_field(name="**팔번간**", value="사용법: 팔번간 (번역할 문장)\n중국간체로 번역합니다.", inline=True)
            embed.add_field(name="**팔번일**", value="사용법: 팔번일 (번역할 문장)\n일본어로 번역합니다.", inline=True)
            embed.add_field(name="**팔번한**", value="사용법: 팔번한 (번역할 문장)\한국어로 번역합니다.", inline=True)
            embed.set_footer(text="제작자 : !  PLRS#3588", icon_url="https://cdn.discordapp.com/avatars/384227121267998722/45244dc5542cccc4ca0424befef4167e.webp?size=1024")
            await ctx.send(embed=embed)
        elif category == "정보":
            embed=discord.Embed(title="**카테고리 : 정보**", color=0xff752e)
            embed.add_field(name="**팔유저**", value="사용법: 팔유저 (유저맨션)\n해당 유저에 대해 알려줍니다.", inline=True)
            embed.add_field(name="**팔서버**", value="사용법: 팔서버\n현재 명령어를 친 서버정보를 가져옵니다.", inline=True)
            embed.add_field(name="**팔채널**", value="사용법: 팔채널\n해당 서버에 있는 채널에 대해 알려줍니다.", inline=True)
            embed.add_field(name="**팔아바타**", value="사용법: 팔아바타 (유저맨션)\n해당유저의 프로필사진을 가져옵니다.", inline=True)
            embed.add_field(name="**팔이모지**", value="사용법: 팔이모지\n해당 서버에 있는 이모지에 대해 알려줍니다.", inline=True)
            embed.add_field(name="**팔역할**", value="사용법: 팔역할\n해당 서버에 있는 역할에 대해 알려줍니다.", inline=True)
            embed.set_footer(text="제작자 : !  PLRS#3588", icon_url="https://cdn.discordapp.com/avatars/384227121267998722/45244dc5542cccc4ca0424befef4167e.webp?size=1024")
            await ctx.send(embed=embed)
    @help.error
    async def help_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("오류가 떳어요! 잠시후 다시 실행해보세요! " + format(ctx.message.author) + "님")
        elif isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="안녕하세요. 로라스입니다.", description="**카테고리**\n관리 게임 음악 검색 계산 번역 정보 기타\n\n사용법: 팔도움 (카테고리)", color=0xff752e)
            embed.add_field(name="**관리**", value="팔추방 팔밴 팔언밴 팔청소\n팔슬로우모드 팔역할추가\n팔역할제거")
            embed.add_field(name="**경고**", value="팔경고 팔경고삭제\n팔누적경고 팔경고확인")
            embed.add_field(name="**검색**", value="팔네이버 팔뉴스 팔실검\n팔유튜브 팔노래순위 팔인벤")
            embed.add_field(name="**음악**", value="팔재생 팔추가 팔스킵")
            embed.add_field(name="**번역**", value="팔번역 팔번영 팔번한\n팔번일 팔번간")
            embed.add_field(name="**게임**", value="팔동전 팔랜덤 팔계정생성\n팔통장 팔일 팔도박\n팔계정삭제 팔송금")
            embed.add_field(name="**전적**", value="팔배그솔로 팔배그듀오\n팔배그스쿼드 팔경쟁전 팔롤전적")
            embed.add_field(name="**계산**", value="팔계산기 팔최대공약수\n팔최소공배수팔근 팔제곱근")
            embed.add_field(name="**정보**", value="팔유저 팔서버  팔아바타\n팔채널팔역할 팔봇정보")
            embed.add_field(name="**부가기능**", value="팔출력 팔계산 팔아바타\n팔핑 팔유저 팔서버 팔타이머\n팔시간")# 팔자가진단 팔자가진단설정
            embed.add_field(name="ㅤ", value="\n더빨리 업데이트 소식을 들으실려면 서포트서버에 접속해주세요\n[봇 초대하기](https://discord.com/api/oauth2/authorize?client_id=723346442932191302&permissions=8&scope=bot)\n [서포트 서버](https://discord.gg/SVDm3hg)", inline=False)
            embed.set_footer(text="제작자 : !  PLRS#3588", icon_url="https://cdn.discordapp.com/avatars/384227121267998722/45244dc5542cccc4ca0424befef4167e.webp?size=1024")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            await ctx.send("**카테고리**를 넣어주세요.")
        elif isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    # @commands.command(name="44도움")
    # async def helpcommand(self, ctx, func=None):
    #     if func is None:
    #         embed = discord.Embed(title="Python Bot 도움말", description="접두사는 `팔` 입니다.") #Embed 생성
    #         cog_list = ['manage','core','music2','user','discord_bot_list_korea','calculate','search','translate','listener','game' ] # Cog 리스트 추가
    #         for x in cog_list: # cog_list에 대한 반복문
    #             cog_data = self.bot.get_cog(x) # x에 대해 Cog 데이터를 구하기
    #             command_list = cog_data.get_commands() # cog_data에서 명령어 리스트 구하기
    #             embed.add_field(name=x, value=" ".join([c.name for c in command_list]), inline=True) # 필드 추가
    #         await ctx.send(embed=embed) # 보내기
    #     else: # func가 None이 아니면
    #         command_notfound = True # 이걸 어떻게 쓸지 생각해보세요!
    #         for _title, cog in self.bot.cogs.items(): # title, cog로 item을 돌려주는데 title은 필요가 없습니다.
    #             if not command_notfound: # False면
    #                 break # 반복문 나가기

    #             else: # 아니면
    #                 for title in cog.get_commands(): # 명령어를 아까처럼 구하고 title에 순차적으로 넣습니다.
    #                     if title.name == func: # title.name이 func와 같으면
    #                         cmd = self.bot.get_command(title.name) # title의 명령어 데이터를 구합니다.
    #                         embed = discord.Embed(title=f"명령어 : {cmd}", description=cmd.help) # Embed 만들기
    #                         embed.add_field(name="사용법", value=cmd.usage) # 사용법 추가
    #                         await ctx.send(embed=embed) # 보내기
    #                         command_notfound = False
    #                         break # 반복문 나가기
    #                     else:
    #                         command_notfound = True

def setup(bot): #5
    bot.add_cog(helper(bot))