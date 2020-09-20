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
from config import OWNERS

class game(commands.Cog):

    def __init__(self, bot):
        """Initialisation bot"""
        self.bot = bot

    @commands.command(name="동전", aliases=['ehdwjs','coin','채ㅑㅜ'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def coin(self, ctx):
        randomlist = ["앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "앞면", "뒷면", "옆면?"]
        ran = random.choice(randomlist)
        guild_id = str(ctx.guild.id)
        author_id = str(ctx.author.id)
        with open(f'game/money.json', 'r') as f:
            money = json.load(f)
        if 3000 > money[author_id]['money']:
            await ctx.send('돈이 부족합니다.')
            return
        money[author_id]['money'] -= 3000
        with open(f'game/money.json', 'w') as s:
            json.dump(money, s, indent=4)
        await ctx.send(f'동전을 던지고 버렸다. -3000원 (현재잔액:{money[author_id]["money"]})')
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
                cha = self.bot.get_channel(11111111111111)

                embed2 = discord.Embed(title='이스터에그 발*견', description=f'태그번호`{ctx.author.discriminator}`님이 이스터에그를 발견하셨습니다.', color=ctx.author.color)
                await cha.send(embed=embed2)

            except KeyError:
                got_money = 500000
                author_id = str(ctx.author.id)
                with open(f'game/money.json', 'r') as f:
                    money = json.load(f)
                money[author_id] = {}
                money[author_id]['money'] = got_money
                with open(f'game/money.json', 'w') as s:
                    json.dump(money, s, indent=4)
                await ctx.send(f'이스터에그를 찾아서 포상금이 주어집니다. ({got_money}원)')
                await ctx.send(f'계정이 없어서 계정을 생성하였습니다. 통장 잔고는 {got_money}원 입니다.')
                cha = self.bot.get_channel(11111111111111)

                embed2 = discord.Embed(title='이스터에그 발*견', description=f'태그번호`{ctx.author.discriminator}`님이 이스터에그를 발견하셨습니다.', color=ctx.author.color)
                await cha.send(embed=embed2)
            return
        else:
            embed = discord.Embed(title="결과", description="어이쿠 실수로 던졌다~ "+ran, color=0xb8bb6a)
            await ctx.send(embed=embed)
    @coin.error
    async def coin_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:.5s:752150489390645269>')


    @commands.command(name="계정생성",aliases=['rPwjdtodtjd'])
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def createaccount(self, ctx):
        guild_id = str(ctx.guild.id)
        author_id = str(ctx.author.id)
        with open(f'game/money.json', 'r') as f:
            money = json.load(f)
        money[author_id] = {}
        money[author_id]['money'] = 0
        money[author_id]['work'] = 0
        with open(f'game/money.json', 'w') as s:
            json.dump(money, s, indent=4)
        await ctx.send('계정이 생성되었습니다. 통장 잔고는 0원 입니다.')
    @createaccount.error
    async def createaccount_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<.10min:752150489096781966>')

    @commands.command(name="일", aliases=['일하기','dlf','dlfgkrl'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def work(self, ctx):
        author_id = str(ctx.author.id)
        with open(f'game/money.json', 'r') as f:
            money = json.load(f)
        try:
            firstlose = random.randint(1, 5000)
            second = random.randint(1, 15000)
            fff = firstlose - second
            ff = second - firstlose

            got_money = random.randint(1, 20000)
            lose_money = random.randint(1, 17000)
            mmm = got_money - lose_money
            mm = lose_money - got_money
            if money[author_id]['money'] <= 100000:
                money[author_id]['money'] += firstlose
                money[author_id]['work'] += 1
                with open(f'game/money.json', 'w') as s:
                    json.dump(money, s, indent=4)
                await ctx.send(f'{firstlose}원을 일하여 얻었다. ({ctx.author.name}#{ctx.author.discriminator}님의 현재잔액:{money[author_id]["money"]})')
            elif money[author_id]['money'] <= 500000 and money[author_id]['money'] > 100000:
                if fff > 0:
                    money[author_id]['money'] -= fff
                    money[author_id]['work'] += 1
                    with open(f'game/money.json', 'w') as s:
                        json.dump(money, s, indent=4)
                    await ctx.send(f'일하다가 큰부상을 입어 {fff}원을 병원비로 지출하게되었다. ({ctx.author.name}#{ctx.author.discriminator}님의 현재잔액:{money[author_id]["money"]})')
                elif ff > 0:
                    money[author_id]['money'] += ff
                    money[author_id]['work'] += 1
                    with open(f'game/money.json', 'w') as s:
                        json.dump(money, s, indent=4)
                    await ctx.send(f'{ff}원을 일하여 얻었다. ({ctx.author.name}#{ctx.author.discriminator}님의 현재잔액:{money[author_id]["money"]})')
                elif ff == 0 and fff == 0:
                    money[author_id]['work'] += 1
                    with open(f'game/money.json', 'w') as s:
                        json.dump(money, s, indent=4)
                    await ctx.send(f"{ctx.author.name}#{ctx.author.discriminator}님은 열심히 일을 하였지만 사고로 인해 돈이 나가서 번돈이 없다")
                
            elif money[author_id]['money'] > 500000:
                if mm > 0:
                    money[author_id]['money'] -= mm
                    money[author_id]['work'] += 1
                    with open(f'game/money.json', 'w') as s:
                        json.dump(money, s, indent=4)
                    await ctx.send(f'일하다가 큰부상을 입어 {mm}원을 병원비로 지출하게되었다. ({ctx.author.name}#{ctx.author.discriminator}님의 현재잔액:{money[author_id]["money"]})')
                elif mmm > 0:
                    money[author_id]['money'] += mmm
                    money[author_id]['work'] += 1
                    with open(f'game/money.json', 'w') as s:
                        json.dump(money, s, indent=4)
                    await ctx.send(f'{mmm}원을 일하여 얻었다. ({ctx.author.name}#{ctx.author.discriminator}님의 현재잔액:{money[author_id]["money"]})')
                elif mm == 0 and mmm == 0:
                    money[author_id]['work'] += 1
                    with open(f'game/money.json', 'w') as s:
                        json.dump(money, s, indent=4)
                    await ctx.send(f"{ctx.author.name}#{ctx.author.discriminator}님은 열심히 일을 하였지만 사고로 인해 돈이 나가서 번돈이 없다")
        except KeyError:
            guild_id = str(ctx.guild.id)
            author_id = str(ctx.author.id)
            with open(f'game/money.json', 'r') as f:
                money = json.load(f)
            money[author_id] = {}
            money[author_id]['money'] = 0
            money[author_id]['work'] = 0
            with open(f'game/money.json', 'w') as s:
                json.dump(money, s, indent=4)
            await ctx.send(f'{ctx.author.name}#{ctx.author.discriminator}님의 계정이 없어서 계정을 생성하였습니다. 통장 잔고는 0원 입니다.')
            return
    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:3s:752150489344507955>')


    @commands.command(name="도박",aliases=['gamble','ehqkr'])
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
            result = random.randint(1, 10000)
            if result > 7000:
                await ctx.send(f'{ctx.author.name}#{ctx.author.discriminator}님의 도박에 성공했습니다. 2배의 돈을 벌었습니다.')
                money[author_id]['money'] += 판돈 * 2
            elif result <= 7000 and result >1000:
                await ctx.send(f'{ctx.author.name}#{ctx.author.discriminator}님의 배팅에 실패했습니다. 돈을 잃었습니다.')
            elif result <= 1000 and result > 80:
                await ctx.send(f'{ctx.author.name}#{ctx.author.discriminator}님의 원금은 회수하셨네요... 배팅금만큼의 돈을 얻었습니다.')
                money[author_id]['money'] += 판돈
            elif result <= 80 and result > 10:
                await ctx.send(f'{ctx.author.name}#{ctx.author.discriminator}님의 도박에 성공했습니다. 3배의 돈을 벌었습니다.')
                money[author_id]['money'] += 판돈 * 3
            elif result <= 10 and result > 2:
                await ctx.send(f'{ctx.author.name}#{ctx.author.discriminator}님의 배팅에 실패했습니다. 돈을 잃었습니다.')
            elif result <= 2:
                await ctx.send(f'{ctx.author.name}#{ctx.author.discriminator}님의 도박에 성공했습니다. 5배의 돈을 벌었습니다.')
                money[author_id]['money'] += 판돈*5+100000
                cha = self.bot.get_channel(11111111111111)

                embed1 = discord.Embed(title='도박!', description=f'태그번호`{ctx.author.discriminator}`님이 이스터에그를 발견하셨습니다.', color=ctx.author.color)
                await cha.send(embed=embed1)

                embed2 = discord.Embed(title='이스터에그 발*견', description=f'당신은 이스터에그를 발견하여 사례금 10만원을 드립니다.', color=ctx.author.color)
                embed2.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed=embed2)
            else:
                await ctx.send(f'{ctx.author.name}#{ctx.author.discriminator}님의 배팅에 실패했습니다. 돈을 잃었습니다.')
            with open(f'game/money.json', 'w') as s:
                json.dump(money, s, indent=4)
        except KeyError:
            guild_id = str(ctx.guild.id)
            author_id = str(ctx.author.id)
            with open(f'game/money.json', 'r') as f:
                money = json.load(f)
            money[author_id] = {}
            money[author_id]['money'] = 0
            money[author_id]['work'] = 0
            with open(f'game/money.json', 'w') as s:
                json.dump(money, s, indent=4)
            await ctx.send('계정이 없어서 계정을 생성하였습니다. 통장 잔고는 0원 입니다.')
            return
    @gamble.error
    async def gamble_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:5s:752150489390645269>')
            
    @commands.command(name="통장",aliases=['xhdwkd','account','ㅁㅊ채ㅕㅜㅅ'])
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
            money[author_id]['work'] = 0
            with open(f'game/money.json', 'w') as s:
                json.dump(money, s, indent=4)
            await ctx.send('계정이 없어서 계정을 생성하였습니다. 통장 잔고는 0원 입니다.')
            return
    @account.error
    async def account_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:.15s:752150489386450974>')
    
    @commands.command(name="계좌번호확인", aliases=['계좌확인', '계좌','rPwhk','rPwhkghkrdls','rPwhkqjsghghkrdls'], help="현재시간을 알려줍니다")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def dadafasfafwscfasewsdcfsasc(self,ctx,*, user_name: discord.Member):
        await ctx.send(f"{user_name.name}#{user_name.discriminator}님의 계좌번호는 `{user_name.id}` 입니다.")
    @dadafasfafwscfasewsdcfsasc.error
    async def dadafasfafwscfasewsdcfsasc_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(name="송금",aliases=['thdrma','ㄴ둥','send'])
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def sendmoney(self, ctx, 계좌번호, amount:int):
        sss = amount
        xx = int(amount*0.8)
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
                money[계좌번호]['money'] += xx
            except KeyError:
                await ctx.send('계좌번호가 존재하지 않습니다.')
                return
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
            money[author_id]['work'] = 0
            with open(f'game/money.json', 'w') as s:
                json.dump(money, s, indent=4)
            await ctx.send('계정이 없어서 계정을 생성하였습니다. 통장 잔고는 0원 입니다.')
            return
    @sendmoney.error
    async def sendmoney_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:.1h:752150489776390277>')

    @commands.command(name="계정삭제",aliases=['deleteaccount','rPwjdtkrwp'])
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
            money[author_id]['work'] = 0
            with open(f'game/money.json', 'w') as s:
                json.dump(money, s, indent=4)
            await ctx.send('계정이 없어서 계정을 생성하였습니다. 통장 잔고는 0원 입니다.')
            return
        await ctx.send('당신의 계정이 삭제되었습니다.')
    @deleteaccount.error
    async def deleteaccount_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:10min:752150489096781966>')

    @commands.command(name="가위바위보", aliases=['묵찌빠','anrWLQK','anrWlQk'])
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def rpc(self, ctx):
        user_id = str(ctx.author.id)
        user_name = str(ctx.author)
        with open("game/money.json", 'r') as f:
            user_data = json.load(f)  # 유저 데이터 불러오는 코드
        try:
            a = user_data[user_id]
            if 30000 > user_data[user_id]['money']:
                await ctx.send('돈이 부족합니다.(요구하는액수 : 30000원)')
                return
        except KeyError:
            await ctx.send('계정을 먼저 생성해주세요.')
            return
        
        await ctx.send("`가위, 바위, 보` 중에서 하나를 5초 안에 말해주세요!")
        

        rpc = ['가위', '바위', '보']
        rpc1 = ['묵', '찌', '빠']

        def check(m):
            return m.content == "가위" or m.content == "바위" or m.content == "보" or m.content == "묵" or m.content == "찌" or m.content == "빠"

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
            await ctx.send(f"{ctx.author.mention}님이 이겼어요... ({ctx.author.name}#{ctx.author.discriminator}님:{answer.content}, 봇:{choice})\n`+10000원`")
            user_data[user_id]["money"] += 10000
        elif result == 3:
            await ctx.send(f"제가 이겼어요! ({ctx.author.name}#{ctx.author.discriminator}님:{answer.content}, 봇:{choice}) `-30000원`")
            user_data[user_id]["money"] -= 30000
        elif result == 2:
            await ctx.send(f"비겼네요. ({ctx.author.name}#{ctx.author.discriminator}님:{answer.content}, 봇:{choice})\n`+5000원`")
            user_data[user_id]["money"] += 5000
        with open("game/money.json", 'w') as f:
            json.dump(user_data, f, indent=4)
    @rpc.error
    async def rpc_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:20s:752150489583452211>')

def setup(bot):
    bot.add_cog(game(bot))
