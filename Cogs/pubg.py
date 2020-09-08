import discord
import asyncio
from discord.ext import commands
from urllib.request import urlopen, Request
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.parse import quote
from urllib import parse
import bs4
import urllib
import requests
import urllib.request
import os
import json
from bs4 import BeautifulSoup
import re # Regex for youtube link
import warnings
import unicodedata
import time

class pubg(commands.Cog):
    
    def __init__(self, bot):
        """Initialisation bot"""
        self.bot = bot
    
    def is_owner(self, ctx):
        return ctx.message.author.id == 384227121267998722

    @commands.Cog.listener()
    async def on_message(self, message):    
        if message.author.bot:
            return None

        if message.content.startswith("팔경쟁전"): #TabErrorTPP
            baseURL = "https://dak.gg/profile/"
            playerNickname = ''.join((message.content).split(' ')[1:])
            URL = baseURL + quote(playerNickname)
            
            try:
                html = urlopen(URL)
                bs = BeautifulSoup(html, 'html.parser')
                if len(message.content.split(" ")) == 1:
                    embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x5CD1E5)
                    embed.add_field(name="Player nickname not entered",value="To use command 팔경쟁전(1 : TPP or 2 : FPP) : 팔경쟁전 (Nickname)", inline=False)
                    await message.channel.send("Error : Incorrect command usage ", embed=embed)
                else:
                    accessors = bs.findAll('a', {'href': re.compile('\/statistics\/[A-Za-z]')})
    
                    # Season Information : ['PUBG',(season info),(Server),'overview']
                    seasonInfo = []
                    for si in bs.findAll('li', {'class': "active"}):
                        seasonInfo.append(si.text.strip())
                    serverAccessorAndStatus = []
                    # To prevent : Parsing Server Status, Make a result like Server:\nOnline. So I need to delete '\n'to get     good result
                    for a in accessors:
                        serverAccessorAndStatus.append(re.sub(pattern='[\n]', repl="", string=a.text.strip()))
    
                    # Varaible serverAccessorAndStatus : [(accessors),(ServerStatus),(Don't needed value)]
                    
                    # Varaibel rankElements : index 0: fpp 1 : tpp
                    
                    rankElements = bs.findAll('div',{'class' : re.compile('squad ranked [A-Za-z0-9]')})
                    
                    '''
                    -> 클래스 값을 가져와서 판별하는 것도 있지만 이 방법을 사용해 본다.
                    -> 만약 기록이 존재 하지 않는 경우 class 가 no_record라는 값을 가진 <div>가 생성된다. 이 태그로 데이터 유무     판별하면된다.
                    print(rankElements[1].find('div',{'class' : 'no_record'}))
                    '''
                    
                    if rankElements[0].find('div',{'class' : 'no_record'}) != None: # 인덱스 0 : 경쟁전 fpp -> 정보가 있는지     없는지 유무를 판별한다.
                        embed = discord.Embed(title="Record not found", description="Rank TPP record not found.",color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)

                        await message.channel.send("PUBG player " + playerNickname + "'s TPP Ranking information",embed=embed) 
                    else:
                        #Short of fpp Rank
                        fR = rankElements[0]
                        # Tier Information
        
                        # Get tier medal image
                        tierMedalImage = fR.find('div',{'class' : 'grade-info'}).img['src']
                        # Get tier Information
                        tierInfo = fR.find('div',{'class' : 'grade-info'}).img['alt']
        
                        # Rating Inforamtion
                        # RP Score
                        RPScore = fR.find('div',{'class' : 'rating'}).find('span',{'class' : 'caption'}).text
        
                        #Get top rate statistics
                        
                        #등수
                        topRatioRank  = topRatio = fR.find('p',{'class' : 'desc'}).find('span',{'class' : 'rank'}).text     
                         #상위 %                          
                        topRatio = fR.find('p',{'class' : 'desc'}).find('span',{'class' : 'top'}).text
        
                        # Main : Stats all in here.
        
                        mainStatsLayout = fR.find('div',{'class' : 'stats'})
        
                        #Stats Data Saved As List
        
                        statsList = mainStatsLayout.findAll('p',{'class' : 'value'})# [KDA,승률,Top10,평균딜량, 게임수, 평균등수]
                        statsRatingList = mainStatsLayout.findAll('span',{'class' : 'top'})#[KDA, 승률,Top10 평균딜량, 게임수]
                
                        for r in range(0,len(statsList)):
                        # \n으로 큰 여백이 있어 split 처리
                            statsList[r] = statsList[r].text.strip().split('\n')[0]
                            statsRatingList[r] = statsRatingList[r].text
                        # 평균등수는 stats Rating을 표시하지 않는다.
                        statsRatingList = statsRatingList[0:5]
                                                   
                        
                        embed = discord.Embed(title="Player Unkonw Battle Ground player search from dak.gg", description="",    color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        embed.add_field(name="Real Time Accessors and Server Status",
                                        value="Accessors : " + serverAccessorAndStatus[0] + " | " "Server Status : " +
                                              serverAccessorAndStatus[1].split(':')[-1], inline=False)  
                        embed.add_field(name="Player located server", value=seasonInfo[2] + " Server", inline=False)
                        embed.add_field(name = "Tier / Top Rate / Average Rank",
                                       value = tierInfo + " (" + RPScore + ") / "+topRatio + " / " + topRatioRank,inline=False)
                        embed.add_field(name="K/D", value=statsList[0] + "/" + statsRatingList[0], inline=True)
                        embed.add_field(name="승률", value=statsList[1] + "/" + statsRatingList[1], inline=True)
                        embed.add_field(name="Top 10 비율", value=statsList[2] + "/" + statsRatingList[2], inline=True)
                        embed.add_field(name="평균딜량", value=statsList[3] + "/" + statsRatingList[3], inline=True)
                        embed.add_field(name="게임수", value=statsList[4] + "판/" + statsRatingList[4], inline=True)
                        embed.add_field(name="평균등수", value=statsList[5],inline=True)
                        embed.set_thumbnail(url=f'https:{tierMedalImage}')

                        await message.channel.send("PUBG player " + playerNickname + "'s TPP Ranking information", embed=embed)
                        
                
            except HTTPError as e:
                embed = discord.Embed(title="Not existing plyer", description="Can't find player " + playerNickname + "'s     information.\nPlease check player's nickname again",color=0x5CD1E5)
                await message.channel.send("Error : Not existing player", embed=embed)
                print(e)
            except AttributeError as e:
                embed = discord.Embed(title="Not existing plyer",
                                      description="Can't find player " + playerNickname + "'s information.\nPlease check     player's nickname again",
                                      color=0x5CD1E5)
                await message.channel.send("Error : Not existing player", embed=embed)
                print(e)
        
        if message.content.startswith("팔경쟁전2"):#FPP 
            baseURL = "https://dak.gg/profile/"
            playerNickname = ''.join((message.content).split(' ')[1:])
            URL = baseURL + quote(playerNickname)
            
            try:
                html = urlopen(URL)
                bs = BeautifulSoup(html, 'html.parser')
                if len(message.content.split(" ")) == 1:
                    embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x5CD1E5)
                    embed.add_field(name="Player nickname not entered",
                                    value="To use command 팔경쟁전(1 : TPP or 2 : FPP) : 팔경쟁전2 (Nickname)", inline=False)

                    await message.channel.send("Error : Incorrect command usage ", embed=embed)
                else:
                    accessors = bs.findAll('a', {'href': re.compile('\/statistics\/[A-Za-z]')})
    
                    # Season Information : ['PUBG',(season info),(Server),'overview']
                    seasonInfo = []
                    for si in bs.findAll('li', {'class': "active"}):
                        seasonInfo.append(si.text.strip())
                    serverAccessorAndStatus = []
                    # To prevent : Parsing Server Status, Make a result like Server:\nOnline. So I need to delete '\n'to get     good result
                    for a in accessors:
                        serverAccessorAndStatus.append(re.sub(pattern='[\n]', repl="", string=a.text.strip()))
    
                    # Varaible serverAccessorAndStatus : [(accessors),(ServerStatus),(Don't needed value)]
                    
                    # index 0: fpp 1 : tpp
                    
                    rankElements = bs.findAll('div',{'class' : re.compile('squad ranked [A-Za-z0-9]')})
                    
                    '''
                    -> 클래스 값을 가져와서 판별하는 것도 있지만 이 방법을 사용해 본다.
                    -> 만약 기록이 존재 하지 않는 경우 class 가 no_record라는 값을 가진 <div>가 생성된다. 이 태그로 데이터 유무     판별하면된다.
                    print(rankElements[1].find('div',{'class' : 'no_record'}))
                    '''
                    
                    if rankElements[1].find('div',{'class' : 'no_record'}) != None: # 인덱스 0 : 경쟁전 fpp -> 정보가 있는지     없는지 유무를 판별한다a.
                        embed = discord.Embed(title="Record not found", description="Solo que record not found.",
                                              color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)

                        await message.channel.send("PUBG player " + playerNickname + "'s FPP Ranking information",embed=embed) 
                    else:
                        #Short of fpp Rank
                        fR = rankElements[1]
                        # Tier Information
        
                        # Get tier medal image
                        tierMedalImage = fR.find('div',{'class' : 'grade-info'}).img['src']
                        # Get tier Information
                        tierInfo = fR.find('div',{'class' : 'grade-info'}).img['alt']
        
                        # Rating Inforamtion
                        # RP Score
                        RPScore = fR.find('div',{'class' : 'rating'}).find('span',{'class' : 'caption'}).text
        
                        #Get top rate statistics
                        
                        #등수
                        topRatioRank  = topRatio = fR.find('p',{'class' : 'desc'}).find('span',{'class' : 'rank'}).text     
                         #상위 %                          
                        topRatio = fR.find('p',{'class' : 'desc'}).find('span',{'class' : 'top'}).text
        
                        # Main : Stats all in here.
        
                        mainStatsLayout = fR.find('div',{'class' : 'stats'})
        
                        #Stats Data Saved As List
        
                        statsList = mainStatsLayout.findAll('p',{'class' : 'value'})# [KDA,승률,Top10,평균딜량, 게임수, 평균등수]
                        statsRatingList = mainStatsLayout.findAll('span',{'class' : 'top'})#[KDA, 승률,Top10 평균딜량, 게임수]
                
                        for r in range(0,len(statsList)):
                        # \n으로 큰 여백이 있어 split 처리
                            statsList[r] = statsList[r].text.strip().split('\n')[0]
                            statsRatingList[r] = statsRatingList[r].text
                        # 평균등수는 stats Rating을 표시하지 않는다.
                        statsRatingList = statsRatingList[0:5]
                                                   
                        
                        embed = discord.Embed(title="Player Unkonw Battle Ground player search from dak.gg", description="",    color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        embed.add_field(name="Real Time Accessors and Server Status",
                                        value="Accessors : " + serverAccessorAndStatus[0] + " | " "Server Status : " +
                                              serverAccessorAndStatus[1].split(':')[-1], inline=False)  
                        embed.add_field(name="Player located server", value=seasonInfo[2] + " Server", inline=False)
                        embed.add_field(name = "Tier / Top Rate / Average Rank",
                                       value = tierInfo + " (" + RPScore + ") / "+topRatio + " / " + topRatioRank,inline=False)
                        embed.add_field(name="K/D", value=statsList[0] + "/" + statsRatingList[0], inline=True)
                        embed.add_field(name="승률", value=statsList[1] + "/" + statsRatingList[1], inline=True)
                        embed.add_field(name="Top 10 비율", value=statsList[2] + "/" + statsRatingList[2], inline=True)
                        embed.add_field(name="평균딜량", value=statsList[3] + "/" + statsRatingList[3], inline=True)
                        embed.add_field(name="게임수", value=statsList[4] + "판/" + statsRatingList[4], inline=True)
                        embed.add_field(name="평균등수", value=statsList[5],inline=True)
                        embed.set_thumbnail(url=f'https:{tierMedalImage}')

                        await message.channel.send("PUBG player " + playerNickname + "'s FPP Ranking information", embed=embed)
                        
                
            except HTTPError as e:
                embed = discord.Embed(title="Not existing plyer", description="Can't find player " + playerNickname + "'s     information.\nPlease check player's nickname again",color=0x5CD1E5)
                await message.channel.send("Error : Not existing player", embed=embed)
            except AttributeError as e:
                embed = discord.Embed(title="Not existing plyer",
                                      description="Can't find player " + playerNickname + "'s information.\nPlease check     player's nickname again",
                                      color=0x5CD1E5)
                await message.channel.send("Error : Not existing player", embed=embed)
    
        if message.content.startswith("팔배그솔로"):
            baseURL = "https://dak.gg/profile/"
            playerNickname = ''.join((message.content).split(' ')[1:])
            URL = baseURL + quote(playerNickname)
            try:
                html = urlopen(URL)
                bs = BeautifulSoup(html, 'html.parser')
                if len(message.content.split(" ")) == 1:
                    embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x5CD1E5)
                    embed.add_field(name="Player nickname not entered",
                                    value="To use command 팔배그솔로 : 팔배그솔로 (Nickname)", inline=False)

                    await message.channel.send("Error : Incorrect command usage ", embed=embed)
    
                else:
                    accessors = bs.findAll('a', {'href': re.compile('\/statistics\/[A-Za-z]')})
    
                    # Season Information : ['PUBG',(season info),(Server),'overview']
                    seasonInfo = []
                    for si in bs.findAll('li', {'class': "active"}):
                        seasonInfo.append(si.text.strip())
                    serverAccessorAndStatus = []
                    # To prevent : Parsing Server Status, Make a result like Server:\nOnline. So I need to delete '\n'to get     good result
                    for a in accessors:
                        serverAccessorAndStatus.append(re.sub(pattern='[\n]', repl="", string=a.text.strip()))
    
                    # Varaible serverAccessorAndStatus : [(accessors),(ServerStatus),(Don't needed value)]
    
                    soloQueInfo = bs.find('section', {'class': "solo modeItem"}).find('div', {'class': "mode-section tpp"})
                    if soloQueInfo == None:
                        embed = discord.Embed(title="Record not found", description="Solo que record not found.",
                                              color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        await message.channel.send("PUBG player " + playerNickname + "'s TPP solo que information", embed=embed)
                    else:
                        # print(soloQueInfo)
                        # Get total playtime
                        soloQueTotalPlayTime = soloQueInfo.find('span', {'class': "time_played"}).text.strip()
                        # Get Win/Top10/Lose : [win,top10,lose]
                        soloQueGameWL = soloQueInfo.find('em').text.strip().split(' ')
                        # RankPoint
                        rankPoint = soloQueInfo.find('span', {'class': 'value'}).text
                        # Tier image url, tier
                        tierInfos = soloQueInfo.find('img', {
                            'src': re.compile('\/\/static\.dak\.gg\/images\/icons\/tier\/[A-Za-z0-9_.]')})
                        tierImage = "https:" + tierInfos['src']
                        print(tierImage)
                        tier = tierInfos['alt']
    
                        # Comprehensive info
                        comInfo = []
                        # [K/D,승률,Top10,평균딜량,게임수, 최다킬수,헤드샷,저격거리,생존,평균순위]
                        for ci in soloQueInfo.findAll('p', {'class': 'value'}):
                            comInfo.append(''.join(ci.text.split()))
    
                        embed = discord.Embed(title="Player Unkonw Battle Ground player search from dak.gg", description="",
                                              color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        embed.add_field(name="Real Time Accessors and Server Status",
                                        value="Accessors : " + serverAccessorAndStatus[0] + " | " "Server Status : " +
                                              serverAccessorAndStatus[1].split(':')[-1], inline=False)
                        embed.add_field(name="Player located server", value=seasonInfo[2] + " Server / Total playtime : "     +soloQueTotalPlayTime, inline=False)
                        embed.add_field(name="Tier",
                                        value=tier + " ("+rankPoint+"p)" , inline=False)
                        embed.add_field(name="K/D", value=comInfo[0], inline=True)
                        embed.add_field(name="승률", value=comInfo[1], inline=True)
                        embed.add_field(name="Top 10 비율", value=comInfo[2], inline=True)
                        embed.add_field(name="평균딜량", value=comInfo[3], inline=True)
                        embed.add_field(name="게임수", value=comInfo[4] + "판", inline=True)
                        embed.add_field(name="최다킬수", value=comInfo[5] + "킬", inline=True)
                        embed.add_field(name="헤드샷 비율", value=comInfo[6], inline=True)
                        embed.add_field(name="저격거리", value=comInfo[7], inline=True)
                        embed.add_field(name="평균생존시간", value=comInfo[8], inline=True)

                        await message.channel.send("PUBG player " + playerNickname + "'s TPP solo que information", embed=embed)
            except HTTPError as e:
                embed = discord.Embed(title="Not existing plyer", description="Can't find player " + playerNickname + "'s     information.\nPlease check player's nickname again",color=0x5CD1E5)
                await message.channel.send("Error : Not existing player", embed=embed)
            except AttributeError as e:
                embed = discord.Embed(title="Not existing plyer",
                                      description="Can't find player " + playerNickname + "'s information.\nPlease check     player's nickname again",
                                      color=0x5CD1E5)
                await message.channel.send("Error : Not existing player", embed=embed)
    
        if message.content.startswith("팔배그듀오"):
            baseURL = "https://dak.gg/profile/"
            playerNickname = ''.join((message.content).split(' ')[1:])
            URL = baseURL + quote(playerNickname)
            try:
                html = urlopen(URL)
                bs = BeautifulSoup(html, 'html.parser')
                if len(message.content.split(" ")) == 1:
                    embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x5CD1E5)
                    embed.add_field(name="Player nickname not entered",
                                    value="To use command 팔배그듀오 : 팔배그듀오 (Nickname)", inline=False)

                    await message.channel.send("Error : Incorrect command usage ", embed=embed)
    
                else:
                    accessors = bs.findAll('a', {'href': re.compile('\/statistics\/[A-Za-z]')})
    
                    # Season Information : ['PUBG',(season info),(Server),'overview']
                    seasonInfo = []
                    for si in bs.findAll('li', {'class': "active"}):
                        seasonInfo.append(si.text.strip())
                    serverAccessorAndStatus = []
                    # To prevent : Parsing Server Status, Make a result like Server:\nOnline. So I need to delete '\n'to get     good result
                    for a in accessors:
                        serverAccessorAndStatus.append(re.sub(pattern='[\n]', repl="", string=a.text.strip()))
    
                    # Varaible serverAccessorAndStatus : [(accessors),(ServerStatus),(Don't needed value)]
    
                    duoQueInfo = bs.find('section',{'class' : "duo modeItem"}).find('div',{'class' : "mode-section tpp"})
                    if duoQueInfo == None:
                        embed = discord.Embed(title="Record not found", description="Duo que record not found.",
                                              color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        await message.channel.send("PUBG player " + playerNickname + "'s TPP duo que information", embed=embed)
                    else:
                        # print(duoQueInfo)
                        # Get total playtime
                        duoQueTotalPlayTime = duoQueInfo.find('span', {'class': "time_played"}).text.strip()
                        # Get Win/Top10/Lose : [win,top10,lose]
                        duoQueGameWL = duoQueInfo.find('em').text.strip().split(' ')
                        # RankPoint
                        rankPoint = duoQueInfo.find('span', {'class': 'value'}).text
                        # Tier image url, tier
                        tierInfos = duoQueInfo.find('img', {
                            'src': re.compile('\/\/static\.dak\.gg\/images\/icons\/tier\/[A-Za-z0-9_.]')})
                        tierImage = "https:" + tierInfos['src']
                        tier = tierInfos['alt']
    
                        # Comprehensive info
                        comInfo = []
                        # [K/D,승률,Top10,평균딜량,게임수, 최다킬수,헤드샷,저격거리,생존,평균순위]
                        for ci in duoQueInfo.findAll('p', {'class': 'value'}):
                            comInfo.append(''.join(ci.text.split()))
    
                        embed = discord.Embed(title="Player Unkonw Battle Ground player search from dak.gg", description="",
                                              color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        embed.add_field(name="Real Time Accessors and Server Status",
                                        value="Accessors : " + serverAccessorAndStatus[0] + " | " "Server Status : " +
                                              serverAccessorAndStatus[1].split(':')[-1], inline=False)
                        embed.add_field(name="Player located server and total playtime", value=seasonInfo[2] + " Server / Total     playtime : " +duoQueTotalPlayTime, inline=False)
                        embed.add_field(name="Tier(Rank Point)",
                                        value=tier + " ("+rankPoint+"p)", inline=False)
                        embed.add_field(name="K/D", value=comInfo[0], inline=True)
                        embed.add_field(name="승률", value=comInfo[1], inline=True)
                        embed.add_field(name="Top 10 비율", value=comInfo[2], inline=True)
                        embed.add_field(name="평균딜량", value=comInfo[3], inline=True)
                        embed.add_field(name="게임수", value=comInfo[4] + "판", inline=True)
                        embed.add_field(name="최다킬수", value=comInfo[5] + "킬", inline=True)
                        embed.add_field(name="헤드샷 비율", value=comInfo[6], inline=True)
                        embed.add_field(name="저격거리", value=comInfo[7], inline=True)
                        embed.add_field(name="평균생존시간", value=comInfo[8], inline=True)

                        await message.channel.send("PUBG player " + playerNickname + "'s TPP duo que information", embed=embed)
            except HTTPError as e:
                embed = discord.Embed(title="Not existing plyer",
                                      description="Can't find player " + playerNickname + "'s information.\nPlease check     player's nickname again",
                                      color=0x5CD1E5)
                await message.channel.send("Error : Not existing player", embed=embed)
            except AttributeError as e:
                embed = discord.Embed(title="Not existing plyer",
                                      description="Can't find player " + playerNickname + "'s information.\nPlease check     player's nickname again",
                                      color=0x5CD1E5)
                await message.channel.send("Error : Not existing player", embed=embed)
    
        if message.content.startswith("팔배그스쿼드1"):
            baseURL = "https://dak.gg/profile/"
            playerNickname = ''.join((message.content).split(' ')[1:])
            URL = baseURL + quote(playerNickname)
            try:
                html = urlopen(URL)
                bs = BeautifulSoup(html, 'html.parser')
                if len(message.content.split(" ")) == 1:
                    embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x5CD1E5)
                    embed.add_field(name="Player nickname not entered",
                                    value="To use command 팔배그스쿼드 : 팔배그스쿼드 (Nickname)", inline=False)

                    await message.channel.send("Error : Incorrect command usage ", embed=embed)
    
                else:
                    accessors = bs.findAll('a', {'href': re.compile('\/statistics\/[A-Za-z]')})
    
                    # Season Information : ['PUBG',(season info),(Server),'overview']
                    seasonInfo = []
                    for si in bs.findAll('li', {'class': "active"}):
                        seasonInfo.append(si.text.strip())
                    serverAccessorAndStatus = []
                    # To prevent : Parsing Server Status, Make a result like Server:\nOnline. So I need to delete '\n'to get     good result
                    for a in accessors:
                        serverAccessorAndStatus.append(re.sub(pattern='[\n]', repl="", string=a.text.strip()))
    
                    # Varaible serverAccessorAndStatus : [(accessors),(ServerStatus),(Don't needed value)]
    
                    squadQueInfo = bs.find('section',{'class' : "squad modeItem"}).find('div',{'class' : "mode-section tpp"})
                    if squadQueInfo == None:
                        embed = discord.Embed(title="Record not found", description="Squad que record not found.",
                                              color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        await message.channel.send("PUBG player " + playerNickname + "'s TPP squad que information",     embed=embed)
                    else:
                        # print(duoQueInfo)
                        # Get total playtime
                        squadQueTotalPlayTime = squadQueInfo.find('span', {'class': "time_played"}).text.strip()
                        # Get Win/Top10/Lose : [win,top10,lose]
                        squadQueGameWL = squadQueInfo.find('em').text.strip().split(' ')
                        # RankPoint
                        rankPoint = squadQueInfo.find('span', {'class': 'value'}).text
                        # Tier image url, tier
                        tierInfos = squadQueInfo.find('img', {
                            'src': re.compile('\/\/static\.dak\.gg\/images\/icons\/tier\/[A-Za-z0-9_.]')})
                        tierImage = "https:" + tierInfos['src']
                        tier = tierInfos['alt']
    
                        # Comprehensive info
                        comInfo = []
                        # [K/D,승률,Top10,평균딜량,게임수, 최다킬수,헤드샷,저격거리,생존,평균순위]
                        for ci in squadQueInfo.findAll('p', {'class': 'value'}):
                            comInfo.append(''.join(ci.text.split()))
                        embed = discord.Embed(title="Player Unkonw Battle Ground player search from dak.gg", description="",
                                              color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        embed.add_field(name="Real Time Accessors and Server Status",
                                        value="Accessors : " + serverAccessorAndStatus[0] + " | " "Server Status : " +
                                              serverAccessorAndStatus[1].split(':')[-1], inline=False)
                        embed.add_field(name="Player located server", value=seasonInfo[2] + " Server / Total playtime : "     +squadQueTotalPlayTime, inline=False)
                        embed.add_field(name="Tier(Rank Point)",
                                        value=tier + " (" + rankPoint + "p)", inline=False)
                        embed.add_field(name="K/D", value=comInfo[0] , inline=True)
                        embed.add_field(name="승률", value=comInfo[1] , inline=True)
                        embed.add_field(name="Top 10 비율", value=comInfo[2] , inline=True)
                        embed.add_field(name="평균딜량", value=comInfo[3] , inline=True)
                        embed.add_field(name="게임수", value=comInfo[4] + "판", inline=True)
                        embed.add_field(name="최다킬수", value=comInfo[5] + "킬", inline=True)
                        embed.add_field(name="헤드샷 비율", value=comInfo[6], inline=True)
                        embed.add_field(name="저격거리", value=comInfo[7], inline=True)
                        embed.add_field(name="평균생존시간", value=comInfo[8], inline=True)

                        await message.channel.send("PUBG player " + playerNickname + "'s TPP squad que information",     embed=embed)
            except HTTPError as e:
                embed = discord.Embed(title="Not existing plyer",
                                      description="Can't find player " + playerNickname + "'s information.\nPlease check     player's nickname again",
                                      color=0x5CD1E5)
                await message.channel.send("Error : Not existing player", embed=embed)
            except AttributeError as e:
                embed = discord.Embed(title="Not existing plyer",
                                      description="Can't find player " + playerNickname + "'s information.\nPlease check     player's nickname again",
                                      color=0x5CD1E5)
                await message.channel.send("Error : Not existing player", embed=embed)
    
        if message.content.startswith("팔배그솔로2"):
            baseURL = "https://dak.gg/profile/"
            playerNickname = ''.join((message.content).split(' ')[1:])
            URL = baseURL + quote(playerNickname)
            try:
                html = urlopen(URL)
                bs = BeautifulSoup(html, 'html.parser')
                if len(message.content.split(" ")) == 1:
                    embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x5CD1E5)
                    embed.add_field(name="Player nickname not entered",
                                    value="To use command 팔배그솔로 : 팔배그솔로 (Nickname)", inline=False)

                    await message.channel.send("Error : Incorrect command usage ", embed=embed)
    
                else:
                    accessors = bs.findAll('a', {'href': re.compile('\/statistics\/[A-Za-z]')})
    
                    # Season Information : ['PUBG',(season info),(Server),'overview']
                    seasonInfo = []
                    for si in bs.findAll('li', {'class': "active"}):
                        seasonInfo.append(si.text.strip())
                    serverAccessorAndStatus = []
                    # To prevent : Parsing Server Status, Make a result like Server:\nOnline. So I need to delete '\n'to get     good result
                    for a in accessors:
                        serverAccessorAndStatus.append(re.sub(pattern='[\n]', repl="", string=a.text.strip()))
    
                    # Varaible serverAccessorAndStatus : [(accessors),(ServerStatus),(Don't needed value)]
    
                    soloQueInfo = bs.find('section', {'class': "solo modeItem"}).find('div', {'class': "mode-section fpp"})
                    if soloQueInfo == None:
                        embed = discord.Embed(title="Record not found", description="Solo que record not found.",
                                              color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        await message.channel.send("PUBG player " + playerNickname + "'s FPP solo que information",
                                                   embed=embed)
                    else:
                        # print(soloQueInfo)
                        # Get total playtime
                        soloQueTotalPlayTime = soloQueInfo.find('span', {'class': "time_played"}).text.strip()
                        # Get Win/Top10/Lose : [win,top10,lose]
                        soloQueGameWL = soloQueInfo.find('em').text.strip().split(' ')
                        # RankPoint
                        rankPoint = soloQueInfo.find('span', {'class': 'value'}).text
                        # Tier image url, tier
                        tierInfos = soloQueInfo.find('img', {
                            'src': re.compile('\/\/static\.dak\.gg\/images\/icons\/tier\/[A-Za-z0-9_.]')})
                        tierImage = "https:" + tierInfos['src']
                        print(tierImage)
                        tier = tierInfos['alt']
    
                        # Comprehensive info
                        comInfo = []
                        # [K/D,승률,Top10,평균딜량,게임수, 최다킬수,헤드샷,저격거리,생존,평균순위]
                        for ci in soloQueInfo.findAll('p', {'class': 'value'}):
                            comInfo.append(''.join(ci.text.split()))
                        embed = discord.Embed(title="Player Unkonw Battle Ground player search from dak.gg", description="",
                                              color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        embed.add_field(name="Real Time Accessors and Server Status",
                                        value="Accessors : " + serverAccessorAndStatus[0] + " | " "Server Status : " +
                                              serverAccessorAndStatus[1].split(':')[-1], inline=False)
                        embed.add_field(name="Player located server",
                                        value=seasonInfo[2] + " Server / Total playtime : " + soloQueTotalPlayTime,
                                        inline=False)
                        embed.add_field(name="Tier(Rank Point)",
                                        value=tier + " (" + rankPoint + "p)", inline=False)
                        embed.add_field(name="K/D", value=comInfo[0], inline=True)
                        embed.add_field(name="승률", value=comInfo[1], inline=True)
                        embed.add_field(name="Top 10 비율", value=comInfo[2], inline=True)
                        embed.add_field(name="평균딜량", value=comInfo[3], inline=True)
                        embed.add_field(name="게임수", value=comInfo[4] + "판" , inline=True)
                        embed.add_field(name="최다킬수", value=comInfo[5] + "킬" , inline=True)
                        embed.add_field(name="헤드샷 비율", value=comInfo[6] , inline=True)
                        embed.add_field(name="저격거리", value=comInfo[7], inline=True)
                        embed.add_field(name="평균생존시간", value=comInfo[8] , inline=True)

                        await message.channel.send("PUBG player " + playerNickname + "'s FPP solo que information",
                                                   embed=embed)
            except HTTPError as e:
                embed = discord.Embed(title="Not existing plyer",
                                      description="Can't find player " + playerNickname + "'s information.\nPlease check     player's nickname again",
                                      color=0x5CD1E5)
                await message.channel.send("Error : Not existing player", embed=embed)
            except AttributeError as e:
                embed = discord.Embed(title="Not existing plyer",
                                      description="Can't find player " + playerNickname + "'s information.\nPlease check     player's nickname again",
                                      color=0x5CD1E5)
                await message.channel.send("Error : Not existing player", embed=embed)
    
        if message.content.startswith("팔배그듀오2"):
            baseURL = "https://dak.gg/profile/"
            playerNickname = ''.join((message.content).split(' ')[1:])
            URL = baseURL + quote(playerNickname)
            try:
                html = urlopen(URL)
                bs = BeautifulSoup(html, 'html.parser')
                if len(message.content.split(" ")) == 1:
                    embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x5CD1E5)
                    embed.add_field(name="Player nickname not entered",
                                    value="To use command 팔배그듀오 : 팔배그듀오2 (Nickname)", inline=False)

                    await message.channel.send("Error : Incorrect command usage ", embed=embed)
    
                else:
                    accessors = bs.findAll('a', {'href': re.compile('\/statistics\/[A-Za-z]')})
    
                    # Season Information : ['PUBG',(season info),(Server),'overview']
                    seasonInfo = []
                    for si in bs.findAll('li', {'class': "active"}):
                        seasonInfo.append(si.text.strip())
                    serverAccessorAndStatus = []
                    # To prevent : Parsing Server Status, Make a result like Server:\nOnline. So I need to delete '\n'to get     good result
                    for a in accessors:
                        serverAccessorAndStatus.append(re.sub(pattern='[\n]', repl="", string=a.text.strip()))
    
                    # Varaible serverAccessorAndStatus : [(accessors),(ServerStatus),(Don't needed value)]
    
                    duoQueInfo = bs.find('section', {'class': "duo modeItem"}).find('div', {'class': "mode-section fpp"})
                    if duoQueInfo == None:
                        embed = discord.Embed(title="Record not found", description="Duo que record not found.",
                                              color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        await message.channel.send("PUBG player " + playerNickname + "'s FPP duo que information",
                                                   embed=embed)
                    else:
                        # print(duoQueInfo)
                        # Get total playtime
                        duoQueTotalPlayTime = duoQueInfo.find('span', {'class': "time_played"}).text.strip()
                        # Get Win/Top10/Lose : [win,top10,lose]
                        duoQueGameWL = duoQueInfo.find('em').text.strip().split(' ')
                        # RankPoint
                        rankPoint = duoQueInfo.find('span', {'class': 'value'}).text
                        # Tier image url, tier
                        tierInfos = duoQueInfo.find('img', {
                            'src': re.compile('\/\/static\.dak\.gg\/images\/icons\/tier\/[A-Za-z0-9_.]')})
                        tierImage = "https:" + tierInfos['src']
                        tier = tierInfos['alt']
    
                        # Comprehensive info
                        comInfo = []
                        # [K/D,승률,Top10,평균딜량,게임수, 최다킬수,헤드샷,저격거리,생존,평균순위]
                        for ci in duoQueInfo.findAll('p', {'class': 'value'}):
                            comInfo.append(''.join(ci.text.split()))
                        embed = discord.Embed(title="Player Unkonw Battle Ground player search from dak.gg", description="",
                                              color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        embed.add_field(name="Real Time Accessors and Server Status",
                                        value="Accessors : " + serverAccessorAndStatus[0] + " | " "Server Status : " +
                                              serverAccessorAndStatus[1].split(':')[-1], inline=False)
                        embed.add_field(name="Player located server and total playtime",
                                        value=seasonInfo[2] + " Server / Total playtime : " + duoQueTotalPlayTime,
                                        inline=False)
                        embed.add_field(name="Tier(Rank Point)",
                                        value=tier + " (" + rankPoint + "p)", inline=False)
                        embed.add_field(name="K/D", value=comInfo[0] , inline=True)
                        embed.add_field(name="승률", value=comInfo[1], inline=True)
                        embed.add_field(name="Top 10 비율", value=comInfo[2], inline=True)
                        embed.add_field(name="평균딜량", value=comInfo[3], inline=True)
                        embed.add_field(name="게임수", value=comInfo[4] + "판", inline=True)
                        embed.add_field(name="최다킬수", value=comInfo[5] + "킬", inline=True)
                        embed.add_field(name="헤드샷 비율", value=comInfo[6] , inline=True)
                        embed.add_field(name="저격거리", value=comInfo[7] , inline=True)
                        embed.add_field(name="평균생존시간", value=comInfo[8] , inline=True)

                        await message.channel.send("PUBG player " + playerNickname + "'s FPP duo que information",
                                                   embed=embed)
            except HTTPError as e:
                embed = discord.Embed(title="Not existing plyer",
                                      description="Can't find player " + playerNickname + "'s information.\nPlease check     player's nickname again",
                                      color=0x5CD1E5)
                await message.channel.send("Error : Not existing player", embed=embed)
            except AttributeError as e:
                embed = discord.Embed(title="Not existing plyer",
                                      description="Can't find player " + playerNickname + "'s information.\nPlease check     player's nickname again",
                                      color=0x5CD1E5)
                await message.channel.send("Error : Not existing player", embed=embed)
    
        if message.content.startswith("팔배그스쿼드2"):
            baseURL = "https://dak.gg/profile/"
            playerNickname = ''.join((message.content).split(' ')[1:])
            URL = baseURL + quote(playerNickname)
            try:
                html = urlopen(URL)
                bs = BeautifulSoup(html, 'html.parser')
                if len(message.content.split(" ")) == 1:
                    embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x5CD1E5)
                    embed.add_field(name="Player nickname not entered",
                                    value="To use command 팔배그스쿼드 : 팔배그스쿼드2 (Nickname)", inline=False)

                    await message.channel.send("Error : Incorrect command usage ", embed=embed)
    
                else:
                    accessors = bs.findAll('a', {'href': re.compile('\/statistics\/[A-Za-z]')})
    
                    # Season Information : ['PUBG',(season info),(Server),'overview']
                    seasonInfo = []
                    for si in bs.findAll('li', {'class': "active"}):
                        seasonInfo.append(si.text.strip())
                    serverAccessorAndStatus = []
                    # To prevent : Parsing Server Status, Make a result like Server:\nOnline. So I need to delete '\n'to get     good result
                    for a in accessors:
                        serverAccessorAndStatus.append(re.sub(pattern='[\n]', repl="", string=a.text.strip()))
    
                    # Varaible serverAccessorAndStatus : [(accessors),(ServerStatus),(Don't needed value)]
    
                    squadQueInfo = bs.find('section', {'class': "squad modeItem"}).find('div',
                                                                                        {'class': "mode-section fpp"})
                    if squadQueInfo == None:
                        embed = discord.Embed(title="Record not found", description="Squad que record not found.",
                                              color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        await message.channel.send("PUBG player " + playerNickname + "'s FPP squad que information",
                                                   embed=embed)
                    else:
                        # print(duoQueInfo)
                        # Get total playtime
                        squadQueTotalPlayTime = squadQueInfo.find('span', {'class': "time_played"}).text.strip()
                        # Get Win/Top10/Lose : [win,top10,lose]
                        squadQueGameWL = squadQueInfo.find('em').text.strip().split(' ')
                        # RankPoint
                        rankPoint = squadQueInfo.find('span', {'class': 'value'}).text
                        # Tier image url, tier
                        tierInfos = squadQueInfo.find('img', {
                            'src': re.compile('\/\/static\.dak\.gg\/images\/icons\/tier\/[A-Za-z0-9_.]')})
                        tierImage = "https:" + tierInfos['src']
                        tier = tierInfos['alt']
    
                        # Comprehensive info
                        comInfo = []
                        # [K/D,승률,Top10,평균딜량,게임수, 최다킬수,헤드샷,저격거리,생존,평균순위]
                        for ci in squadQueInfo.findAll('p', {'class': 'value'}):
                            comInfo.append(''.join(ci.text.split()))
                        embed = discord.Embed(title="Player Unkonw Battle Ground player search from dak.gg", description="",
                                              color=0x5CD1E5)
                        embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                        embed.add_field(name="Real Time Accessors and Server Status",
                                        value="Accessors : " + serverAccessorAndStatus[0] + " | " "Server Status : " +
                                              serverAccessorAndStatus[1].split(':')[-1], inline=False)
                        embed.add_field(name="Player located server",
                                        value=seasonInfo[2] + " Server / Total playtime : " + squadQueTotalPlayTime,
                                        inline=False)
                        embed.add_field(name="Tier(Rank Point)",
                                        value=tier + " (" + rankPoint + "p)", inline=False)
                        embed.add_field(name="K/D", value=comInfo[0], inline=True)
                        embed.add_field(name="승률", value=comInfo[1], inline=True)
                        embed.add_field(name="Top 10 비율", value=comInfo[2], inline=True)
                        embed.add_field(name="평균딜량", value=comInfo[3], inline=True)
                        embed.add_field(name="게임수", value=comInfo[4] + "판", inline=True)
                        embed.add_field(name="최다킬수", value=comInfo[5] + "킬", inline=True)
                        embed.add_field(name="헤드샷 비율", value=comInfo[6] , inline=True)
                        embed.add_field(name="저격거리", value=comInfo[7], inline=True)
                        embed.add_field(name="평균생존시간", value=comInfo[8], inline=True)

                        await message.channel.send("PUBG player " + playerNickname + "'s FPP squad que information",
                                                   embed=embed)
            except HTTPError as e:
                embed = discord.Embed(title="Not existing plyer",
                                      description="Can't find player " + playerNickname + "'s information.\nPlease check     player's nickname again",
                                      color=0x5CD1E5)
                await message.channel.send("Error : Not existing player", embed=embed)
            except AttributeError as e:
                embed = discord.Embed(title="Not existing plyer",
                                      description="Can't find player " + playerNickname + "'s information.\nPlease check     player's nickname again",
                                      color=0x5CD1E5)
                await message.channel.send("Error : Not existing player", embed=embed)
        
def setup(bot):
    bot.add_cog(pubg(bot))    