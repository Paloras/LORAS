# To make a discord bot you need to download discord.py with pip
#-*- coding: utf-8 -*-
import random
import discord
import json
import random
import os
import shutil
from discord.ext import commands
import asyncio

class game(commands.Cog):

    def __init__(self, bot):
        """Initialisation bot"""
        self.bot = bot

    # @commands.command(aliases=['운세'])
    # @commands.cooldown(1, 2, commands.BucketType.user)
    # async def _8ball(self, ctx, *, question):
    #     """8-ball game"""
    #     responses = [ "확실하다 ",
    #                  "정말입니다 ",
    #                  "의심의 여지없이",
    #                  "예 — 확실히",
    #                  "당신은 그것에 의지 할 수 있습니다 ",
    #                  "알다시피, 네 ",
    #                  "아마도 ",
    #                  "전망 좋은 ",
    #                  "표지판 예",
    #                  "예 ",
    #                  "흐리게 답하기, 다시 시도하십시오",
    #                  "나중에 다시 질문",
    #                  "더 이상 말하지 말라",
    #                  "지금 예측할 수 없습니다",
    #                  "집중하고 다시 묻습니다",
    #                  "믿지 마라",
    #                  "제 답장이 없습니다",
    #                  "내 응답은 아니오입니다",
    #                  "전망이 좋지 않다",
    #                  "아주 의심 스럽다"]
    #     await ctx.send(f'질문: {question}\n답: {random.choice(responses)}')

    @commands.command(aliases=['뭔겜할까', '무슨게임','뭔겜'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def WhatByGame(self, ctx):
        """Function for choice game"""
        responses = ["포트나이트", "카운터 스트라이크(카스)", "GTA5", "배틀그라운드(배그)", "러스트", "RDR2", "어쌔신크리드", "콜 오브 듀티", "리그 오브 레전드(롤)", "마인크래프트"]
        await ctx.send(f'{random.choice(responses)}을(를) 플레이해!')
    @WhatByGame.error
    async def WhatByGame_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(aliases=['랜덤게임', '랜덤'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def RandomGame(self, ctx, *, games):
        """Random choice game"""
        await ctx.send(f'{random.choice(games.split())}')
    @RandomGame.error
    async def RandomGame_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')
    
    @commands.command(name="동전")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def coin(self, ctx):
        randomlist = ["앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "옆면?"]
        ran = random.choice(randomlist)
        if ran == "옆면?":
            author_id = str(ctx.author.id)
            with open(f'game/money.json', 'r') as f:
                money = json.load(f)
            try:
                got_money = 500000
                money[author_id]['money'] += got_money
                with open(f'game/money.json', 'w') as s:
                    json.dump(money, s, indent=4)
                with open(f'game/money.json', 'r') as f:
                    money = json.load(f)
                embed1 = discord.Embed(title="결과", description="어이쿠 실수로 던졌다~ "+ran, color=0xb8bb6a)
                await ctx.send(embed=embed1)

                await ctx.send(f'이스터에그를 찾아서 포상금이 주어집니다. ({got_money}원)')
                embed = discord.Embed(title='통장', description=f'{ctx.author}', color=ctx.author.color)
                embed.set_thumbnail(url=ctx.author.avatar_url)

                embed.add_field(name="계좌번호", value=f'{ctx.author.id}')
                embed.add_field(name="잔액", value=f'{money[author_id]["money"]}원', inline=False)

                await ctx.send(embed=embed)

            except KeyError:
                got_money = 500000
                author_id = str(ctx.author.id)
                with open(f'game/money.json', 'r') as f:
                    money = json.load(f)
                money[author_id] = {}
                money[author_id]['money'] = got_money
                with open(f'game/money.json', 'w') as s:
                    json.dump(money, s, indent=4)
                await ctx.send(f'계정이 없어서 계정을 생성하였습니다. 통장 잔고는 {got_money}원 입니다.')
            return
        else:
            embed = discord.Embed(title="결과", description="어이쿠 실수로 던졌다~ "+ran, color=0xb8bb6a)
            await ctx.send(embed=embed)
    @coin.error
    async def coin_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:5s:752150489390645269>')

    @commands.command(name="주사위")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def dice(self, ctx):
        random = ["1", "2", "3", "4", "5", "6"]
        ran = random.randint(random)
        embed = discord.Embed(title="결과", description=ran, color=0xb8bb6a)
        await ctx.send(embed=embed)
    @dice.error
    async def dice_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(name="계정생성")
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def createaccount(self, ctx):
        guild_id = str(ctx.guild.id)
        author_id = str(ctx.author.id)
        with open(f'game/money.json', 'r') as f:
            money = json.load(f)
        money[author_id] = {}
        money[author_id]['money'] = 0
        money[author_id]['username'] = str(ctx.author)
        with open(f'game/money.json', 'w') as s:
            json.dump(money, s, indent=4)
        await ctx.send('계정이 생성되었습니다. 통장 잔고는 0원 입니다.')
    @createaccount.error
    async def createaccount_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:10min:752150489096781966>')

    @commands.command(name="일", aliases=['일하기'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def work(self, ctx):
        guild_id = str(ctx.guild.id)
        author_id = str(ctx.author.id)
        with open(f'game/money.json', 'r') as f:
            money = json.load(f)
        try:
            got_money = random.randint(1000, 10000)
            money[author_id]['money'] += got_money
            with open(f'game/money.json', 'w') as s:
                json.dump(money, s, indent=4)
            await ctx.send(f'{got_money}원을 일하여 얻었다. (현재잔액:{money[author_id]["money"]})')
        except KeyError:
            guild_id = str(ctx.guild.id)
            author_id = str(ctx.author.id)
            with open(f'game/money.json', 'r') as f:
                money = json.load(f)
            money[author_id] = {}
            money[author_id]['money'] = 0
            with open(f'game/money.json', 'w') as s:
                json.dump(money, s, indent=4)
            await ctx.send('계정이 없어서 계정을 생성하였습니다. 통장 잔고는 0원 입니다.')
            return
    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:3s:752150489344507955>')


    @commands.command(name="도박")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gamble(self, ctx, 판돈:int):
        author_id = str(ctx.author.id)
        if 판돈 == 0:
            await ctx.send('1원 이상으로 입력해주세요.')
            return
        with open(f'game/money.json', 'r') as f:
            money = json.load(f)
        try:
            if 판돈 > money[author_id]['money']:
                await ctx.send('돈이 부족합니다.')
                return
            money[author_id]['money'] -= 판돈
            result = random.randint(1, 100)
            if result > 70:
                await ctx.send('도박에 성공했습니다. 2배의 돈을 벌었습니다.')
                money[author_id]['money'] += 판돈 * 2
            elif result <= 70 and result >10:
                await ctx.send('배팅에 실패했습니다. 돈을 잃었습니다.')
            elif result <= 10 and result > 2:
                await ctx.send('도박에 성공했습니다. 3배의 돈을 벌었습니다.')
                money[author_id]['money'] += 판돈 * 3
            elif result <= 2:
                await ctx.send('원금은 회수하셨네요... 배팅금만큼의 돈을 얻었습니다.')
                money[author_id]['money'] += 판돈
            else:
                await ctx.send('배팅에 실패했습니다. 돈을 잃었습니다.')
            with open(f'game/money.json', 'w') as s:
                json.dump(money, s, indent=4)
        except KeyError:
            guild_id = str(ctx.guild.id)
            author_id = str(ctx.author.id)
            with open(f'game/money.json', 'r') as f:
                money = json.load(f)
            money[author_id] = {}
            money[author_id]['money'] = 0
            with open(f'game/money.json', 'w') as s:
                json.dump(money, s, indent=4)
            await ctx.send('계정이 없어서 계정을 생성하였습니다. 통장 잔고는 0원 입니다.')
            return
    @gamble.error
    async def gamble_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:5s:752150489390645269>')
            
    @commands.command(name="통장")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def account(self, ctx):
        author_id = str(ctx.author.id)
        try:
            with open(f'game/money.json', 'r') as f:
                money = json.load(f)
            embed = discord.Embed(title='통장', description=f'{ctx.author}', color=ctx.author.color)
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.add_field(name="계좌번호", value=f'{ctx.author.id}')
            embed.add_field(name="잔액", value=f'{money[author_id]["money"]}원', inline=False)
            await ctx.send(embed=embed)

        except KeyError:
            guild_id = str(ctx.guild.id)
            author_id = str(ctx.author.id)
            with open(f'game/money.json', 'r') as f:
                money = json.load(f)
            money[author_id] = {}
            money[author_id]['money'] = 0
            with open(f'game/money.json', 'w') as s:
                json.dump(money, s, indent=4)
            await ctx.send('계정이 없어서 계정을 생성하였습니다. 통장 잔고는 0원 입니다.')
            return
    @account.error
    async def account_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:15s:752150489386450974>')
    
    @commands.command(name="계좌번호확인", aliases=['계좌확인', '계좌'], help="현재시간을 알려줍니다")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def dadafasfafwscfasewsdcfsasc(self,ctx, user_name: discord.Member):
        await ctx.send(user_name.id)
    @dadafasfafwscfasewsdcfsasc.error
    async def dadafasfafwscfasewsdcfsasc_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(name="송금")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def sendmoney(self, ctx, 계좌번호, amount:int):
        sss = amount
        amount = int(amount*0.8)
        author_id = str(ctx.author.id)
        xaxa = int(amount*0.2)
        with open(f'game/money.json', 'r') as f:
            money = json.load(f)
        try:
            with open(f'game/money.json', 'r') as f:
                money = json.load(f)
            if sss+1000 > money[author_id]['money']:
                await ctx.send('돈이 부족합니다.')
                return
            try:
                money[author_id]['money'] -= (sss + 1000)
                money[계좌번호]['money'] += amount
            except KeyError:
                await ctx.send('계좌번호가 존재하지 않습니다.')
            await ctx.send(f'정상적으로 송금했습니다. 수수료 {xaxa}')
            with open(f'game/money.json', 'w') as s:
                json.dump(money, s, indent=4)
        except KeyError:
            guild_id = str(ctx.guild.id)
            author_id = str(ctx.author.id)
            with open(f'game/money.json', 'r') as f:
                money = json.load(f)
            money[author_id] = {}
            money[author_id]['money'] = 0
            with open(f'game/money.json', 'w') as s:
                json.dump(money, s, indent=4)
            await ctx.send('계정이 없어서 계정을 생성하였습니다. 통장 잔고는 0원 입니다.')
            return
    @sendmoney.error
    async def sendmoney_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:1h:752150489776390277>')

    @commands.command(name="계정삭제")
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def deleteaccount(self, ctx):
        author_id = str(ctx.author.id)
        try:
            with open(f'game/money.json', 'r') as f:
                money = json.load(f)
            del money[author_id]
            with open(f'game/money.json', 'w') as s:
                json.dump(money, s, indent=4)
        except KeyError:
            guild_id = str(ctx.guild.id)
            author_id = str(ctx.author.id)
            with open(f'game/money.json', 'r') as f:
                money = json.load(f)
            money[author_id] = {}
            money[author_id]['money'] = 0
            with open(f'game/money.json', 'w') as s:
                json.dump(money, s, indent=4)
            await ctx.send('계정이 없어서 계정을 생성하였습니다. 통장 잔고는 0원 입니다.')
            return
        await ctx.send('당신의 계정이 삭제되었습니다.')
    @deleteaccount.error
    async def deleteaccount_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:10min:752150489096781966>')

    @commands.command()
    async def 가위바위보(self, ctx):
        user_id = str(ctx.author.id)
        with open("game/money.json", 'r') as f:
            user_data = json.load(f)  # 유저 데이터 불러오는 코드
        await ctx.send("`가위, 바위, 보` 중에서 하나를 5초 안에 말해주세요!")
        try:
            a = user_data[user_id]
        except KeyError:
            await ctx.send('계정을 먼저 생성해주세요.')
            return

        rpc = ['가위', '바위', '보']

        def check(m):
            return m.content == "가위" or m.content == "바위" or m.content == "보"

        def game(A, B):
            if A not in rpc:
                return
            if A == rpc[0] and B == rpc[2] or A == rpc[1] and B == rpc[0] or A == rpc[2] and B == rpc[1]:
                return 1
            elif A == B:
                return 2
            elif A == rpc[0] and B == rpc[1] or A == rpc[1] and B == rpc[2] or A == rpc[2] and B == rpc[0]:
                return 3

        try:
            answer = await self.bot.wait_for("message", timeout=5, check=check)
        except asyncio.TimeoutError:
            await ctx.send("시간이 초과됬어요...")
            return

        choice = random.choice(rpc)
        result = game(answer.content, choice)
        if result == 1:
            await ctx.send(f"{ctx.author.mention}님이 이겼어요... ({answer.content}, {choice})\n`+100원`")
            user_data[user_id]["money"] += 100
        elif result == 3:
            await ctx.send(f"제가 이겼어요! ({answer.content}, {choice})")
        elif result == 2:
            await ctx.send(f"비겼네요. ({answer.content}, {choice})\n`+50원`")
            user_data[user_id]["money"] += 50
        with open("game/money.json", 'w') as f:
            json.dump(user_data, f, indent=4)

def setup(bot):
    bot.add_cog(game(bot))