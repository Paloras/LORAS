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
import requests
from urllib.request import urlopen, Request
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.parse import quote
from urllib import parse
import json
import datetime
import aiohttp
from requests import get, post
from os import environ

class search(commands.Cog): 

    def __init__(self, bot): 
        self.bot = bot 

    @commands.command(aliases=['네이버'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def blog(self, ctx, *, search_query):
        temp = 0
        url_base = "https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query="
        url = url_base + urllib.parse.quote(search_query)
        title = ["", "", "", "", ""] # 더 많은 검색 : 빈칸("")을 늘리셔야 합니다.
        link = ["", "", "", "", ""] # 더 많은 검색 : 빈칸("")을 늘리셔야 합니다.
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')
        result = soup.find_all('a', "sh_blog_title _sp_each_url _sp_each_title")
        embed = discord.Embed(title="검색 결과", description=" ", color=0x00ff56)
        for n in result:
            if temp == 5: # 더 많은 검색 : 숫자(3)를 늘리셔야 합니다.
                break
            title[temp] = n.get("title")
            link[temp] = n.get("href")
            embed.add_field(name="블로그", value="["+title[temp]+"]("+link[temp]+")", inline=False)
            temp += 1
        embed.set_footer(text="검색 완료!")
        await ctx.send(embed=embed)
    @blog.error
    async def blog_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    
    @commands.command(name="오늘뉴스") 
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def adwuhi(self, ctx):
        temp = 0
        u = requests.get("https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=100")
        t = u.content
        bus = BeautifulSoup(t, "html.parser")
        babo = bus.find("ul", {"class": "type06_headline"})
        hi = babo.find_all("li")
        embed = discord.Embed(title="투데이 뉴스", description="")
        for item in hi:
            if temp == 3:
                break
            title = item.find("dt", "").find("a").text.strip("\n\t")
            cuty = item.find("span", {"class": "lede"}).text
            sim = item.find("span", {"class": "writing"}).text
            embed.add_field(name=title, value=cuty+ "\n"+sim + "\n출처 네이버 news", inline=False)
            temp+=1
        await ctx.send(embed=embed)
    @adwuhi.error
    async def adwuhi_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(aliases=['유튜브'], pass_context=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def 유튜브검색(self, ctx, *, search=None):
        await ctx.send("검색중입니다.")
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True
            }
            song_search = " ".join(search)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(f"ytsearch1:{song_search}", download=False)['entries'][0]['webpage_url']
            await ctx.send(str(result))
        except youtube_dl.DownloadError:
            await ctx.send("검색에 실패했습니다...\n혹시 모르니까 여기라도 확인해보세요.")
            result = search.replace(" ", "+")
            embed = discord.Embed(title="유튜브 검색 결과", description=f"'{search}'의 검색 결과입니다.", colour=discord.Color.red(),
                                  url=f"https://www.youtube.com/results?search_query={result}")
            embed.set_thumbnail(url="https://www.youtube.com/yts/img/yt_1200-vflhSIVnY.png")
            await ctx.send(embed=embed)
    @유튜브검색.error
    async def 유튜브검색_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(aliases=['뉴스'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _news(self, ctx, *, search_query):
        temp = 0
        url_base = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query="
        url = url_base + urllib.parse.quote(search_query)
        title = ["", "", "", "", ""] # 더 많은 검색 : 빈칸("")을 늘리셔야 합니다.
        link = ["", "", "", "", ""] # 더 많은 검색 : 빈칸("")을 늘리셔야 합니다.
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')
        result = soup.find_all('a', "_sp_each_title")
        embed = discord.Embed(title="검색 결과", description=" ", color=0x00ff56)
        for n in result:
            if temp == 5: # 더 많은 검색 : 숫자(3)를 늘리셔야 합니다.
                break
            title[temp] = n.get("title")
            link[temp] = n.get("href")
            embed.add_field(name="뉴스", value="["+title[temp]+"]("+link[temp]+")", inline=False)
            temp+=1
        embed.set_footer(text="검색 완료!")
        await ctx.send(embed=embed)
    @_news.error
    async def _news_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command("실검")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def realtime(self, ctx):
        url = "https://m.search.naver.com/search.naver?query=%EC%8B%A4%EA%B2%80"
        html = urlopen(url)
        parse = BeautifulSoup(html, "html.parser")
        result = ""
        tags = parse.find_all("span", {"class" : "tit _keyword"})
        temp = 1
        for i, e in enumerate(tags):
            if temp == 16:
                break
            url = "https://search.naver.com/search.naver?ie=UTF-8&query=" + urllib.parse.quote(e.text)
            result = result + (str(i+1))+"위 | ["+e.text+"]("+url+")\n"
            temp+=1
        embed = discord.Embed(title="네이버 실시간 검색어 순위", description=result, color=0xb8bb6a)
        await ctx.send(embed=embed)
    @realtime.error
    async def realtime_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(name="인벤", pass_context=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def inven(self, ctx):
        """인벤의 주요뉴스를 보여줍니다"""
        embed = discord.Embed(title="인벤 주요뉴스", color=0xb8bb6a)
        targetSite = 'http://www.inven.co.kr/webzine/news/?hotnews=1'

        header = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        melonrqRetry = requests.get(targetSite, headers=header)
        melonht = melonrqRetry.text
        melonsp = BeautifulSoup(melonht, 'html.parser')
        artists = melonsp.findAll('span', {'class': 'title'})
        titles = melonsp.findAll('span', {'class': 'summary'})
        for i in range(5):
            artist = artists[i].text.strip()
            title = titles[i].text.strip()
            embed.add_field(name="{0:3d}".format(i + 1), value='제목:{0} - 내용:{1}'.format(artist, title), inline=False)
            embed.timestamp = ctx.message.created_at
        await ctx.send(embed=embed)
    @inven.error
    async def inven_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(name="노래순위", pass_context=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def musicadad(self, ctx):
        """멜론차트를 모여줍니다."""
        embed = discord.Embed(
            title="노래순위", description="노래순위입니다.", color=0xb8bb6a
        )
        targetSite = 'https://www.melon.com/chart/index.htm'

        header = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        melonrqRetry = requests.get(targetSite, headers=header)
        melonht = melonrqRetry.text
        melonsp = BeautifulSoup(melonht, 'html.parser')
        artists = melonsp.findAll('span', {'class': 'checkEllipsis'})
        titles = melonsp.findAll('div', {'class': 'ellipsis rank01'})
        for i in range(10):
            artist = artists[i].text.strip()
            title = titles[i].text.strip()
            embed.add_field(name="{0:3d}위".format(i + 1), value='{0} - {1}'.format(artist, title), inline=False)
            embed.timestamp = ctx.message.created_at
        await ctx.send(embed=embed)
    @musicadad.error
    async def musicadad_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')
    
    @commands.command(name="날씨")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def weather(self, ctx, location):
        enc_location = urllib.parse.quote(location+'날씨')
        hdr = {'User-Agent': 'Mozilla/5.0'}
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + enc_location
        req = Request(url, headers=hdr)
        html = urllib.request.urlopen(req)
        bsObj = BeautifulSoup(html, "html.parser")
        todayBase = bsObj.find('div', {'class': 'main_info'})

        todayTemp1 = todayBase.find('span', {'class': 'todaytemp'})
        todayTemp = todayTemp1.text.strip()  # 온도

        todayValueBase = todayBase.find('ul', {'class': 'info_list'})
        todayValue2 = todayValueBase.find('p', {'class': 'cast_txt'})
        todayValue = todayValue2.text.strip()  # 밝음,어제보다 ?도 높거나 낮음을 나타내줌

        todayFeelingTemp1 = todayValueBase.find('span', {'class': 'sensible'})
        todayFeelingTemp = todayFeelingTemp1.text.strip()  # 체감온도

        todayMiseaMongi1 = bsObj.find('div', {'class': 'sub_info'})
        todayMiseaMongi2 = todayMiseaMongi1.find('div', {'class': 'detail_box'})
        todayMiseaMongi3 = todayMiseaMongi2.find('dd')
        todayMiseaMongi = todayMiseaMongi3.text  # 미세먼지

        tomorrowBase = bsObj.find('div', {'class': 'table_info weekly _weeklyWeather'})
        tomorrowTemp1 = tomorrowBase.find('li', {'class': 'date_info'})
        tomorrowTemp2 = tomorrowTemp1.find('dl')
        tomorrowTemp3 = tomorrowTemp2.find('dd')
        tomorrowTemp = tomorrowTemp3.text.strip()  # 오늘 오전,오후온도

        tomorrowAreaBase = bsObj.find('div', {'class': 'tomorrow_area'})
        tomorrowMoring1 = tomorrowAreaBase.find('div', {'class': 'main_info morning_box'})
        tomorrowMoring2 = tomorrowMoring1.find('span', {'class': 'todaytemp'})
        tomorrowMoring = tomorrowMoring2.text.strip()  # 내일 오전 온도

        tomorrowValue1 = tomorrowMoring1.find('div', {'class': 'info_data'})
        tomorrowValue = tomorrowValue1.text.strip()  # 내일 오전 날씨상태, 미세먼지 상태

        tomorrowAreaBase = bsObj.find('div', {'class': 'tomorrow_area'})
        tomorrowAllFind = tomorrowAreaBase.find_all('div', {'class': 'main_info morning_box'})
        tomorrowAfter1 = tomorrowAllFind[1]
        tomorrowAfter2 = tomorrowAfter1.find('p', {'class': 'info_temperature'})
        tomorrowAfter3 = tomorrowAfter2.find('span', {'class': 'todaytemp'})
        tomorrowAfterTemp = tomorrowAfter3.text.strip()  # 내일 오후 온도

        tomorrowAfterValue1 = tomorrowAfter1.find('div', {'class': 'info_data'})
        tomorrowAfterValue = tomorrowAfterValue1.text.strip()# 내일 오후 날씨상태,미세먼지

        embed = discord.Embed(
            title=location+ ' 날씨 정보', description=location+ '날씨 정보입니다.',
            colour=discord.Colour.gold()
        )
        embed.add_field(name='현재온도', value=todayTemp+'˚', inline=False)  # 현재온도
        embed.add_field(name='체감온도', value=todayFeelingTemp, inline=False)  # 체감온도
        embed.add_field(name='현재상태', value=todayValue, inline=False)  # 밝음,어제보다 ?도 높거나 낮음을 나타내줌
        embed.add_field(name='현재 미세먼지 상태', value=todayMiseaMongi, inline=False)  # 오늘 미세먼지
        embed.add_field(name='오늘 오전/오후 날씨', value=tomorrowTemp, inline=False)  # 오늘날씨 # color=discord.Color.blue()
        embed.add_field(name='**----------------------------------**',value='**----------------------------------**', inline=False)  # 구분선
        embed.add_field(name='내일 오전온도', value=tomorrowMoring+'˚', inline=False)  # 내일오전날씨
        embed.add_field(name='내일 오전날씨상태, 미세먼지 상태', value=tomorrowValue, inline=False)  # 내일오전 날씨상태
        embed.add_field(name='내일 오후온도', value=tomorrowAfterTemp + '˚', inline=False)  # 내일오후날씨
        embed.add_field(name='내일 오후날씨상태, 미세먼지 상태', value=tomorrowAfterValue, inline=False)  # 내일오후 날씨상태
        await ctx.send(embed=embed)
    @weather.error
    async def weather_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(aliases=['한강'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def 수온(self, ctx):
        req = Request("http://hangang.dkserver.wo.tc/")
        webpage = urlopen(req).read()
        output = json.loads(webpage)
        temp = output['temp']
        time = output['time']
        embed = discord.Embed(title="한강 수온", description=f"온도 : {temp}", color=0x00ff56)
        embed.set_footer(text=f"측정시간 : {time}")
        await ctx.send(embed=embed)
    @수온.error
    async def 수온_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')
    
    @commands.command(aliases=['코로나'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def corona(self, ctx):
        req = Request("http://api.corona-19.kr/korea/?serviceKey=e5d81b982aff2f6bd7c5ec2811bd77d66")
        webpage = urlopen(req).read()
        output = json.loads(webpage)
        total = output['TotalCase']
        recover = output['TotalRecovered']
        death = output['TotalDeath']
        time = output['updateTime']
        Quarantine = output['NowCase']
        recoveryrate = output['recoveredPercentage']
        deathrate = output['deathPercentage']
        recovering = output['checkingCounter']
        todaydeath = output['TodayDeath']
        todayrecover = output['TodayRecovered']
        caserate = output['casePercentage']
        testing = output['TotalChecking']

        req2 = Request("http://api.corona-19.kr/korea/country/new/?serviceKey=e5d81b982aff2f6bd7c5ec2811bd77d66")
        webpage1 = urlopen(req2).read()
        output2 = json.loads(webpage1)
        todaycase = output2['korea']['newCase']
        localcase = output2['korea']['newCcase']
        foreigncase = output2['korea']['newFcase']

        todayrecovering = int(todaycase) - int(todayrecover)

        embed = discord.Embed(title="**코로나 확진자수**", color=0x00ff56)
        embed.set_thumbnail(url= 'https://search.pstatic.net/common/?src=http%3A%2F%2Fimgnews.naver.net%2Fimage%2F025%2F2020%2F04%2F03%2F0002990027_001_20200403143505263.jpg&type=sc960_832')
        embed.add_field(name="**확진자**", value=f"{total}명(+{todaycase}명)")
        embed.add_field(name="**일일확진자**", value=f'{todaycase}명\n   ㄴ국내발생 : {localcase}명/ 해외발생: {foreigncase}명')
        embed.add_field(name="**치료중**", value=f"{Quarantine}명(+{todayrecovering})")
        embed.add_field(name="**사망자**", value=f"{death}명(+{todaydeath}명)\n치사율:{deathrate}%")
        embed.add_field(name="**완치자**", value=f"{recover}명(+{todayrecover}명)\n완치율: {recoveryrate}%")
        embed.add_field(name="**검사자**", value=f"{testing}명"
        embed.add_field(name="**누적 확진률**", value=f"{caserate}%")
        embed.add_field(name="**치사율**", value=f"{deathrate}%")

        temp = 0
        title = ["", ""] # 더 많은 검색 : 빈칸("")을 늘리셔야 합니다.
        link = ["", ""] # 더 많은 검색 : 빈칸("")을 늘리셔야 합니다.
        url ="https://search.naver.com/search.naver?where=news&sm=tab_jum&query=%EC%BD%94%EB%A1%9C%EB%82%98"
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')
        result = soup.find_all('a', "_sp_each_title")
        for n in result:
            if temp == 2: # 더 많은 검색 : 숫자(3)를 늘리셔야 합니다.
                break
            title[temp] = n.get("title")
            link[temp] = n.get("href")
            embed.add_field(name="뉴스", value="["+title[temp]+"]("+link[temp]+")", inline=False)
            temp+=1
        
        embed.set_footer(text=f"{time}")
        await ctx.send(embed=embed)
    @corona.error
    async def corona_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')
    
def setup(bot):
    bot.add_cog(search(bot))
